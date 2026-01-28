# Tarefa 4 - API

API de busca de operadoras de saúde com interface web Vue.js e servidor Python Flask.

## Requisitos

- Python 3.8+
- Node.js 16+
- npm ou yarn

## Estrutura

```
Tarefa4_API/
├── backend/
│   ├── app.py              # Servidor Flask
│   ├── requirements.txt    # Dependências Python
│   └── Relatorio_cadop.csv # Dados das operadoras
├── frontend/
│   ├── src/                # Código fonte Vue.js
│   ├── public/             # Arquivos estáticos
│   └── package.json        # Dependências Node.js
├── postman/
│   └── IntuitiveCare_API.postman_collection.json
└── README.md
```

## Preparação

### 1. Obter o arquivo CSV

Copie o arquivo `Relatorio_cadop.csv` para a pasta `backend/`.

Este arquivo pode ser obtido em:
https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/

## Executando o Backend

```bash
cd backend

# Instalar dependências
pip install -r requirements.txt

# Executar o servidor
python app.py
```

O servidor estará disponível em: http://localhost:8000

## Executando o Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run serve
```

O frontend estará disponível em: http://localhost:8080

### Build para produção

```bash
npm run build
```

Os arquivos de build serão gerados em `frontend/dist/`.

## Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/pesquisa?consulta={termo}` | Busca em todas as colunas |
| GET | `/api/pesquisa/avancada?campo={coluna}&consulta={termo}` | Busca em coluna específica |
| GET | `/api/campos` | Lista campos disponíveis |
| GET | `/teste` | Health check |

### Exemplos de uso

```bash
# Busca simples
curl "http://localhost:8000/api/pesquisa?consulta=unimed"

# Busca avançada
curl "http://localhost:8000/api/pesquisa/avancada?campo=Razao_Social&consulta=bradesco"

# Listar campos
curl "http://localhost:8000/api/campos"

# Health check
curl "http://localhost:8000/teste"
```

## Coleção Postman

Importe o arquivo `postman/IntuitiveCare_API.postman_collection.json` no Postman para testar a API.

A coleção inclui:
- Health Check
- Listar Campos
- Busca Simples (vários exemplos)
- Busca Avançada (vários exemplos)

## Tecnologias

### Backend
- Flask - Framework web Python
- Pandas - Processamento de dados
- Flask-CORS - Cross-Origin Resource Sharing

### Frontend
- Vue.js 3 - Framework JavaScript
- Vue CLI - Build tool
- Axios - Cliente HTTP
