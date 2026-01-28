<template>
  <div v-if="results.length > 0" class="results-grid">
    <div
      v-for="(item, index) in results"
      :key="index"
      class="result-card"
      @click="$emit('select', item)"
    >
      <!-- Card Header -->
      <div class="card-header">
        <h3 class="company-name">{{ item.Razao_Social || item.razao_social || 'Operadora' }}</h3>
        <span class="badge" :class="getBadgeClass(item)">
          {{ item.Modalidade || item.modalidade || 'N/A' }}
        </span>
      </div>

      <!-- Card Body -->
      <div class="card-body">
        <div class="info-row">
          <span class="info-label">Registro ANS</span>
          <span class="info-value">{{ item.Registro_ANS || item.registro_ans || '-' }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">CNPJ</span>
          <span class="info-value">{{ formatCNPJ(item.CNPJ || item.cnpj) }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Cidade/UF</span>
          <span class="info-value">{{ formatLocation(item) }}</span>
        </div>
      </div>

      <!-- Card Footer -->
      <div class="card-footer">
        <span class="view-details">
          Ver detalhes
          <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchResults',
  props: {
    results: {
      type: Array,
      default: () => []
    },
    columnOrder: {
      type: Array,
      default: () => []
    }
  },
  emits: ['select'],
  methods: {
    formatCNPJ(cnpj) {
      if (!cnpj) return '-';
      const cleaned = String(cnpj).replace(/\D/g, '');
      if (cleaned.length !== 14) return cnpj;
      return cleaned.replace(
        /^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/,
        '$1.$2.$3/$4-$5'
      );
    },
    formatLocation(item) {
      const cidade = item.Cidade || item.cidade || '';
      const uf = item.UF || item.uf || '';
      if (!cidade && !uf) return '-';
      return `${cidade}${cidade && uf ? '/' : ''}${uf}`;
    },
    getBadgeClass(item) {
      const modalidade = (item.Modalidade || item.modalidade || '').toLowerCase();
      if (modalidade.includes('cooperativa')) return 'badge-green';
      if (modalidade.includes('autogestão')) return 'badge-blue';
      if (modalidade.includes('seguradora')) return 'badge-yellow';
      if (modalidade.includes('medicina de grupo')) return 'badge-purple';
      return 'badge-gray';
    }
  }
};
</script>

<style scoped>
.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
}

.result-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
}

.result-card:hover {
  border-color: #7C3AED;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
  transform: translateY(-2px);
}

/* Card Header */
.card-header {
  padding: 16px 20px;
  border-bottom: 1px solid #F3F4F6;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.company-name {
  font-size: 15px;
  font-weight: 600;
  color: #1F2937;
  margin: 0;
  line-height: 1.4;
  flex: 1;
}

.badge {
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
  white-space: nowrap;
  flex-shrink: 0;
}

.badge-purple {
  background: #F5F3FF;
  color: #7C3AED;
}

.badge-green {
  background: #ECFDF5;
  color: #059669;
}

.badge-blue {
  background: #EFF6FF;
  color: #2563EB;
}

.badge-yellow {
  background: #FFFBEB;
  color: #D97706;
}

.badge-gray {
  background: #F3F4F6;
  color: #6B7280;
}

/* Card Body */
.card-body {
  padding: 16px 20px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.info-row:not(:last-child) {
  border-bottom: 1px solid #F3F4F6;
}

.info-label {
  font-size: 13px;
  color: #6B7280;
}

.info-value {
  font-size: 13px;
  font-weight: 500;
  color: #1F2937;
  text-align: right;
}

/* Card Footer */
.card-footer {
  padding: 12px 20px;
  background: #FAFAFA;
  border-top: 1px solid #F3F4F6;
}

.view-details {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
  color: #7C3AED;
}

.arrow-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.2s;
}

.result-card:hover .arrow-icon {
  transform: translateX(4px);
}

/* Responsive */
@media (max-width: 640px) {
  .results-grid {
    grid-template-columns: 1fr;
  }
}
</style>
