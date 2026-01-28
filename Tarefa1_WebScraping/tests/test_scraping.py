"""
Testes para o módulo de Web Scraping (Tarefa 1)

Execução:
    pytest tests/test_scraping.py -v
"""

import pytest
import os
import sys
import tempfile
import zipfile
from unittest.mock import patch, MagicMock

# Adiciona o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import baixar_pdf, extrair_e_baixar_pdfs, compactar_pasta


class TestBaixarPDF:
    """Testes para a função baixar_pdf"""

    def test_baixar_pdf_sucesso(self):
        """Testa download bem-sucedido de um PDF"""
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_response = MagicMock()
            mock_response.iter_content.return_value = [b'%PDF-1.4 conteudo fake']
            mock_response.raise_for_status = MagicMock()

            with patch('main.requests.get', return_value=mock_response):
                resultado = baixar_pdf(
                    'https://exemplo.com/arquivo.pdf',
                    pasta_saida=temp_dir
                )

            assert resultado is not None
            assert resultado.endswith('.pdf')
            assert os.path.exists(resultado)

    def test_baixar_pdf_adiciona_extensao(self):
        """Testa se adiciona .pdf quando URL não tem extensão"""
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_response = MagicMock()
            mock_response.iter_content.return_value = [b'conteudo']
            mock_response.raise_for_status = MagicMock()

            with patch('main.requests.get', return_value=mock_response):
                resultado = baixar_pdf(
                    'https://exemplo.com/arquivo',
                    pasta_saida=temp_dir
                )

            assert resultado.endswith('.pdf')

    def test_baixar_pdf_erro_conexao(self):
        """Testa tratamento de erro de conexão"""
        with patch('main.requests.get', side_effect=Exception('Erro de conexão')):
            resultado = baixar_pdf('https://exemplo.com/arquivo.pdf')

        assert resultado is None


class TestExtrairEBaixarPDFs:
    """Testes para a função extrair_e_baixar_pdfs"""

    def test_encontra_links_anexos(self):
        """Testa se encontra links de Anexo I e Anexo II"""
        html_mock = '''
        <html>
            <body>
                <a href="/anexo1.pdf">Anexo I - Procedimentos</a>
                <a href="/anexo2.pdf">Anexo II - Diretrizes</a>
                <a href="/outro.pdf">Outro documento</a>
            </body>
        </html>
        '''

        mock_response = MagicMock()
        mock_response.text = html_mock
        mock_response.raise_for_status = MagicMock()

        with patch('main.requests.get', return_value=mock_response):
            with patch('main.baixar_pdf', return_value='/tmp/arquivo.pdf') as mock_baixar:
                resultado = extrair_e_baixar_pdfs(
                    'https://exemplo.com',
                    ['Anexo I', 'Anexo II']
                )

        # Deve encontrar 2 PDFs (Anexo I e Anexo II)
        assert mock_baixar.call_count == 2
        assert len(resultado) == 2

    def test_nenhum_link_encontrado(self):
        """Testa quando não encontra links correspondentes"""
        html_mock = '<html><body><a href="/outro.pdf">Outro</a></body></html>'

        mock_response = MagicMock()
        mock_response.text = html_mock
        mock_response.raise_for_status = MagicMock()

        with patch('main.requests.get', return_value=mock_response):
            resultado = extrair_e_baixar_pdfs(
                'https://exemplo.com',
                ['Anexo I', 'Anexo II']
            )

        assert resultado == []

    def test_erro_acesso_pagina(self):
        """Testa tratamento de erro ao acessar página"""
        import requests
        with patch('main.requests.get', side_effect=requests.RequestException('Erro')):
            resultado = extrair_e_baixar_pdfs(
                'https://exemplo.com',
                ['Anexo I']
            )

        assert resultado == []


class TestCompactarPasta:
    """Testes para a função compactar_pasta"""

    def test_compactar_pasta_sucesso(self):
        """Testa compactação de arquivos em ZIP"""
        with tempfile.TemporaryDirectory() as temp_dir:
            arquivo1 = os.path.join(temp_dir, 'teste1.pdf')
            arquivo2 = os.path.join(temp_dir, 'teste2.pdf')

            with open(arquivo1, 'w') as f:
                f.write('conteudo1')
            with open(arquivo2, 'w') as f:
                f.write('conteudo2')

            arquivo_zip = os.path.join(temp_dir, 'saida.zip')
            compactar_pasta(temp_dir, arquivo_zip)

            assert os.path.exists(arquivo_zip)

            with zipfile.ZipFile(arquivo_zip, 'r') as zf:
                nomes = zf.namelist()
                assert 'teste1.pdf' in nomes
                assert 'teste2.pdf' in nomes


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
