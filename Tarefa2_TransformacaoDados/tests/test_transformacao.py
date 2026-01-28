"""
Testes para o módulo de Transformação de Dados (Tarefa 2)

Execução:
    pytest tests/test_transformacao.py -v
"""

import pytest
import pandas as pd
import os
import sys

# Adiciona o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import limpar_texto, processar_tabelas, MAPEAMENTO_LEGENDA, SCHEMA


class TestLimparTexto:
    """Testes para a função limpar_texto"""

    def test_limpar_texto_com_quebras(self):
        """Testa remoção de quebras de linha"""
        texto = "Texto\ncom\nquebras"
        resultado = limpar_texto(texto)
        assert resultado == "Texto com quebras"

    def test_limpar_texto_com_espacos_extras(self):
        """Testa remoção de espaços extras"""
        texto = "Texto   com   muitos    espaços"
        resultado = limpar_texto(texto)
        assert resultado == "Texto com muitos espaços"

    def test_limpar_texto_com_tabs(self):
        """Testa remoção de tabs"""
        texto = "Texto\tcom\ttabs"
        resultado = limpar_texto(texto)
        assert resultado == "Texto com tabs"

    def test_limpar_texto_nulo(self):
        """Testa tratamento de valor nulo"""
        resultado = limpar_texto(None)
        assert resultado is None

    def test_limpar_texto_nan(self):
        """Testa tratamento de NaN"""
        resultado = limpar_texto(pd.NA)
        assert pd.isna(resultado)

    def test_limpar_texto_vazio(self):
        """Testa texto vazio"""
        resultado = limpar_texto("")
        assert resultado == ""

    def test_limpar_texto_apenas_espacos(self):
        """Testa texto com apenas espaços"""
        resultado = limpar_texto("   ")
        assert resultado == ""


class TestMapeamentoLegenda:
    """Testes para o mapeamento de legendas OD/AMB"""

    def test_mapeamento_od(self):
        """Testa se OD está mapeado corretamente"""
        assert 'OD' in MAPEAMENTO_LEGENDA
        assert MAPEAMENTO_LEGENDA['OD'] == 'Seg. Odontológica'

    def test_mapeamento_amb(self):
        """Testa se AMB está mapeado corretamente"""
        assert 'AMB' in MAPEAMENTO_LEGENDA
        assert MAPEAMENTO_LEGENDA['AMB'] == 'Seg. Ambulatorial'


class TestProcessarTabelas:
    """Testes para a função processar_tabelas"""

    def test_processar_tabela_simples(self):
        """Testa processamento de uma tabela simples"""
        df = pd.DataFrame({
            'PROCEDIMENTO': ['Consulta\nmédica', 'Exame'],
            'OD': ['OD', 'OD'],
            'AMB': ['AMB', 'AMB']
        })

        resultado = processar_tabelas([df])

        # Verifica limpeza de texto
        assert 'Consulta médica' in resultado['PROCEDIMENTO'].values

        # Verifica substituição de OD/AMB
        assert 'Seg. Odontológica' in resultado['OD'].values
        assert 'Seg. Ambulatorial' in resultado['AMB'].values

    def test_processar_tabelas_combinadas(self):
        """Testa combinação de múltiplas tabelas"""
        df1 = pd.DataFrame({
            'PROCEDIMENTO': ['Proc1'],
            'OD': ['OD']
        })
        df2 = pd.DataFrame({
            'PROCEDIMENTO': ['Proc2'],
            'OD': ['OD']
        })

        resultado = processar_tabelas([df1, df2])

        assert len(resultado) == 2
        assert 'Proc1' in resultado['PROCEDIMENTO'].values
        assert 'Proc2' in resultado['PROCEDIMENTO'].values

    def test_processar_tabela_remove_linhas_vazias(self):
        """Testa remoção de linhas completamente vazias"""
        df = pd.DataFrame({
            'PROCEDIMENTO': ['Proc1', None, 'Proc2'],
            'OD': ['OD', None, 'OD']
        })

        resultado = processar_tabelas([df])

        # Linha com todos None deve ser removida
        assert len(resultado) == 2

    def test_processar_tabela_vazia_erro(self):
        """Testa que lista vazia gera erro"""
        with pytest.raises(SystemExit):
            processar_tabelas([])


class TestSchema:
    """Testes para validação do schema"""

    def test_schema_contem_colunas_obrigatorias(self):
        """Testa se schema contém colunas obrigatórias"""
        colunas_obrigatorias = ['PROCEDIMENTO', 'OD', 'AMB']

        for coluna in colunas_obrigatorias:
            assert coluna in SCHEMA

    def test_schema_tipos_corretos(self):
        """Testa se tipos estão corretos no schema"""
        assert SCHEMA['PROCEDIMENTO'] == str
        assert SCHEMA['DUT'] == 'Int64'  # Nullable integer


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
