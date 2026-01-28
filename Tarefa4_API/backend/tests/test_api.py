"""
Testes para a API Flask (Tarefa 4)

Execução:
    pytest tests/test_api.py -v
"""

import pytest
import pandas as pd
import os
import sys
from unittest.mock import patch

# Adiciona o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, limpar_valor


@pytest.fixture
def client():
    """Fixture que cria um cliente de teste"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_dataframe():
    """Fixture que cria um DataFrame de teste"""
    return pd.DataFrame({
        'Registro_ANS': ['123456', '789012'],
        'CNPJ': ['12345678000199', '98765432000188'],
        'Razao_Social': ['Operadora Teste', 'Outra Operadora'],
        'Modalidade': ['Medicina de Grupo', 'Cooperativa'],
        'Cidade': ['São Paulo', 'Rio de Janeiro'],
        'UF': ['SP', 'RJ']
    })


class TestLimparValor:
    """Testes para a função limpar_valor"""

    def test_limpar_valor_float_inteiro(self):
        """Testa conversão de float para int"""
        assert limpar_valor(32.0) == '32'
        assert limpar_valor(100.0) == '100'

    def test_limpar_valor_float_decimal(self):
        """Testa que float com decimal mantém decimal"""
        assert limpar_valor(32.5) == '32.5'

    def test_limpar_valor_string(self):
        """Testa que string permanece igual"""
        assert limpar_valor('texto') == 'texto'

    def test_limpar_valor_nan(self):
        """Testa que NaN vira string vazia"""
        assert limpar_valor(pd.NA) == ''
        assert limpar_valor(float('nan')) == ''

    def test_limpar_valor_none(self):
        """Testa que None vira string vazia"""
        assert limpar_valor(None) == ''


class TestHealthCheck:
    """Testes para o endpoint /teste"""

    def test_health_check(self, client):
        """Testa se o health check retorna status ok"""
        response = client.get('/teste')

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert 'mensagem' in data


class TestPesquisaSimples:
    """Testes para o endpoint /api/pesquisa"""

    def test_pesquisa_sem_parametro(self, client):
        """Testa erro quando não passa parâmetro"""
        response = client.get('/api/pesquisa')

        assert response.status_code == 400
        data = response.get_json()
        assert 'erro' in data

    def test_pesquisa_parametro_vazio(self, client):
        """Testa erro quando parâmetro está vazio"""
        response = client.get('/api/pesquisa?consulta=')

        assert response.status_code == 400

    def test_pesquisa_com_resultados(self, client, mock_dataframe):
        """Testa pesquisa que retorna resultados"""
        with patch('app.carregar_csv', return_value=mock_dataframe):
            response = client.get('/api/pesquisa?consulta=Teste')

        assert response.status_code == 200
        data = response.get_json()
        assert 'contagem' in data
        assert 'resultados' in data
        assert data['contagem'] >= 1

    def test_pesquisa_sem_resultados(self, client, mock_dataframe):
        """Testa pesquisa que não retorna resultados"""
        with patch('app.carregar_csv', return_value=mock_dataframe):
            response = client.get('/api/pesquisa?consulta=XYZABC123')

        assert response.status_code == 200
        data = response.get_json()
        assert data['contagem'] == 0
        assert data['resultados'] == []

    def test_pesquisa_case_insensitive(self, client, mock_dataframe):
        """Testa que pesquisa é case-insensitive"""
        with patch('app.carregar_csv', return_value=mock_dataframe):
            response1 = client.get('/api/pesquisa?consulta=teste')
            response2 = client.get('/api/pesquisa?consulta=TESTE')

        data1 = response1.get_json()
        data2 = response2.get_json()
        assert data1['contagem'] == data2['contagem']


class TestPesquisaAvancada:
    """Testes para o endpoint /api/pesquisa/avancada"""

    def test_pesquisa_avancada_sem_parametros(self, client):
        """Testa erro quando não passa parâmetros"""
        response = client.get('/api/pesquisa/avancada')

        assert response.status_code == 400

    def test_pesquisa_avancada_campo_invalido(self, client, mock_dataframe):
        """Testa erro quando campo não existe"""
        with patch('app.carregar_csv', return_value=mock_dataframe):
            response = client.get('/api/pesquisa/avancada?campo=CampoInexistente&consulta=teste')

        assert response.status_code == 400
        data = response.get_json()
        assert 'erro' in data

    def test_pesquisa_avancada_sucesso(self, client, mock_dataframe):
        """Testa pesquisa avançada bem-sucedida"""
        with patch('app.carregar_csv', return_value=mock_dataframe):
            response = client.get('/api/pesquisa/avancada?campo=UF&consulta=SP')

        assert response.status_code == 200
        data = response.get_json()
        assert data['contagem'] == 1
        assert data['resultados'][0]['UF'] == 'SP'


class TestCampos:
    """Testes para o endpoint /api/campos"""

    def test_listar_campos(self, client, mock_dataframe):
        """Testa listagem de campos disponíveis"""
        with patch('app.carregar_csv', return_value=mock_dataframe):
            response = client.get('/api/campos')

        assert response.status_code == 200
        data = response.get_json()
        assert 'campos' in data
        assert 'Registro_ANS' in data['campos']
        assert 'Razao_Social' in data['campos']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
