<template>
  <div class="container">
    <h1>Pesquisa de Operadoras ANS</h1>

    <SearchForm
      @search="performSearch"
      @advancedSearch="performAdvancedSearch"
      :fields="fields"
    />

    <div v-if="loading" class="loading">
      <Spinner />
      <p>Pesquisando...</p>
    </div>

    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <div v-if="showResults && resultCount > 0" class="alert alert-tip">
      <TipIcon class="tip-icon" />
      Dica: Clique nos resultados para ver mais detalhes.
    </div>

    <div v-if="showResults && resultCount > 0" class="alert alert-info">
      Encontrados {{ resultCount }} resultados
    </div>

    <div v-if="showResults && resultCount === 0" class="alert alert-warning">
      Nenhum resultado encontrado.
    </div>

    <SearchResults
      :results="results"
      :columnOrder="fields"
      @select="showDetail"
    />

    <DetailModal
      v-if="selectedItem"
      :item="selectedItem"
      @close="selectedItem = null"
    />
  </div>
</template>

<script>
import axios from 'axios';
import SearchForm from './components/SearchForm.vue';
import SearchResults from './components/SearchResults.vue';
import DetailModal from './components/DetailModal.vue';
import Spinner from './components/Spinner.vue';
import TipIcon from './components/icons/TipIcon.vue';

export default {
  name: 'App',
  components: {
    SearchForm,
    SearchResults,
    DetailModal,
    Spinner,
    TipIcon
  },
  data() {
    return {
      results: [],
      resultCount: 0,
      fields: [],
      loading: false,
      showResults: false,
      error: null,
      selectedItem: null
    };
  },
  mounted() {
    this.loadFields();
  },
  methods: {
    async loadFields() {
      try {
        const response = await axios.get('/api/campos');
        this.fields = response.data.campos;
        this.error = null;
      } catch (error) {
        console.error('Erro ao carregar campos:', error);
        this.error = 'Erro ao carregar campos. Verifique se o servidor está rodando.';
      }
    },

    async performSearch(query) {
      this.loading = true;
      this.showResults = false;
      this.error = null;

      try {
        const response = await axios.get(`/api/pesquisa?consulta=${encodeURIComponent(query)}`);
        this.results = response.data.resultados;
        this.resultCount = response.data.contagem;
        this.showResults = true;
      } catch (error) {
        console.error('Erro na pesquisa:', error);
        this.error = error.response?.data?.erro || 'Erro ao realizar pesquisa.';
      } finally {
        this.loading = false;
      }
    },

    async performAdvancedSearch(field, query) {
      this.loading = true;
      this.showResults = false;
      this.error = null;

      try {
        const response = await axios.get(
          `/api/pesquisa/avancada?campo=${encodeURIComponent(field)}&consulta=${encodeURIComponent(query)}`
        );
        this.results = response.data.resultados;
        this.resultCount = response.data.contagem;
        this.showResults = true;
      } catch (error) {
        console.error('Erro na pesquisa avançada:', error);
        this.error = error.response?.data?.erro || 'Erro ao realizar pesquisa avançada.';
      } finally {
        this.loading = false;
      }
    },

    showDetail(item) {
      this.selectedItem = item;
    }
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background-color: #f5f5f5;
  color: #333;
  line-height: 1.6;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 2rem;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 2rem 0;
}

.loading p {
  margin-top: 10px;
  color: #666;
}

.alert {
  padding: 12px 20px;
  border-radius: 8px;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.alert-error {
  background-color: #fee2e2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.alert-info {
  background-color: #dbeafe;
  color: #1d4ed8;
  border: 1px solid #bfdbfe;
}

.alert-warning {
  background-color: #fef3c7;
  color: #d97706;
  border: 1px solid #fde68a;
}

.alert-tip {
  background-color: #f0fdf4;
  color: #16a34a;
  border: 1px solid #bbf7d0;
}

.tip-icon {
  width: 20px;
  height: 20px;
}
</style>
