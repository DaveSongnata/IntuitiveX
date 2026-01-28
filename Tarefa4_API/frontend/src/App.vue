<template>
  <div class="app">
    <!-- Header -->
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-text">Intuitive</span>
          <span class="logo-accent">Care</span>
        </div>
        <nav class="nav">
          <a href="#" class="nav-link active">Pesquisa</a>
          <div class="nav-dropdown">
            <span class="nav-link nav-dropdown-toggle">
              Dados ANS
              <svg class="dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 9l6 6 6-6"/>
              </svg>
            </span>
            <div class="dropdown-menu">
              <a href="https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/" target="_blank" class="dropdown-item">
                Operadoras Ativas
              </a>
              <a href="https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/" target="_blank" class="dropdown-item">
                Demonstrações Contábeis
              </a>
            </div>
          </div>
        </nav>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1>Pesquisa de Operadoras</h1>
        <p class="hero-subtitle">
          Consulte informações cadastrais de operadoras de planos de saúde
          registradas na ANS de forma rápida e simples.
        </p>
      </div>
    </section>

    <!-- Main Content -->
    <main class="main-content">
      <SearchForm
        @search="performSearch"
        @advancedSearch="performAdvancedSearch"
        :fields="fields"
      />

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <Spinner />
        <p>Pesquisando operadoras...</p>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="message message-error">
        <span class="message-icon">!</span>
        {{ error }}
      </div>

      <!-- Results Count -->
      <div v-if="showResults && resultCount > 0" class="results-header">
        <div class="results-count">
          <span class="count-number">{{ resultCount }}</span>
          <span class="count-label">{{ resultCount === 1 ? 'resultado encontrado' : 'resultados encontrados' }}</span>
        </div>
        <p class="results-tip">Clique em uma operadora para ver todos os detalhes</p>
      </div>

      <!-- No Results -->
      <div v-if="showResults && resultCount === 0" class="message message-warning">
        <span class="message-icon">?</span>
        Nenhuma operadora encontrada para esta pesquisa.
      </div>

      <!-- Results -->
      <SearchResults
        :results="results"
        :columnOrder="fields"
        @select="showDetail"
      />

      <!-- Pagination -->
      <div v-if="showResults && totalPaginas > 1" class="pagination">
        <button
          class="page-btn"
          :disabled="paginaAtual === 1"
          @click="mudarPagina(1)"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 17l-5-5 5-5M18 17l-5-5 5-5"/>
          </svg>
        </button>
        <button
          class="page-btn"
          :disabled="paginaAtual === 1"
          @click="mudarPagina(paginaAtual - 1)"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15 18l-6-6 6-6"/>
          </svg>
        </button>

        <span class="page-info">
          Página <strong>{{ paginaAtual }}</strong> de <strong>{{ totalPaginas }}</strong>
        </span>

        <button
          class="page-btn"
          :disabled="paginaAtual === totalPaginas"
          @click="mudarPagina(paginaAtual + 1)"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 18l6-6-6-6"/>
          </svg>
        </button>
        <button
          class="page-btn"
          :disabled="paginaAtual === totalPaginas"
          @click="mudarPagina(totalPaginas)"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M13 17l5-5-5-5M6 17l5-5-5-5"/>
          </svg>
        </button>
      </div>

      <!-- Detail Modal -->
      <DetailModal
        v-if="selectedItem"
        :item="selectedItem"
        @close="selectedItem = null"
      />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <p>Dados obtidos da ANS - Agência Nacional de Saúde Suplementar</p>
      <div class="footer-links">
        <a href="https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/" target="_blank">Operadoras Ativas</a>
        <span class="footer-divider">|</span>
        <a href="https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/" target="_blank">Demonstrações Contábeis</a>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';
import SearchForm from './components/SearchForm.vue';
import SearchResults from './components/SearchResults.vue';
import DetailModal from './components/DetailModal.vue';
import Spinner from './components/Spinner.vue';

