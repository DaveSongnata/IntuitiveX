<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">
      <!-- Modal Header -->
      <div class="modal-header">
        <div class="header-content">
          <h2>{{ item.Razao_Social || item.razao_social || 'Detalhes da Operadora' }}</h2>
          <span class="header-badge">{{ item.Modalidade || item.modalidade || 'N/A' }}</span>
        </div>
        <button class="close-btn" @click="$emit('close')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="modal-body">
        <div class="detail-grid">
          <div
            v-for="(value, key) in filteredItem"
            :key="key"
            class="detail-item"
          >
            <span class="detail-label">{{ formatLabel(key) }}</span>
            <span class="detail-value">{{ formatValue(key, value) }}</span>
          </div>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="modal-footer">
        <button class="btn-close" @click="$emit('close')">
          Fechar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DetailModal',
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  emits: ['close'],
  computed: {
    filteredItem() {
      const result = {};
      for (const [key, value] of Object.entries(this.item)) {
        if (value !== null && value !== undefined && value !== '' && value !== 'nan') {
          result[key] = value;
        }
      }
      return result;
    }
  },
  methods: {
    formatLabel(key) {
      return key.replace(/_/g, ' ');
    },
    formatValue(key, value) {
      if (value === null || value === undefined || value === 'nan') {
        return '-';
      }

      const keyLower = key.toLowerCase();

      if (keyLower === 'cnpj') {
        const cleaned = String(value).replace(/\D/g, '');
        if (cleaned.length === 14) {
          return cleaned.replace(
            /^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/,
            '$1.$2.$3/$4-$5'
          );
        }
      }

      if (keyLower === 'cep') {
        const cleaned = String(value).replace(/\D/g, '');
        if (cleaned.length === 8) {
          return cleaned.replace(/^(\d{5})(\d{3})$/, '$1-$2');
        }
      }

      return value;
    }
  },
  mounted() {
    document.body.style.overflow = 'hidden';
  },
  unmounted() {
    document.body.style.overflow = '';
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(17, 24, 39, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 24px;
}

.modal-container {
  background: white;
  border-radius: 16px;
  max-width: 700px;
  width: 100%;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: modalIn 0.2s ease-out;
}

@keyframes modalIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px;
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  border-radius: 16px 16px 0 0;
  color: white;
}

.header-content {
  flex: 1;
  min-width: 0;
}

.modal-header h2 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.header-badge {
  display: inline-block;
  font-size: 12px;
  font-weight: 500;
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  color: white;
  transition: background 0.2s;
  flex-shrink: 0;
  margin-left: 16px;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.close-btn svg {
  width: 20px;
  height: 20px;
  display: block;
}

/* Body */
.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.detail-item {
  padding: 14px 16px;
  background: #F9FAFB;
  border-radius: 10px;
  border: 1px solid #E5E7EB;
}

.detail-label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.detail-value {
  display: block;
  font-size: 14px;
  color: #1F2937;
  word-break: break-word;
}

/* Footer */
.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #E5E7EB;
  display: flex;
  justify-content: flex-end;
}

.btn-close {
  padding: 12px 24px;
  background: #F3F4F6;
  color: #374151;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-close:hover {
  background: #E5E7EB;
}

/* Responsive */
@media (max-width: 640px) {
  .modal-overlay {
    padding: 16px;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }

  .modal-header h2 {
    font-size: 16px;
  }
}
</style>
