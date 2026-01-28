-- =============================================================================
-- Script 03: Criação das tabelas para dados contábeis trimestrais
-- Compatível com PostgreSQL 10+
--
-- IMPORTANTE: Execute este script APÓS os scripts 01 e 02
-- =============================================================================

-- =============================================================================
-- Verifica se a tabela operadoras existe
-- =============================================================================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'operadoras') THEN
        RAISE EXCEPTION 'A tabela operadoras não existe. Execute primeiro os scripts 01 e 02.';
    END IF;
END
$$;

-- =============================================================================
-- Remove tabelas se existirem
-- =============================================================================
DROP TABLE IF EXISTS dados_contabeis_trimestral CASCADE;
DROP TABLE IF EXISTS plano_contas CASCADE;

-- =============================================================================
-- Tabela: plano_contas (Estrutura hierárquica de contas)
-- =============================================================================
CREATE TABLE plano_contas (
    codigo_conta_contabil VARCHAR(20) PRIMARY KEY,
    descricao_conta VARCHAR(255) NOT NULL,
    conta_pai VARCHAR(20),
    nivel INTEGER NOT NULL DEFAULT 1,
    tipo_conta VARCHAR(50),

    CONSTRAINT fk_conta_pai FOREIGN KEY (conta_pai)
        REFERENCES plano_contas (codigo_conta_contabil) ON DELETE CASCADE
);

CREATE INDEX idx_plano_contas_pai ON plano_contas(conta_pai);

COMMENT ON TABLE plano_contas IS 'Estrutura hierárquica do plano de contas';
COMMENT ON COLUMN plano_contas.codigo_conta_contabil IS 'Código da conta - chave primária';
COMMENT ON COLUMN plano_contas.conta_pai IS 'Referência à conta pai para hierarquia';
COMMENT ON COLUMN plano_contas.nivel IS 'Nível na hierarquia (1=raiz, 2=primeiro nível, etc.)';
COMMENT ON COLUMN plano_contas.tipo_conta IS 'Tipo: Ativo, Passivo, Patrimônio Líquido, Receita, Despesa';

-- =============================================================================
-- Tabela: dados_contabeis_trimestral
-- =============================================================================
CREATE TABLE dados_contabeis_trimestral (
    id SERIAL PRIMARY KEY,
    data_referencia DATE NOT NULL,
    registro_ans VARCHAR(10) NOT NULL,
    codigo_conta_contabil VARCHAR(20) NOT NULL,
    descricao_conta VARCHAR(255) NOT NULL,
    valor_saldo_inicial NUMERIC(15, 2) NOT NULL DEFAULT 0,
    valor_saldo_final NUMERIC(15, 2) NOT NULL DEFAULT 0,
    trimestre VARCHAR(10) NOT NULL,
    ano INTEGER NOT NULL,

    -- Referência à tabela operadoras
    CONSTRAINT fk_operadora FOREIGN KEY (registro_ans)
        REFERENCES operadoras (registro_ans) ON DELETE CASCADE
);

-- =============================================================================
-- Índices para otimização de consultas
-- =============================================================================
CREATE INDEX idx_dados_contabeis_registro_ans ON dados_contabeis_trimestral(registro_ans);
CREATE INDEX idx_dados_contabeis_data ON dados_contabeis_trimestral(data_referencia);
CREATE INDEX idx_dados_contabeis_conta ON dados_contabeis_trimestral(codigo_conta_contabil);
CREATE INDEX idx_dados_contabeis_trimestre_ano ON dados_contabeis_trimestral(trimestre, ano);
CREATE INDEX idx_dados_contabeis_descricao ON dados_contabeis_trimestral(descricao_conta);

-- Comentários
COMMENT ON TABLE dados_contabeis_trimestral IS 'Dados contábeis trimestrais das operadoras de saúde';
COMMENT ON COLUMN dados_contabeis_trimestral.registro_ans IS 'Número de registro ANS - FK para operadoras';
COMMENT ON COLUMN dados_contabeis_trimestral.codigo_conta_contabil IS 'Código do plano de contas';
COMMENT ON COLUMN dados_contabeis_trimestral.valor_saldo_inicial IS 'Saldo inicial do período';
COMMENT ON COLUMN dados_contabeis_trimestral.valor_saldo_final IS 'Saldo final do período';
COMMENT ON COLUMN dados_contabeis_trimestral.trimestre IS 'Trimestre (1T, 2T, 3T, 4T)';
COMMENT ON COLUMN dados_contabeis_trimestral.ano IS 'Ano de referência';

-- =============================================================================
-- View: Posição financeira por operadora
-- =============================================================================
CREATE OR REPLACE VIEW posicao_financeira_operadoras AS
SELECT
    o.registro_ans,
    o.razao_social,
    o.modalidade,
    d.trimestre,
    d.ano,
    SUM(CASE WHEN LEFT(d.codigo_conta_contabil, 1) = '1' THEN d.valor_saldo_final ELSE 0 END) as total_ativos,
    SUM(CASE WHEN LEFT(d.codigo_conta_contabil, 1) = '2' THEN d.valor_saldo_final ELSE 0 END) as total_passivos,
    SUM(CASE WHEN LEFT(d.codigo_conta_contabil, 1) = '3' THEN d.valor_saldo_final ELSE 0 END) as patrimonio_liquido
FROM
    dados_contabeis_trimestral d
JOIN
    operadoras o ON d.registro_ans = o.registro_ans
GROUP BY
    o.registro_ans, o.razao_social, o.modalidade, d.trimestre, d.ano;

-- =============================================================================
-- Fim do script
-- =============================================================================
