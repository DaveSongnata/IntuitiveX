<template>
  <div class="search-card">
    <!-- Search Type Tabs -->
    <div class="search-tabs">
      <button
        :class="['tab-btn', { active: !advancedMode }]"
        @click="advancedMode = false"
      >
        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.35-4.35"/>
        </svg>
        Busca Simples
      </button>
      <button
        :class="['tab-btn', { active: advancedMode }]"
        @click="advancedMode = true"
      >
        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
        </svg>
        Busca Avançada
      </button>
    </div>

    <!-- Search Form -->
    <form @submit.prevent="handleSubmit" class="search-form">
      <!-- Field Select (Advanced Mode) -->
      <div v-if="advancedMode" class="form-group">
        <label for="campo">Campo de busca</label>
        <div class="select-wrapper">
          <svg class="select-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <path d="M9 9h6M9 12h6M9 15h4"/>
          </svg>
          <select id="campo" v-model="selectedField" class="form-select">
            <option value="">Selecione um campo...</option>
            <option v-for="field in fields" :key="field" :value="field">
              {{ formatFieldName(field) }}
            </option>
          </select>
          <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 9l6 6 6-6"/>
          </svg>
        </div>
      </div>

      <!-- Search Input -->
      <div class="form-group">
        <label for="consulta">
          {{ advancedMode ? 'Termo de busca' : 'Pesquisar operadora' }}
        </label>
        <div class="input-wrapper">
          <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.35-4.35"/>
          </svg>
          <input
            id="consulta"
            type="text"
            v-model="query"
            :placeholder="advancedMode ? 'Digite o valor para buscar...' : 'Nome, CNPJ, cidade...'"
            class="form-input"
            required
          />
        </div>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="btn-search" :disabled="!canSubmit">
        Pesquisar
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'SearchForm',
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
  computed: {
    canSubmit() {
      if (!this.query.trim()) return false;
      if (this.advancedMode && !this.selectedField) return false;
      return true;
    }
  },
  methods: {
    handleSubmit() {
      if (!this.canSubmit) return;

      if (this.advancedMode) {
        this.$emit('advancedSearch', this.selectedField, this.query);
      } else {
        this.$emit('search', this.query);
      }
    },
    formatFieldName(field) {
      return field.replace(/_/g, ' ');
    }
  }
};
</script>

<style scoped>
.search-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 24px;
  margin-bottom: 24px;
}

/* Tabs */
.search-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.tab-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 20px;
  border: 2px solid #E5E7EB;
  background: white;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  border-color: #7C3AED;
  color: #7C3AED;
}

.tab-btn.active {
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  border-color: transparent;
  color: white;
}

.tab-icon {
  width: 18px;
  height: 18px;
}

/* Form */
.search-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

/* Custom Select */
.select-wrapper {
  position: relative;
  background: linear-gradient(135deg, #FAFAFA 0%, #F5F3FF 100%);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.select-wrapper:hover {
  background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
}

.select-wrapper:focus-within {
  background: linear-gradient(135deg, #EDE9FE 0%, #DDD6FE 100%);
}

.select-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #7C3AED;
  pointer-events: none;
  z-index: 1;
  transition: color 0.2s;
}

.select-wrapper:focus-within .select-icon {
  color: #5B21B6;
}

.select-arrow {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #7C3AED;
  pointer-events: none;
  transition: transform 0.3s ease, color 0.2s;
}

.select-wrapper:focus-within .select-arrow {
  transform: translateY(-50%) rotate(180deg);
  color: #5B21B6;
}

.form-select {
  width: 100%;
  padding: 16px 48px;
  border: 2px solid transparent;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  color: #1F2937;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

.select-wrapper:hover .form-select {
  border-color: #DDD6FE;
}

.select-wrapper:focus-within .form-select {
  border-color: #7C3AED;
}

.form-select:focus {
  outline: none;
}

.form-select option {
  padding: 12px;
  background: white;
  color: #1F2937;
}

.form-select option:checked {
  background: #F5F3FF;
  color: #7C3AED;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #9CA3AF;
}

.form-input {
  width: 100%;
  padding: 14px 16px 14px 48px;
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  font-size: 15px;
  color: #1F2937;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #7C3AED;
}

.form-input::placeholder {
  color: #9CA3AF;
}

/* Button */
.btn-search {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px 24px;
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-search:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
}

.btn-search:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-icon {
  width: 20px;
  height: 20px;
}

/* Responsive */
@media (max-width: 640px) {
  .search-tabs {
    flex-direction: column;
  }
}
</style>
