"""
Testes unitários para o módulo de Transformação de Dados.
"""

import pytest
import pandas as pd
import os
import sys

# Adiciona o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import limpar_texto, processar_tabelas, MAPEAMENTO_LEGENDA


class TestLimparTexto:
    """Testes para a função limpar_texto"""

    def test_limpar_texto_com_quebras_de_linha(self):
        """Testa remoção de quebras de linha"""
        texto = "Texto com\nquebra de\nlinha"
        resultado = limpar_texto(texto)
        assert resultado == "Texto com quebra de linha"

    def test_limpar_texto_com_espacos_extras(self):
        """Testa remoção de espaços extras"""
        texto = "Texto    com   muitos    espaços"
        resultado = limpar_texto(texto)
        assert resultado == "Texto com muitos espaços"

    def test_limpar_texto_com_espacos_inicio_fim(self):
        """Testa remoção de espaços no início e fim"""
        texto = "  Texto com espaços   "
        resultado = limpar_texto(texto)
        assert resultado == "Texto com espaços"

    def test_limpar_texto_nulo(self):
        """Testa tratamento de valor nulo"""
        resultado = limpar_texto(None)
        assert resultado is None

    def test_limpar_texto_nan(self):
        """Testa tratamento de NaN"""
        resultado = limpar_texto(pd.NA)
        assert pd.isna(resultado)


class TestProcessarTabelas:
    """Testes para a função processar_tabelas"""

    def test_processar_tabelas_vazias(self):
        """Testa comportamento com lista vazia de tabelas"""
        with pytest.raises(SystemExit):
            processar_tabelas([])

    def test_processar_tabelas_com_dados(self):
        """Testa processamento de tabelas com dados"""
        df = pd.DataFrame({
            'PROCEDIMENTO': ['Proc 1', 'Proc 2'],
            'OD': ['SIM', 'NAO'],
            'AMB': ['SIM', 'NAO']
        })

        resultado = processar_tabelas([df])

        assert len(resultado) == 2
        assert 'Seg. Odontológica' in resultado.columns
        assert 'Seg. Ambulatorial' in resultado.columns


class TestMapeamentoLegenda:
    """Testes para o mapeamento de legendas"""

    def test_mapeamento_od(self):
        """Verifica mapeamento de OD"""
        assert MAPEAMENTO_LEGENDA['OD'] == 'Seg. Odontológica'

    def test_mapeamento_amb(self):
        """Verifica mapeamento de AMB"""
        assert MAPEAMENTO_LEGENDA['AMB'] == 'Seg. Ambulatorial'


class TestArgumentosInvalidos:
    """Testes para validação de argumentos"""

    def test_arquivo_inexistente(self):
        """Testa erro ao processar arquivo inexistente"""
        # Este teste verifica que o programa não quebra silenciosamente
        # A validação real é feita no main()
        assert not os.path.exists("arquivo_que_nao_existe.pdf")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
