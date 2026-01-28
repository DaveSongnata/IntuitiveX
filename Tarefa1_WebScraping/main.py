"""
Teste 1 - Web Scraping

Acessa o site da ANS, baixa os Anexos I e II em formato PDF
e compacta todos os anexos em um arquivo ZIP.

Uso:
    python main.py

Autor: Dave
Data: Janeiro/2026
"""

import requests
from bs4 import BeautifulSoup
import os
import zipfile
import shutil
from urllib.parse import urljoin


def baixar_pdf(url, pasta_saida="arquivos_pdf"):
    """
    Baixa um arquivo PDF de uma URL e salva na pasta especificada.

    Args:
        url: URL do arquivo PDF
        pasta_saida: Pasta onde o arquivo será salvo

    Returns:
        Caminho do arquivo baixado ou None em caso de erro
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Extrai o nome do arquivo da URL
        nome_arquivo = url.split("/")[-1]

        # Garante que tenha extensão .pdf
        if not nome_arquivo.lower().endswith(".pdf"):
            nome_arquivo += ".pdf"

        # Cria a pasta de saída se não existir
        os.makedirs(pasta_saida, exist_ok=True)
        caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)

        # Salva o arquivo em chunks para economizar memória
        with open(caminho_arquivo, "wb") as arquivo:
            for bloco in response.iter_content(chunk_size=8192):
                if bloco:
                    arquivo.write(bloco)

        print(f"Arquivo baixado: {nome_arquivo}")
        return caminho_arquivo

    except Exception as erro:
        print(f"Erro ao baixar {url}: {erro}")
        return None


def extrair_e_baixar_pdfs(url_pagina, textos_busca):
    """
    Acessa uma página web, encontra links de PDFs que correspondem
    aos textos de busca e faz o download.

    Args:
        url_pagina: URL da página a ser acessada
        textos_busca: Lista de textos para filtrar os links (ex: ["Anexo I", "Anexo II"])

    Returns:
        Lista de caminhos dos arquivos baixados
    """
    try:
        response = requests.get(url_pagina)
        response.raise_for_status()
    except requests.RequestException as erro:
        print(f"Erro ao acessar a página {url_pagina}: {erro}")
        return []

    # Parse do HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontra todos os links
    links = soup.find_all("a", href=True)
    links_correspondentes = []

    # Filtra links que são PDFs e contêm os textos de busca
    for link in links:
        href = link["href"]
        texto_link = link.get_text().lower()

        # Constrói URL completa
        url_completa = urljoin(url_pagina, href)

        # Verifica se é um PDF e contém algum texto de busca
        if href.lower().endswith(".pdf"):
            for texto_busca in textos_busca:
                if texto_busca.lower() in texto_link:
                    links_correspondentes.append(url_completa)
                    break

    if not links_correspondentes:
        print("Nenhum PDF correspondente encontrado.")
        return []

    print(f"Encontrados {len(links_correspondentes)} PDF(s) correspondente(s).")

    # Baixa os PDFs
    arquivos_baixados = []
    for link_pdf in links_correspondentes:
        caminho = baixar_pdf(link_pdf)
        if caminho:
            arquivos_baixados.append(caminho)

    return arquivos_baixados


def compactar_pasta(pasta_origem, arquivo_zip):
    """
    Compacta todos os arquivos de uma pasta em um arquivo ZIP.

    Args:
        pasta_origem: Pasta contendo os arquivos a serem compactados
        arquivo_zip: Nome do arquivo ZIP de saída
    """
    with zipfile.ZipFile(arquivo_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for arquivo in os.listdir(pasta_origem):
            caminho_completo = os.path.join(pasta_origem, arquivo)
            if os.path.isfile(caminho_completo):
                zipf.write(caminho_completo, arquivo)
    print(f"Arquivos compactados em: {arquivo_zip}")


def main():
    """Função principal que executa o web scraping."""

    # URL da página da ANS
    url_pagina = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

    # Textos para buscar nos links
    textos_busca = ["Anexo I", "Anexo II"]

    # Pasta temporária para os PDFs
    pasta_pdfs = "arquivos_pdf"

    # Arquivo ZIP de saída
    arquivo_zip = "arquivos_pdf.zip"

    print("=" * 50)
    print("Teste 1 - Web Scraping")
    print("=" * 50)
    print(f"\nAcessando: {url_pagina}")
    print(f"Buscando: {', '.join(textos_busca)}\n")

    # Baixa os PDFs
    arquivos = extrair_e_baixar_pdfs(url_pagina, textos_busca)

    if not arquivos:
        print("\nErro: Nenhum arquivo foi baixado.")
        return

    print(f"\n{len(arquivos)} arquivo(s) baixado(s) com sucesso.")

    # Compacta os arquivos
    if os.path.exists(pasta_pdfs):
        compactar_pasta(pasta_pdfs, arquivo_zip)

        # Remove a pasta temporária
        shutil.rmtree(pasta_pdfs)
        print(f"Pasta temporária '{pasta_pdfs}' removida.")
    else:
        print("Erro: Pasta de PDFs não encontrada.")
        return

    print("\n" + "=" * 50)
    print("Concluído!")
    print(f"Arquivo gerado: {arquivo_zip}")
    print("=" * 50)


if __name__ == "__main__":
    main()
