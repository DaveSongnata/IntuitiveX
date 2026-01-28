-- =============================================================================
-- Script 05: Queries Analíticas
-- Compatível com PostgreSQL 10+
--
-- Responde às perguntas:
-- 1. Top 10 operadoras com maiores despesas em "EVENTOS/SINISTROS CONHECIDOS
--    OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre
-- 2. Top 10 operadoras com maiores despesas nessa categoria no último ano
-- =============================================================================

-- =============================================================================
-- QUERY 1: Top 10 operadoras - ÚLTIMO TRIMESTRE
-- =============================================================================

WITH ultimo_trimestre AS (
    -- Identifica o último trimestre disponível nos dados
    SELECT
        ano,
        trimestre
    FROM
        dados_contabeis_trimestral
    ORDER BY
        ano DESC,
        CASE
            WHEN trimestre = '4T' THEN 4
            WHEN trimestre = '3T' THEN 3
            WHEN trimestre = '2T' THEN 2
            WHEN trimestre = '1T' THEN 1
            ELSE 0
        END DESC
    LIMIT 1
)
SELECT
    o.registro_ans,
    o.razao_social,
    o.modalidade,
    ut.ano,
    ut.trimestre,
    -- Converte para valores positivos (despesas geralmente têm saldo negativo)
    ABS(SUM(d.valor_saldo_final)) as total_despesas_eventos
FROM
    dados_contabeis_trimestral d
JOIN
    operadoras o ON d.registro_ans = o.registro_ans
JOIN
    ultimo_trimestre ut ON d.ano = ut.ano AND d.trimestre = ut.trimestre
WHERE
    -- Busca pela descrição da conta de eventos/sinistros médico-hospitalares
    UPPER(d.descricao_conta) LIKE UPPER('%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS%MEDICO HOSPITALAR%')
GROUP BY
    o.registro_ans, o.razao_social, o.modalidade, ut.ano, ut.trimestre
ORDER BY
    total_despesas_eventos DESC
LIMIT 10;

-- =============================================================================
-- QUERY 2: Top 10 operadoras - ÚLTIMO ANO
-- =============================================================================

WITH ultimo_ano AS (
    -- Identifica o último ano disponível nos dados
    SELECT
        MAX(ano) as ano
    FROM
        dados_contabeis_trimestral
)
SELECT
    o.registro_ans,
    o.razao_social,
    o.modalidade,
    ua.ano,
    -- Converte para valores positivos (despesas geralmente têm saldo negativo)
    ABS(SUM(d.valor_saldo_final)) as total_despesas_eventos_anual
FROM
    dados_contabeis_trimestral d
JOIN
    operadoras o ON d.registro_ans = o.registro_ans
JOIN
    ultimo_ano ua ON d.ano = ua.ano
WHERE
    -- Busca pela descrição da conta de eventos/sinistros médico-hospitalares
    UPPER(d.descricao_conta) LIKE UPPER('%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS%MEDICO HOSPITALAR%')
GROUP BY
    o.registro_ans, o.razao_social, o.modalidade, ua.ano
ORDER BY
    total_despesas_eventos_anual DESC
LIMIT 10;

-- =============================================================================
-- QUERY ALTERNATIVA (caso a descrição exata seja diferente)
-- Busca mais flexível para encontrar a conta correta
-- =============================================================================

-- Primeiro, vamos ver quais descrições de conta existem relacionadas a eventos/sinistros:
/*
SELECT DISTINCT descricao_conta
FROM dados_contabeis_trimestral
WHERE UPPER(descricao_conta) LIKE '%EVENTO%'
   OR UPPER(descricao_conta) LIKE '%SINISTRO%'
ORDER BY descricao_conta;
*/

-- =============================================================================
-- Fim do script
-- =============================================================================
