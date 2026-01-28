-- =============================================================================
-- Script 01: Criação das tabelas para dados das operadoras
-- Compatível com PostgreSQL 10+
-- =============================================================================

-- Remove tabelas se existirem (ordem inversa das dependências)
DROP TABLE IF EXISTS operadoras CASCADE;
DROP TABLE IF EXISTS modalidades CASCADE;
DROP TABLE IF EXISTS uf CASCADE;
DROP TABLE IF EXISTS regioes_comercializacao CASCADE;

-- =============================================================================
-- Tabela: uf (Estados brasileiros)
-- =============================================================================
CREATE TABLE uf (
    sigla CHAR(2) PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

COMMENT ON TABLE uf IS 'Estados brasileiros';

-- =============================================================================
-- Tabela: modalidades (Tipos de operadoras)
-- =============================================================================
CREATE TABLE modalidades (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL
);

COMMENT ON TABLE modalidades IS 'Tipos de operadoras de saúde';

-- =============================================================================
-- Tabela: regioes_comercializacao
-- =============================================================================
CREATE TABLE regioes_comercializacao (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    descricao VARCHAR(100)
);

COMMENT ON TABLE regioes_comercializacao IS 'Regiões de comercialização das operadoras';

-- =============================================================================
-- Tabela: operadoras (Principal)
-- =============================================================================
CREATE TABLE operadoras (
    registro_ans VARCHAR(10) PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100) NOT NULL,
    logradouro VARCHAR(255) NOT NULL,
    numero VARCHAR(20),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL,
    cep VARCHAR(8) NOT NULL,
    ddd VARCHAR(4),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    regiao_comercializacao VARCHAR(10),
    data_registro_ans DATE,

    -- Constraints
    CONSTRAINT operadoras_cnpj_ck CHECK (cnpj ~ '^[0-9]{14}$'),
    CONSTRAINT operadoras_cep_ck CHECK (cep ~ '^[0-9]{8}$')
);

-- Comentários da tabela operadoras
COMMENT ON TABLE operadoras IS 'Dados cadastrais das operadoras de saúde da ANS';
COMMENT ON COLUMN operadoras.registro_ans IS 'Número de registro na ANS - chave primária';
COMMENT ON COLUMN operadoras.cnpj IS 'CNPJ da operadora (apenas números)';
COMMENT ON COLUMN operadoras.modalidade IS 'Tipo de operadora (ex: Medicina de Grupo, Cooperativa)';
COMMENT ON COLUMN operadoras.regiao_comercializacao IS 'Código da região de comercialização';
COMMENT ON COLUMN operadoras.data_registro_ans IS 'Data de registro na ANS';

-- =============================================================================
-- Índices para otimização de consultas
-- =============================================================================
CREATE INDEX idx_operadoras_razao_social ON operadoras(razao_social);
CREATE INDEX idx_operadoras_modalidade ON operadoras(modalidade);
CREATE INDEX idx_operadoras_uf ON operadoras(uf);
CREATE INDEX idx_operadoras_cidade ON operadoras(cidade);
CREATE INDEX idx_operadoras_cnpj ON operadoras(cnpj);

-- =============================================================================
-- Trigger para atualizar tabela de modalidades automaticamente
-- =============================================================================
CREATE OR REPLACE FUNCTION update_modalidades()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO modalidades (nome)
    VALUES (NEW.modalidade)
    ON CONFLICT (nome) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trig_update_modalidades
AFTER INSERT OR UPDATE ON operadoras
FOR EACH ROW
EXECUTE FUNCTION update_modalidades();

-- =============================================================================
-- Fim do script
-- =============================================================================
