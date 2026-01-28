"""
Testes unitários para o módulo de Web Scraping.
"""

import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Adiciona o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import baixar_pdf, extrair_e_baixar_pdfs


class TestBaixarPdf:
    """Testes para a função baixar_pdf"""

    @patch('main.requests.get')
    def test_baixar_pdf_sucesso(self, mock_get, tmp_path):
        """Testa download bem-sucedido de PDF"""
        # Configura o mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content = lambda chunk_size: [b'conteudo_pdf']
        mock_get.return_value = mock_response

        # Executa
        pasta_saida = str(tmp_path / "pdfs")
        resultado = baixar_pdf("http://exemplo.com/arquivo.pdf", pasta_saida)

        # Verifica
        assert resultado is not None
        assert os.path.exists(resultado)

    @patch('main.requests.get')
    def test_baixar_pdf_erro(self, mock_get):
        """Testa tratamento de erro no download"""
        mock_get.side_effect = Exception("Erro de conexão")

        resultado = baixar_pdf("http://exemplo.com/arquivo.pdf")

        assert resultado is None


class TestExtrairEBaixarPdfs:
    """Testes para a função extrair_e_baixar_pdfs"""

    @patch('main.baixar_pdf')
    @patch('main.requests.get')
    def test_extrair_pdfs_com_correspondencias(self, mock_get, mock_baixar):
        """Testa extração quando há PDFs correspondentes"""
        # HTML de exemplo com links de PDF
        html_exemplo = '''
        <html>
            <body>
                <a href="/anexo1.pdf">Anexo I - Documento</a>
                <a href="/anexo2.pdf">Anexo II - Documento</a>
                <a href="/outro.pdf">Outro documento</a>
            </body>
        </html>
        '''
        mock_response = MagicMock()
        mock_response.text = html_exemplo
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        mock_baixar.return_value = "/caminho/arquivo.pdf"

        # Executa
        resultado = extrair_e_baixar_pdfs("http://exemplo.com", ["Anexo I", "Anexo II"])

        # Verifica
        assert len(resultado) == 2

    @patch('main.requests.get')
    def test_extrair_pdfs_sem_correspondencias(self, mock_get):
        """Testa quando não há PDFs correspondentes"""
        html_exemplo = '''
        <html>
            <body>
                <a href="/outro.pdf">Outro documento</a>
            </body>
        </html>
        '''
        mock_response = MagicMock()
        mock_response.text = html_exemplo
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        resultado = extrair_e_baixar_pdfs("http://exemplo.com", ["Anexo I"])

        assert len(resultado) == 0

    @patch('main.requests.get')
    def test_extrair_pdfs_erro_requisicao(self, mock_get):
        """Testa tratamento de erro na requisição"""
        mock_get.side_effect = Exception("Erro de conexão")

        resultado = extrair_e_baixar_pdfs("http://exemplo.com", ["Anexo I"])

        assert len(resultado) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
