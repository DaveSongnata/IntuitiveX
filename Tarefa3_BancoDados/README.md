# Tarefa 3 - Banco de Dados

Scripts SQL para criar e popular um banco de dados PostgreSQL com dados das operadoras de saúde da ANS.

## Requisitos

- PostgreSQL 10 ou superior
- Espaço em disco suficiente (os arquivos trimestrais são grandes)

## Tarefas de Preparação (Download Manual)

### 1. Dados das Demonstrações Contábeis (últimos 2 anos)

Baixe os arquivos CSV de:
https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/

Arquivos necessários (últimos 2 anos disponíveis):
- `1T2024.csv`, `2T2024.csv`, `3T2024.csv`, `4T2024.csv`
- `1T2025.csv`, `2T2025.csv`, `3T2025.csv` (4T2025 quando disponível)

### 2. Dados Cadastrais das Operadoras Ativas

Baixe o arquivo de operadoras ativas de:
https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/

O arquivo pode ter nomes como `dados_cadastrais_op.csv` ou `Relatorio_cadop.csv`.

### 3. Coloque os arquivos na pasta `data/`

```
Tarefa3_BancoDados/
├── data/
│   ├── dados_cadastrais_op.csv
│   ├── 1T2024.csv
│   ├── 2T2024.csv
│   ├── 3T2024.csv
│   ├── 4T2024.csv
│   ├── 1T2025.csv
│   ├── 2T2025.csv
│   └── 3T2025.csv
└── scripts/
```

## Scripts SQL

Execute os scripts **na ordem**:

| # | Script | Descrição |
|---|--------|-----------|
| 1 | `01_create_tables_operadoras.sql` | Cria tabelas para operadoras |
| 2 | `02_import_operadoras.sql` | Importa dados das operadoras |
| 3 | `03_create_tables_contabeis.sql` | Cria tabelas para dados contábeis |
| 4 | `04_import_contabeis.sql` | Importa dados trimestrais |
| 5 | `05_queries_analiticas.sql` | Queries para análise |

## Execução

### Via psql (linha de comando):

```bash
# Cria o banco de dados
psql -U postgres -c "CREATE DATABASE ans_teste;"

# Executa os scripts na ordem
psql -U postgres -d ans_teste -f scripts/01_create_tables_operadoras.sql
psql -U postgres -d ans_teste -f scripts/02_import_operadoras.sql
psql -U postgres -d ans_teste -f scripts/03_create_tables_contabeis.sql
psql -U postgres -d ans_teste -f scripts/04_import_contabeis.sql
psql -U postgres -d ans_teste -f scripts/05_queries_analiticas.sql
```

### Via pgAdmin:

1. Abra o pgAdmin
2. Conecte ao seu servidor PostgreSQL
3. Selecione o banco de dados
4. Abra o Query Tool
5. Execute cada script na ordem

## Queries Analíticas

O script `05_queries_analiticas.sql` responde às perguntas:

1. **Top 10 operadoras com maiores despesas no último trimestre**
   - Filtra por "EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR"

2. **Top 10 operadoras com maiores despesas no último ano**
   - Mesma categoria, somando todos os trimestres do ano

## Estrutura do Banco de Dados

### Tabelas Principais

- `operadoras` - Dados cadastrais das operadoras
- `dados_contabeis_trimestral` - Dados financeiros por trimestre
- `plano_contas` - Estrutura hierárquica de contas

### Tabelas de Suporte

- `uf` - Estados brasileiros
- `modalidades` - Tipos de operadoras
- `regioes_comercializacao` - Regiões de atuação

## Estrutura de Arquivos

```
Tarefa3_BancoDados/
├── scripts/
│   ├── 01_create_tables_operadoras.sql
│   ├── 02_import_operadoras.sql
│   ├── 03_create_tables_contabeis.sql
│   ├── 04_import_contabeis.sql
│   └── 05_queries_analiticas.sql
├── data/
│   └── (arquivos CSV baixados)
└── README.md
```

## Problemas Comuns

### Erro de encoding
Certifique-se de que os arquivos CSV estão em UTF-8.

### Erro de caminho
Verifique se o caminho no script está correto e usa barras corretas para seu sistema operacional.

### Erro de permissão
O PostgreSQL precisa de permissão para ler os arquivos. Em alguns casos, pode ser necessário copiar os arquivos para a pasta de dados do PostgreSQL.
