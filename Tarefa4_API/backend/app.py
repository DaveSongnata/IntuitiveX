"""
Teste 4 - API Backend

Servidor Flask que realiza busca textual na lista de cadastros de operadoras.

Uso:
    python app.py

Endpoints:
    GET /api/pesquisa?consulta={termo}&pagina=1&por_pagina=20
    GET /api/pesquisa/avancada?campo={coluna}&consulta={termo}&pagina=1&por_pagina=20
    GET /api/campos
    GET /teste

Autor: Dave
Data: Janeiro/2026
"""

from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os
import logging
import sys

# Configuração de logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Inicializa o Flask
app = Flask(__name__,
            static_folder='../frontend/dist',
            template_folder='../frontend/dist')

# =============================================================================
# Cache do DataFrame (Performance)
# =============================================================================

_df_cache = None


def limpar_valor(valor):
    """
    Converte valor para string, removendo .0 de floats inteiros.
    Ex: 32.0 -> "32", "texto" -> "texto", NaN -> ""
    """
    if pd.isna(valor):
        return ''
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor)


def carregar_csv():
    """
    Carrega o arquivo CSV com tratamento de encoding.
    Usa cache para evitar recarregar a cada request.

    Returns:
        DataFrame com os dados das operadoras
    """
    global _df_cache

    # Retorna cache se já carregado
    if _df_cache is not None:
        logger.debug("Usando DataFrame do cache")
        return _df_cache

    try:
        logger.info("Carregando arquivo CSV (primeira vez)...")

        # Tenta diferentes encodings
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        df = None

        for encoding in encodings:
            try:
                logger.debug(f"Tentando encoding {encoding}...")
                df = pd.read_csv(
                    'dados_cadastrais_op.csv',
                    encoding=encoding,
                    delimiter=';',
                    quotechar='"'
                )
                logger.info(f"CSV carregado com encoding {encoding}")
                break
            except UnicodeDecodeError:
                logger.debug(f"Falha com encoding {encoding}")
                continue

        if df is None:
            raise Exception("Não foi possível carregar o CSV com nenhum encoding")

        # Limpa valores numéricos (remove .0 de inteiros)
        for col in df.columns:
            df[col] = df[col].apply(limpar_valor)

        logger.info(f"Colunas: {df.columns.tolist()}")
        logger.info(f"Total de linhas: {len(df)}")

        # Armazena no cache
        _df_cache = df
        return df

    except Exception as e:
        logger.error(f"Erro ao carregar CSV: {str(e)}")
        raise


def paginar(resultados, pagina, por_pagina):
    """
    Aplica paginação a uma lista de resultados.

    Args:
        resultados: Lista de dicionários
        pagina: Número da página (1-indexed)
        por_pagina: Quantidade por página

    Returns:
        Dict com resultados paginados e metadados
    """
    total = len(resultados)
    total_paginas = (total + por_pagina - 1) // por_pagina if por_pagina > 0 else 1

    # Garante que página está no range válido
    pagina = max(1, min(pagina, total_paginas)) if total_paginas > 0 else 1

    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina

    return {
        'resultados': resultados[inicio:fim],
        'paginacao': {
            'pagina': pagina,
            'por_pagina': por_pagina,
            'total': total,
            'total_paginas': total_paginas
        }
    }


# =============================================================================
# Rotas da API
# =============================================================================

@app.route('/')
def index():
    """Serve o frontend Vue.js"""
    if os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory(app.static_folder, 'index.html')
    return jsonify({
        "mensagem": "API de Busca de Operadoras ANS",
        "endpoints": {
            "/api/pesquisa": "Busca simples",
            "/api/pesquisa/avancada": "Busca por campo específico",
            "/api/campos": "Lista campos disponíveis",
            "/teste": "Health check"
        }
    })


@app.route('/js/<path:path>')
def serve_js(path):
    """Serve arquivos JavaScript"""
    return send_from_directory(os.path.join(app.static_folder, 'js'), path)


@app.route('/css/<path:path>')
def serve_css(path):
    """Serve arquivos CSS"""
    return send_from_directory(os.path.join(app.static_folder, 'css'), path)