export default {
  name: 'App',
  components: {
    SearchForm,
    SearchResults,
    DetailModal,
    Spinner
  },
  data() {
    return {
      results: [],
      resultCount: 0,
      fields: [],
      loading: false,
      showResults: false,
      error: null,
      selectedItem: null,
      // Paginação
      paginaAtual: 1,
      porPagina: 20,
      totalPaginas: 1,
      // Guarda última consulta para paginação
      ultimaConsulta: '',
      ultimoCampo: '',
      modoAvancado: false
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
        this.error = 'Erro ao conectar com o servidor. Verifique se o backend está rodando.';
      }
    },

    async performSearch(query, pagina = 1) {
      this.loading = true;
      this.showResults = false;
      this.error = null;
      this.ultimaConsulta = query;
      this.modoAvancado = false;

      try {
        const response = await axios.get(
          `/api/pesquisa?consulta=${encodeURIComponent(query)}&pagina=${pagina}&por_pagina=${this.porPagina}`
        );
        this.results = response.data.resultados;
        this.resultCount = response.data.contagem;
        this.paginaAtual = response.data.paginacao.pagina;
        this.totalPaginas = response.data.paginacao.total_paginas;
        this.showResults = true;
      } catch (error) {
        console.error('Erro na pesquisa:', error);
        this.error = error.response?.data?.erro || 'Erro ao realizar pesquisa.';
      } finally {
        this.loading = false;
      }
    },

    async performAdvancedSearch(field, query, pagina = 1) {
      this.loading = true;
      this.showResults = false;
      this.error = null;
      this.ultimaConsulta = query;
      this.ultimoCampo = field;
      this.modoAvancado = true;

      try {
        const response = await axios.get(
          `/api/pesquisa/avancada?campo=${encodeURIComponent(field)}&consulta=${encodeURIComponent(query)}&pagina=${pagina}&por_pagina=${this.porPagina}`
        );
        this.results = response.data.resultados;
        this.resultCount = response.data.contagem;
        this.paginaAtual = response.data.paginacao.pagina;
        this.totalPaginas = response.data.paginacao.total_paginas;
        this.showResults = true;
      } catch (error) {
        console.error('Erro na pesquisa avançada:', error);
        this.error = error.response?.data?.erro || 'Erro ao realizar pesquisa avançada.';
      } finally {
        this.loading = false;
      }
    },

    mudarPagina(novaPagina) {
      if (novaPagina < 1 || novaPagina > this.totalPaginas) return;

      if (this.modoAvancado) {
        this.performAdvancedSearch(this.ultimoCampo, this.ultimaConsulta, novaPagina);
      } else {
        this.performSearch(this.ultimaConsulta, novaPagina);
      }
    },

    showDetail(item) {
      this.selectedItem = item;
    }
  }
};
</script>

<style>
/* Reset & Base */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #FAFAFA;
  color: #1F2937;
  line-height: 1.6;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header */
.header {
  background: white;
  border-bottom: 1px solid #E5E7EB;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: 700;
}

.logo-text {
  color: #7C3AED;
}

.logo-accent {
  color: #1F2937;
}

.nav {
  display: flex;
  gap: 32px;
}

.nav-link {
  color: #6B7280;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.active {
  color: #7C3AED;
}

/* Dropdown */
.nav-dropdown {
  position: relative;
}

.nav-dropdown-toggle {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

.dropdown-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.2s;
}

.nav-dropdown:hover .dropdown-icon {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-8px);
  transition: all 0.2s;
}

.nav-dropdown:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-item {
  display: block;
  padding: 12px 16px;
  color: #374151;
  text-decoration: none;
  font-size: 14px;
  transition: background 0.2s;
}

.dropdown-item:first-child {
  border-radius: 8px 8px 0 0;
}

.dropdown-item:last-child {
  border-radius: 0 0 8px 8px;
}

.dropdown-item:hover {
  background: #F5F3FF;
  color: #7C3AED;
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  padding: 48px 24px;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  color: white;
}

.hero h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 1.125rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
  flex: 1;
  width: 100%;
}

/* Loading */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48px;
  color: #6B7280;
}

.loading-container p {
  margin-top: 16px;
  font-size: 14px;
}

/* Messages */
.message {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  font-size: 14px;
}

.message-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.message-error {
  background: #FEF2F2;
  color: #DC2626;
  border: 1px solid #FECACA;
}

.message-error .message-icon {
  background: #DC2626;
  color: white;
}

.message-warning {
  background: #FFFBEB;
  color: #D97706;
  border: 1px solid #FDE68A;
}

.message-warning .message-icon {
  background: #D97706;
  color: white;
}

/* Results Header */
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px 20px;
  background: #F5F3FF;
  border-radius: 12px;
  border: 1px solid #DDD6FE;
}

.results-count {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.count-number {
  font-size: 28px;
  font-weight: 700;
  color: #7C3AED;
}

.count-label {
  color: #6B7280;
  font-size: 14px;
}

.results-tip {
  color: #7C3AED;
  font-size: 13px;
}

/* Footer */
.footer {
  background: #1F2937;
  color: #9CA3AF;
  padding: 24px;
  text-align: center;
  font-size: 14px;
  margin-top: auto;
}

.footer p {
  margin-bottom: 8px;
}

.footer-links {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

.footer-divider {
  color: #4B5563;
}

.footer a {
  color: #A78BFA;
  text-decoration: none;
}

.footer a:hover {
  text-decoration: underline;
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 32px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
}

.page-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 2px solid #E5E7EB;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn svg {
  width: 18px;
  height: 18px;
  color: #6B7280;
}

.page-btn:hover:not(:disabled) {
  border-color: #7C3AED;
  background: #F5F3FF;
}

.page-btn:hover:not(:disabled) svg {
  color: #7C3AED;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #6B7280;
  padding: 0 16px;
}

.page-info strong {
  color: #7C3AED;
  font-weight: 600;
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
  }

  .hero h1 {
    font-size: 1.75rem;
  }

  .results-header {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
}
</style>
