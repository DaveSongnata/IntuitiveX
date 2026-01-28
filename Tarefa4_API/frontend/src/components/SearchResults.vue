<template>
  <div v-if="results.length > 0" class="results-container">
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th v-for="column in displayColumns" :key="column">
              {{ column }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, index) in results"
            :key="index"
            @click="$emit('select', item)"
            class="clickable"
          >
            <td v-for="column in displayColumns" :key="column">
              {{ formatValue(item[column]) }}
            </td>
          </tr>
        </tbody>
      </table>
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
  computed: {
    displayColumns() {
      if (this.results.length === 0) return [];

      // Usa a ordem das colunas se fornecida, senão usa as chaves do primeiro resultado
      if (this.columnOrder.length > 0) {
        return this.columnOrder.filter(col => col in this.results[0]);
      }

      return Object.keys(this.results[0]);
    }
  },
  methods: {
    formatValue(value) {
      if (value === null || value === undefined || value === 'nan') {
        return '-';
      }
      return String(value).substring(0, 50) + (String(value).length > 50 ? '...' : '');
    }
  }
};
</script>

<style scoped>
.results-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

th {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
  white-space: nowrap;
}

tr.clickable {
  cursor: pointer;
  transition: background 0.2s;
}

tr.clickable:hover {
  background: #f3f4f6;
}

td {
  color: #4b5563;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
