"""
Teste 4 - API Backend

Servidor Flask que realiza busca textual na lista de cadastros de operadoras.

Uso:
    python app.py

Endpoints:
    GET /api/pesquisa?consulta={termo}
    GET /api/pesquisa/avancada?campo={coluna}&consulta={termo}
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

    Returns:
        DataFrame com os dados das operadoras
    """
    try:
        logger.debug("Carregando arquivo CSV...")

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
                logger.debug(f"CSV carregado com encoding {encoding}")
                break
            except UnicodeDecodeError:
                logger.debug(f"Falha com encoding {encoding}")
                continue

        if df is None:
            raise Exception("Não foi possível carregar o CSV com nenhum encoding")

        # Limpa valores numéricos (remove .0 de inteiros)
        for col in df.columns:
            df[col] = df[col].apply(limpar_valor)

        logger.debug(f"Colunas: {df.columns.tolist()}")
        logger.debug(f"Total de linhas: {len(df)}")

        return df

    except Exception as e:
        logger.error(f"Erro ao carregar CSV: {str(e)}")
        raise


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
    Busca simples em todas as colunas.

    Query params:
        consulta: Termo de busca

    Returns:
        JSON com contagem e resultados
    """
    try:
        consulta = request.args.get('consulta', '')
        logger.debug(f"Busca simples: {consulta}")

        if not consulta:
            return jsonify({'erro': 'O parâmetro de consulta é obrigatório'}), 400

        # Carrega dados (já vem com valores limpos)
        df = carregar_csv()

        # Cria máscara de busca (case-insensitive)
        mascara = pd.Series(False, index=df.index)

        for col in df.columns:
            mascara = mascara | df[col].str.contains(
                consulta, case=False, regex=False, na=False
            )

        # Filtra e converte para dict
        resultado = df[mascara].to_dict(orient='records')
        logger.debug(f"Encontrados {len(resultado)} resultados")

        return jsonify({
            'contagem': len(resultado),
            'resultados': resultado
        })

    except Exception as e:
        logger.error(f"Erro na busca: {str(e)}")
        return jsonify({'erro': str(e)}), 500


@app.route('/api/pesquisa/avancada', methods=['GET'])
def pesquisa_avancada():
    """
    Busca em um campo específico.

    Query params:
        campo: Nome da coluna
        consulta: Termo de busca

    Returns:
        JSON com contagem e resultados
    """
    try:
        campo = request.args.get('campo', '')
        consulta = request.args.get('consulta', '')
        logger.debug(f"Busca avançada - Campo: {campo}, Consulta: {consulta}")

        if not consulta or not campo:
            return jsonify({'erro': 'Os parâmetros campo e consulta são obrigatórios'}), 400

        # Carrega dados (já vem com valores limpos)
        df = carregar_csv()

        # Verifica se o campo existe
        if campo not in df.columns:
            logger.error(f"Campo não encontrado: {campo}")
            return jsonify({'erro': f'Campo {campo} não encontrado'}), 400

        # Filtra pelo campo específico
        mascara = df[campo].str.contains(
            consulta, case=False, regex=False, na=False
        )
        resultado = df[mascara].to_dict(orient='records')
        logger.debug(f"Encontrados {len(resultado)} resultados")

        return jsonify({
            'contagem': len(resultado),
            'resultados': resultado
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
    print("  GET /api/pesquisa?consulta={termo}")
    print("  GET /api/pesquisa/avancada?campo={coluna}&consulta={termo}")
    print("  GET /api/campos")
    print("  GET /teste")
    print("=" * 50)

    app.run(host='0.0.0.0', port=8000, debug=True)
