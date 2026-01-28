# Testes de Nivelamento - IntuitiveCare

Projeto contendo os 4 testes de nivelamento para a vaga de estágio na IntuitiveCare.

**Autor:** Dave
**Data:** Janeiro/2026

## Estrutura do Projeto

```
IntuitiveX/
├── Tarefa1_WebScraping/        # Teste 1 - Web Scraping
├── Tarefa2_TransformacaoDados/ # Teste 2 - Transformação de Dados
├── Tarefa3_BancoDados/         # Teste 3 - Banco de Dados
├── Tarefa4_API/                # Teste 4 - API
└── README.md
```

## Testes

### Tarefa 1 - Web Scraping

Acessa o site da ANS, baixa os Anexos I e II em PDF e compacta em um arquivo ZIP.

```bash
cd Tarefa1_WebScraping
pip install -r requirements.txt
python main.py
```

**Saída:** `arquivos_pdf.zip`

---

### Tarefa 2 - Transformação de Dados

Extrai dados da tabela "Rol de Procedimentos" do PDF do Anexo I e salva em CSV.

```bash
cd Tarefa2_TransformacaoDados
pip install -r requirements.txt
python main.py <caminho_do_pdf>
```

**Saída:** `Teste_Dave.zip`

---

### Tarefa 3 - Banco de Dados

Scripts SQL para criar e popular um banco de dados PostgreSQL com dados das operadoras de saúde.

```bash
cd Tarefa3_BancoDados

# 1. Baixe os dados manualmente (ver README da tarefa)
# 2. Crie o banco de dados:
psql -U postgres -c "CREATE DATABASE ans_teste;"

# 3. Execute os scripts SQL na ordem:
psql -U postgres -d ans_teste -f scripts/01_create_tables_operadoras.sql
psql -U postgres -d ans_teste -f scripts/02_import_operadoras.sql
psql -U postgres -d ans_teste -f scripts/03_create_tables_contabeis.sql
psql -U postgres -d ans_teste -f scripts/04_import_contabeis.sql
psql -U postgres -d ans_teste -f scripts/05_queries_analiticas.sql
```

**Saída:** Queries analíticas com top 10 operadoras

---

### Tarefa 4 - API

Interface web Vue.js com servidor Python Flask para busca de operadoras.

```bash
# Backend
cd Tarefa4_API/backend
pip install -r requirements.txt
python app.py

# Frontend (em outro terminal)
cd Tarefa4_API/frontend
npm install
npm run serve
```

**Acesso:**
- Backend: http://localhost:8000
- Frontend: http://localhost:8080

---

## Requisitos Gerais

- Python 3.8+
- Node.js 16+
- PostgreSQL 10+
- Postman (para testar a API)

## Tecnologias Utilizadas

| Tarefa | Tecnologias |
|--------|-------------|
| 1 | Python, requests, BeautifulSoup |
| 2 | Python, pdfplumber, pandas |
| 3 | PostgreSQL, SQL |
| 4 | Python Flask, Vue.js 3, Axios |

## Licença

Este projeto foi desenvolvido como parte do processo seletivo da IntuitiveCare.
