<template>
  <div class="search-form">
    <div class="search-tabs">
      <button
        :class="{ active: !advancedMode }"
        @click="advancedMode = false"
      >
        <SearchIcon class="tab-icon" />
        Busca Simples
      </button>
      <button
        :class="{ active: advancedMode }"
        @click="advancedMode = true"
      >
        <FilterIcon class="tab-icon" />
        Busca Avançada
      </button>
    </div>

    <form @submit.prevent="handleSubmit" class="form-content">
      <div v-if="advancedMode" class="field-select">
        <label for="campo">Campo:</label>
        <select id="campo" v-model="selectedField">
          <option value="">Selecione um campo</option>
          <option v-for="field in fields" :key="field" :value="field">
            {{ field }}
          </option>
        </select>
      </div>

      <div class="search-input">
        <label for="consulta">Termo de busca:</label>
        <input
          id="consulta"
          type="text"
          v-model="query"
          :placeholder="advancedMode ? 'Digite o termo para buscar no campo selecionado' : 'Digite para buscar em todos os campos'"
          required
        />
      </div>

      <button type="submit" class="btn-search">
        <SearchIcon class="btn-icon" />
        Pesquisar
      </button>
    </form>
  </div>
</template>

<script>
import SearchIcon from './icons/SearchIcon.vue';
import FilterIcon from './icons/FilterIcon.vue';

export default {
  name: 'SearchForm',
  components: {
    SearchIcon,
    FilterIcon
  },
  props: {
    fields: {
      type: Array,
      default: () => []
    }
  },
  emits: ['search', 'advancedSearch'],
  data() {
    return {
      query: '',
      selectedField: '',
      advancedMode: false
    };
  },
  methods: {
    handleSubmit() {
      if (!this.query.trim()) return;

      if (this.advancedMode && this.selectedField) {
        this.$emit('advancedSearch', this.selectedField, this.query);
      } else {
        this.$emit('search', this.query);
      }
    }
  }
};
</script>

<style scoped>
.search-form {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.search-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-tabs button {
  flex: 1;
  padding: 12px;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.search-tabs button:hover {
  border-color: #3b82f6;
}

.search-tabs button.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.tab-icon {
  width: 18px;
  height: 18px;
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.field-select,
.search-input {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

label {
  font-weight: 500;
  color: #4b5563;
  font-size: 14px;
}

select,
input {
  padding: 12px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.2s;
}

select:focus,
input:focus {
  outline: none;
  border-color: #3b82f6;
}

.btn-search {
  padding: 14px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background 0.2s;
}

.btn-search:hover {
  background: #2563eb;
}

.btn-icon {
  width: 20px;
  height: 20px;
}
</style>
