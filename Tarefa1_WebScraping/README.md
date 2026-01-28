# Tarefa 1 - Web Scraping

Este teste realiza web scraping no site da ANS para baixar os Anexos I e II em formato PDF e compactá-los em um arquivo ZIP.

## Requisitos

- Python 3.8+
- Bibliotecas: requests, beautifulsoup4

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

## O que o script faz

1. Acessa o site: https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos
2. Busca por links de PDFs que contenham "Anexo I" e "Anexo II"
3. Baixa os PDFs para uma pasta temporária `arquivos_pdf/`
4. Compacta todos os PDFs em `arquivos_pdf.zip`
5. Remove a pasta temporária

## Saída

- `arquivos_pdf.zip` - Arquivo ZIP contendo os Anexos I e II

## Testes

```bash
pytest tests/ -v
```

## Estrutura

```
Tarefa1_WebScraping/
├── main.py           # Script principal
├── requirements.txt  # Dependências
├── tests/
│   └── test_scraping.py  # Testes unitários
└── README.md
```