@app.route('/api/pesquisa', methods=['GET'])
def pesquisar():
    """
    Busca simples em todas as colunas com paginação.

    Query params:
        consulta: Termo de busca (obrigatório)
        pagina: Número da página (default: 1)
        por_pagina: Resultados por página (default: 20, max: 100)

    Returns:
        JSON com contagem, paginação e resultados
    """
    try:
        consulta = request.args.get('consulta', '')
        pagina = request.args.get('pagina', 1, type=int)
        por_pagina = min(request.args.get('por_pagina', 20, type=int), 100)

        logger.debug(f"Busca simples: {consulta} (página {pagina})")

        if not consulta:
            return jsonify({'erro': 'O parâmetro de consulta é obrigatório'}), 400

        # Carrega dados do cache
        df = carregar_csv()

        # Cria máscara de busca (case-insensitive)
        mascara = pd.Series(False, index=df.index)

        for col in df.columns:
            mascara = mascara | df[col].str.contains(
                consulta, case=False, regex=False, na=False
            )

        # Filtra e converte para dict
        todos_resultados = df[mascara].to_dict(orient='records')
        logger.debug(f"Encontrados {len(todos_resultados)} resultados")

        # Aplica paginação
        dados_paginados = paginar(todos_resultados, pagina, por_pagina)

        return jsonify({
            'contagem': dados_paginados['paginacao']['total'],
            'paginacao': dados_paginados['paginacao'],
            'resultados': dados_paginados['resultados']
        })

    except Exception as e:
        logger.error(f"Erro na busca: {str(e)}")
        return jsonify({'erro': str(e)}), 500


@app.route('/api/pesquisa/avancada', methods=['GET'])
def pesquisa_avancada():
    """
    Busca em um campo específico com paginação.

    Query params:
        campo: Nome da coluna (obrigatório)
        consulta: Termo de busca (obrigatório)
        pagina: Número da página (default: 1)
        por_pagina: Resultados por página (default: 20, max: 100)

    Returns:
        JSON com contagem, paginação e resultados
    """
    try:
        campo = request.args.get('campo', '')
        consulta = request.args.get('consulta', '')
        pagina = request.args.get('pagina', 1, type=int)
        por_pagina = min(request.args.get('por_pagina', 20, type=int), 100)

        logger.debug(f"Busca avançada - Campo: {campo}, Consulta: {consulta} (página {pagina})")

        if not consulta or not campo:
            return jsonify({'erro': 'Os parâmetros campo e consulta são obrigatórios'}), 400

        # Carrega dados do cache
        df = carregar_csv()

        # Verifica se o campo existe
        if campo not in df.columns:
            logger.error(f"Campo não encontrado: {campo}")
            return jsonify({'erro': f'Campo {campo} não encontrado'}), 400

        # Filtra pelo campo específico
        mascara = df[campo].str.contains(
            consulta, case=False, regex=False, na=False
        )
        todos_resultados = df[mascara].to_dict(orient='records')
        logger.debug(f"Encontrados {len(todos_resultados)} resultados")

        # Aplica paginação
        dados_paginados = paginar(todos_resultados, pagina, por_pagina)

        return jsonify({
            'contagem': dados_paginados['paginacao']['total'],
            'paginacao': dados_paginados['paginacao'],
            'resultados': dados_paginados['resultados']
        })

    except Exception as e:
        logger.error(f"Erro na busca avançada: {str(e)}")
        return jsonify({'erro': str(e)}), 500


@app.route('/api/campos', methods=['GET'])
def obter_campos():
    """
    Lista os campos disponíveis para busca.

    Returns:
        JSON com lista de campos
    """
    try:
        df = carregar_csv()
        campos = list(df.columns)
        logger.debug(f"Campos disponíveis: {campos}")

        return jsonify({
            'campos': campos
        })

    except Exception as e:
        logger.error(f"Erro ao obter campos: {str(e)}")
        return jsonify({'erro': str(e)}), 500


@app.route('/teste', methods=['GET'])
def teste():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "mensagem": "Servidor funcionando!"
    })


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    print("=" * 50)
    print("Teste 4 - API Backend")
    print("=" * 50)
    print("\nIniciando servidor Flask...")
    print("Acesse: http://localhost:8000")
    print("\nEndpoints disponíveis:")
    print("  GET /api/pesquisa?consulta={termo}&pagina=1&por_pagina=20")
    print("  GET /api/pesquisa/avancada?campo={coluna}&consulta={termo}")
    print("  GET /api/campos")
    print("  GET /teste")
    print("=" * 50)

    # Pré-carrega o CSV no startup
    print("\nCarregando dados...")
    carregar_csv()
    print("Dados carregados com sucesso!\n")

    app.run(host='0.0.0.0', port=8000, debug=True)
