-- =============================================================================
-- Script 04: Importação dos dados contábeis trimestrais
-- Compatível com PostgreSQL 10+
--
-- IMPORTANTE: Execute este script APÓS os scripts 01, 02 e 03
-- =============================================================================

-- =============================================================================
-- Verificações de segurança
-- =============================================================================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'operadoras') THEN
        RAISE EXCEPTION 'Tabela operadoras não existe. Execute os scripts 01 e 02 primeiro.';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'dados_contabeis_trimestral') THEN
        RAISE EXCEPTION 'Tabela dados_contabeis_trimestral não existe. Execute o script 03 primeiro.';
    END IF;
END
$$;

-- =============================================================================
-- Cria tabela temporária para importação
-- =============================================================================
CREATE TEMPORARY TABLE temp_dados_contabeis (
    data VARCHAR(20),
    registro_ans VARCHAR(10),
    codigo_conta_contabil VARCHAR(20),
    descricao_conta VARCHAR(255),
    valor_saldo_inicial VARCHAR(50),
    valor_saldo_final VARCHAR(50)
);

-- =============================================================================
-- Função para importar um arquivo CSV trimestral
-- =============================================================================
CREATE OR REPLACE FUNCTION importar_dados_trimestrais(
    caminho_arquivo TEXT,
    trimestre TEXT,
    ano INTEGER
)
RETURNS INTEGER AS $$
DECLARE
    contagem_linhas INTEGER := 0;
    contagem_inseridos INTEGER := 0;
BEGIN
    -- Limpa a tabela temporária
    TRUNCATE TABLE temp_dados_contabeis;

    -- Importa dados do CSV
    EXECUTE format(
        'COPY temp_dados_contabeis FROM %L WITH (FORMAT csv, DELIMITER '';'', HEADER true, QUOTE ''"'', ENCODING ''UTF8'')',
        caminho_arquivo
    );

    -- Conta linhas importadas
    SELECT COUNT(*) INTO contagem_linhas FROM temp_dados_contabeis;

    -- Insere no plano de contas (códigos únicos)
    INSERT INTO plano_contas (codigo_conta_contabil, descricao_conta, nivel, tipo_conta)
    SELECT DISTINCT
        TRIM(codigo_conta_contabil),
        TRIM(descricao_conta),
        CASE
            WHEN LENGTH(TRIM(codigo_conta_contabil)) <= 2 THEN 1
            WHEN LENGTH(TRIM(codigo_conta_contabil)) <= 4 THEN 2
            WHEN LENGTH(TRIM(codigo_conta_contabil)) <= 6 THEN 3
            WHEN LENGTH(TRIM(codigo_conta_contabil)) <= 8 THEN 4
            ELSE 5
        END,
        CASE
            WHEN LEFT(TRIM(codigo_conta_contabil), 1) = '1' THEN 'Ativo'
            WHEN LEFT(TRIM(codigo_conta_contabil), 1) = '2' THEN 'Passivo'
            WHEN LEFT(TRIM(codigo_conta_contabil), 1) = '3' THEN 'Patrimônio Líquido'
            WHEN LEFT(TRIM(codigo_conta_contabil), 1) = '4' THEN 'Receita'
            WHEN LEFT(TRIM(codigo_conta_contabil), 1) = '5' THEN 'Despesa'
            ELSE 'Outro'
        END
    FROM temp_dados_contabeis
    WHERE codigo_conta_contabil IS NOT NULL
    ON CONFLICT (codigo_conta_contabil) DO NOTHING;

    -- Insere dados contábeis (apenas para operadoras existentes)
    INSERT INTO dados_contabeis_trimestral (
        data_referencia,
        registro_ans,
        codigo_conta_contabil,
        descricao_conta,
        valor_saldo_inicial,
        valor_saldo_final,
        trimestre,
        ano
    )
    SELECT
        -- Converte data
        CASE
            WHEN TRIM(data) ~ '^\d{4}-\d{2}-\d{2}$'
            THEN TO_DATE(TRIM(data), 'YYYY-MM-DD')
            WHEN TRIM(data) ~ '^\d{2}/\d{2}/\d{4}$'
            THEN TO_DATE(TRIM(data), 'DD/MM/YYYY')
            ELSE CURRENT_DATE
        END,
        TRIM(registro_ans),
        TRIM(codigo_conta_contabil),
        TRIM(descricao_conta),
        -- Converte valores (substitui vírgula por ponto)
        CAST(REPLACE(COALESCE(NULLIF(TRIM(valor_saldo_inicial), ''), '0'), ',', '.') AS NUMERIC(15, 2)),
        CAST(REPLACE(COALESCE(NULLIF(TRIM(valor_saldo_final), ''), '0'), ',', '.') AS NUMERIC(15, 2)),
        trimestre,
        ano
    FROM temp_dados_contabeis
    WHERE
        registro_ans IS NOT NULL
        AND TRIM(registro_ans) != ''
        AND EXISTS (
            SELECT 1 FROM operadoras o
            WHERE o.registro_ans = TRIM(temp_dados_contabeis.registro_ans)
        );

    -- Conta registros inseridos
    GET DIAGNOSTICS contagem_inseridos = ROW_COUNT;

    RAISE NOTICE 'Arquivo: %, Lidas: %, Inseridas: %', caminho_arquivo, contagem_linhas, contagem_inseridos;

    RETURN contagem_inseridos;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Importação dos arquivos trimestrais
-- Dados dos últimos 2 anos (2024 e 2025)
-- =============================================================================

-- Ano 2024
SELECT importar_dados_trimestrais('C:/IntuitiveX/Tarefa3_BancoDados/data/1T2024.csv', '1T', 2024);
SELECT importar_dados_trimestrais('C:/IntuitiveX/Tarefa3_BancoDados/data/2T2024.csv', '2T', 2024);
SELECT importar_dados_trimestrais('C:/IntuitiveX/Tarefa3_BancoDados/data/3T2024.csv', '3T', 2024);
SELECT importar_dados_trimestrais('C:/IntuitiveX/Tarefa3_BancoDados/data/4T2024.csv', '4T', 2024);

-- Ano 2025
SELECT importar_dados_trimestrais('C:/IntuitiveX/Tarefa3_BancoDados/data/1T2025.csv', '1T', 2025);
SELECT importar_dados_trimestrais('C:/IntuitiveX/Tarefa3_BancoDados/data/2T2025.csv', '2T', 2025);
SELECT importar_dados_trimestrais('C:/IntuitiveX/Tarefa3_BancoDados/data/3T2025.csv', '3T', 2025);

-- =============================================================================
-- Analisa tabelas para otimização
-- =============================================================================
ANALYZE dados_contabeis_trimestral;
ANALYZE plano_contas;

-- =============================================================================
-- Exibe estatísticas
-- =============================================================================
SELECT 'Registros contábeis:' as info, COUNT(*) as total FROM dados_contabeis_trimestral;
SELECT 'Contas no plano:' as info, COUNT(*) as total FROM plano_contas;
SELECT 'Por trimestre/ano:' as info, trimestre, ano, COUNT(*) as total
FROM dados_contabeis_trimestral
GROUP BY trimestre, ano
ORDER BY ano, trimestre;

-- =============================================================================
-- Fim do script
-- =============================================================================
