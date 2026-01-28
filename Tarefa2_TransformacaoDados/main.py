"""
Teste 2 - Transformação de Dados

Extrai dados da tabela "Rol de Procedimentos e Eventos em Saúde" do PDF do Anexo I,
salva em CSV estruturado e compacta como Teste_Dave.zip.

Uso:
    python main.py <caminho_do_arquivo_pdf>

Exemplo:
    python main.py Anexo_I.pdf

Autor: Dave
Data: Janeiro/2026
"""

import pdfplumber
import pandas as pd
import zipfile
import sys
import os


# Schema das colunas esperadas
SCHEMA = {
    'PROCEDIMENTO': str,
    'RN (alteração)': str,
    'VIGÊNCIA': str,
    'OD': str,
    'AMB': str,
    'HCO': str,
    'HSO': str,
    'REF': str,
    'PAC': str,
    'DUT': 'Int64',
    'SUBGRUPO': str,
    'GRUPO': str,
    'CAPÍTULO': str
}

# Mapeamento de legendas conforme rodapé do PDF
MAPEAMENTO_LEGENDA = {
    'OD': 'Seg. Odontológica',
    'AMB': 'Seg. Ambulatorial'
}


def limpar_texto(texto):
    """
    Limpa o texto removendo quebras de linha e espaços extras.

    Args:
        texto: Texto a ser limpo

    Returns:
        Texto limpo ou o valor original se for nulo
    """
    if pd.isna(texto):
        return texto
    return ' '.join(str(texto).strip().replace('\n', ' ').split())


def extrair_tabelas_do_pdf(caminho_pdf):
    """
    Extrai todas as tabelas de um arquivo PDF.

    Args:
        caminho_pdf: Caminho do arquivo PDF

    Returns:
        Lista de DataFrames com as tabelas extraídas
    """
    tabelas = []

    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            total_paginas = len(pdf.pages)
            print(f"Total de páginas: {total_paginas}")

            for i, pagina in enumerate(pdf.pages):
                print(f"Processando página {i + 1}/{total_paginas}...", end='\r')

                # Extrai tabelas da página
                tabelas_pagina = pagina.extract_tables()

                if tabelas_pagina:
                    for tabela in tabelas_pagina:
                        if tabela and len(tabela) > 1:
                            # Limpa os cabeçalhos
                            cabecalhos = [limpar_texto(c) for c in tabela[0]]
                            # Cria DataFrame
                            df = pd.DataFrame(tabela[1:], columns=cabecalhos)
                            tabelas.append(df)

            print(f"\nTabelas extraídas: {len(tabelas)}")

    except Exception as erro:
        print(f"Erro ao processar PDF: {str(erro)}")
        sys.exit(1)

    return tabelas


def processar_tabelas(tabelas):
    """
    Processa e combina as tabelas extraídas, aplicando limpeza e transformações.

    Args:
        tabelas: Lista de DataFrames

    Returns:
        DataFrame processado
    """
    if not tabelas:
        print("Nenhuma tabela encontrada no PDF")
        sys.exit(1)

    # Combina todas as tabelas
    df_combinado = pd.concat(tabelas, ignore_index=True)

    # Remove linhas completamente vazias
    df_combinado = df_combinado.dropna(how='all')

    # Limpa o texto, aplica mapeamento de legendas e substitui vazios
    for coluna in df_combinado.columns:
        df_combinado[coluna] = df_combinado[coluna].apply(limpar_texto)

        # Substitui valores OD/AMB pelas descrições completas (conforme rodapé do PDF)
        if coluna in MAPEAMENTO_LEGENDA:
            df_combinado[coluna] = df_combinado[coluna].replace(MAPEAMENTO_LEGENDA)

        df_combinado[coluna] = df_combinado[coluna].replace('', pd.NA)

    # Aplica tipos de dados do schema
    for coluna, tipo_dado in SCHEMA.items():
        if coluna in df_combinado.columns:
            if tipo_dado == 'Int64':
                df_combinado[coluna] = pd.to_numeric(
                    df_combinado[coluna], errors='coerce'
                ).astype('Int64')
            else:
                df_combinado[coluna] = df_combinado[coluna].fillna('').astype(tipo_dado)

    # Reset do índice
    df_combinado = df_combinado.reset_index(drop=True)

    return df_combinado


def main():
    """Função principal que executa a transformação de dados."""

    # Verifica argumentos
    if len(sys.argv) != 2:
        print("Uso: python main.py <caminho_do_arquivo_pdf>")
        print("Exemplo: python main.py Anexo_I.pdf")
        sys.exit(1)

    caminho_pdf = sys.argv[1]

    # Verifica se o arquivo existe
    if not os.path.exists(caminho_pdf):
        print(f"Erro: Arquivo '{caminho_pdf}' não encontrado")
        sys.exit(1)

    print("=" * 50)
    print("Teste 2 - Transformação de Dados")
    print("=" * 50)
    print(f"\nArquivo: {caminho_pdf}\n")

    # Extrai tabelas do PDF
    print("Extraindo tabelas do PDF...")
    tabelas = extrair_tabelas_do_pdf(caminho_pdf)

    # Processa as tabelas
    print("\nProcessando tabelas...")
    df = processar_tabelas(tabelas)

    print(f"Total de registros: {len(df)}")
    print(f"Colunas: {list(df.columns)}")

    # Define nomes dos arquivos de saída
    nome_base = os.path.splitext(os.path.basename(caminho_pdf))[0]
    arquivo_csv = f"{nome_base}.csv"
    arquivo_zip = "Teste_Dave.zip"

    # Salva como CSV
    df.to_csv(arquivo_csv, index=False, encoding='utf-8')
    print(f"\nDados salvos em: {arquivo_csv}")

    # Compacta o CSV
    with zipfile.ZipFile(arquivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(arquivo_csv, os.path.basename(arquivo_csv))
    print(f"Arquivo compactado em: {arquivo_zip}")

    # Remove o CSV (mantém apenas o ZIP)
    os.remove(arquivo_csv)
    print(f"Arquivo CSV removido (mantido apenas no ZIP)")

    print("\n" + "=" * 50)
    print("Concluído!")
    print(f"Arquivo gerado: {arquivo_zip}")
    print("=" * 50)


if __name__ == "__main__":
    main()
