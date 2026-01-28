# Tarefa 2 - Transformação de Dados

Este teste extrai dados da tabela "Rol de Procedimentos e Eventos em Saúde" do PDF do Anexo I, salva em CSV estruturado e compacta como `Teste_Dave.zip`.

## Requisitos

- Python 3.8+
- Bibliotecas: pdfplumber, pandas

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py <caminho_do_arquivo_pdf>
```

### Exemplo

```bash
python main.py Anexo_I.pdf
```

## O que o script faz

1. Abre o PDF com pdfplumber
2. Itera por todas as páginas extraindo tabelas
3. Combina todas as tabelas em um único DataFrame
4. Limpa o texto (remove quebras de linha, espaços extras)
5. Substitui as abreviações OD e AMB pelas descrições completas:
   - OD → Seg. Odontológica
   - AMB → Seg. Ambulatorial
6. Salva os dados em CSV
7. Compacta o CSV em `Teste_Dave.zip`

## Saída

- `Teste_Dave.zip` - Arquivo ZIP contendo o CSV com os dados extraídos

## Mapeamento de Legendas

Conforme rodapé do PDF:

| Abreviação | Descrição Completa |
|------------|-------------------|
| OD         | Seg. Odontológica |
| AMB        | Seg. Ambulatorial |

## Testes

```bash
pytest tests/ -v
```

## Estrutura

```
Tarefa2_TransformacaoDados/
├── main.py           # Script principal
├── requirements.txt  # Dependências
├── tests/
│   └── test_transformacao.py  # Testes unitários
└── README.md
```
