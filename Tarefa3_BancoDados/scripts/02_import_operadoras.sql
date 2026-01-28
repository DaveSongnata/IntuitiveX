-- =============================================================================
-- Script 02: Importação dos dados das operadoras
-- Compatível com PostgreSQL 10+
-- =============================================================================

-- =============================================================================
-- Popula a tabela UF com os estados brasileiros
-- =============================================================================
INSERT INTO uf (sigla, nome) VALUES
('AC', 'Acre'),
('AL', 'Alagoas'),
('AM', 'Amazonas'),
('AP', 'Amapá'),
('BA', 'Bahia'),
('CE', 'Ceará'),
('DF', 'Distrito Federal'),
('ES', 'Espírito Santo'),
('GO', 'Goiás'),
('MA', 'Maranhão'),
('MG', 'Minas Gerais'),
('MS', 'Mato Grosso do Sul'),
('MT', 'Mato Grosso'),
('PA', 'Pará'),
('PB', 'Paraíba'),
('PE', 'Pernambuco'),
('PI', 'Piauí'),
('PR', 'Paraná'),
('RJ', 'Rio de Janeiro'),
('RN', 'Rio Grande do Norte'),
('RO', 'Rondônia'),
('RR', 'Roraima'),
('RS', 'Rio Grande do Sul'),
('SC', 'Santa Catarina'),
('SE', 'Sergipe'),
('SP', 'São Paulo'),
('TO', 'Tocantins')
ON CONFLICT (sigla) DO NOTHING;

-- =============================================================================
-- Popula regiões de comercialização
-- =============================================================================
INSERT INTO regioes_comercializacao (codigo, descricao) VALUES
('1', 'Região 1'),
('2', 'Região 2'),
('3', 'Região 3'),
('4', 'Região 4'),
('5', 'Região 5'),
('6', 'Região 6')
ON CONFLICT (codigo) DO NOTHING;

-- =============================================================================
-- Cria tabela temporária para importação
-- =============================================================================
CREATE TEMPORARY TABLE temp_operadoras (
    registro_ans VARCHAR(10),
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(4),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    regiao_comercializacao VARCHAR(10),
    data_registro_ans VARCHAR(20)
);

-- =============================================================================
-- Importa dados do CSV
-- =============================================================================
COPY temp_operadoras
FROM 'C:/IntuitiveX/Tarefa3_BancoDados/data/dados_cadastrais_op.csv'
WITH (
    FORMAT csv,
    DELIMITER ';',
    HEADER true,
    QUOTE '"',
    ENCODING 'UTF8'
);

-- =============================================================================
-- Limpa e insere dados na tabela principal
-- =============================================================================
INSERT INTO operadoras (
    registro_ans, cnpj, razao_social, nome_fantasia, modalidade,
    logradouro, numero, complemento, bairro, cidade, uf, cep,
    ddd, telefone, fax, endereco_eletronico, representante,
    cargo_representante, regiao_comercializacao, data_registro_ans
)
SELECT
    TRIM(BOTH '"' FROM registro_ans),
    -- Remove caracteres não numéricos do CNPJ
    REGEXP_REPLACE(TRIM(BOTH '"' FROM cnpj), '[^0-9]', '', 'g'),
    TRIM(BOTH '"' FROM razao_social),
    CASE WHEN TRIM(nome_fantasia) IN ('', '""') THEN NULL
         ELSE TRIM(BOTH '"' FROM nome_fantasia) END,
    TRIM(BOTH '"' FROM modalidade),
    TRIM(BOTH '"' FROM logradouro),
    TRIM(BOTH '"' FROM numero),
    CASE WHEN TRIM(complemento) IN ('', '""') THEN NULL
         ELSE TRIM(BOTH '"' FROM complemento) END,
    CASE WHEN TRIM(bairro) IN ('', '""') THEN NULL
         ELSE TRIM(BOTH '"' FROM bairro) END,
    TRIM(BOTH '"' FROM cidade),
    TRIM(BOTH '"' FROM uf),
    -- Remove caracteres não numéricos do CEP
    REGEXP_REPLACE(TRIM(BOTH '"' FROM cep), '[^0-9]', '', 'g'),
    CASE WHEN TRIM(ddd) IN ('', '""') THEN NULL
         ELSE TRIM(BOTH '"' FROM ddd) END,
    CASE WHEN TRIM(telefone) IN ('', '""') THEN NULL
         ELSE TRIM(BOTH '"' FROM telefone) END,
    CASE WHEN TRIM(fax) IN ('', '""') THEN NULL
         ELSE TRIM(BOTH '"' FROM fax) END,
    CASE WHEN TRIM(endereco_eletronico) IN ('', '""') THEN NULL
         ELSE TRIM(BOTH '"' FROM endereco_eletronico) END,
    CASE WHEN TRIM(representante) IN ('', '""') THEN NULL
         ELSE TRIM(BOTH '"' FROM representante) END,
    CASE WHEN TRIM(cargo_representante) IN ('', '""') THEN NULL
         ELSE TRIM(BOTH '"' FROM cargo_representante) END,
    CASE WHEN TRIM(regiao_comercializacao) IN ('', '""') THEN NULL
         ELSE TRIM(BOTH '"' FROM regiao_comercializacao) END,
    -- Converte data
    CASE
        WHEN TRIM(BOTH '"' FROM data_registro_ans) ~ '^\d{4}-\d{2}-\d{2}$'
        THEN TO_DATE(TRIM(BOTH '"' FROM data_registro_ans), 'YYYY-MM-DD')
        WHEN TRIM(BOTH '"' FROM data_registro_ans) ~ '^\d{2}/\d{2}/\d{4}$'
        THEN TO_DATE(TRIM(BOTH '"' FROM data_registro_ans), 'DD/MM/YYYY')
        ELSE NULL
    END
FROM temp_operadoras
WHERE registro_ans IS NOT NULL AND TRIM(registro_ans) != '';

-- =============================================================================
-- Limpa tabela temporária
-- =============================================================================
DROP TABLE temp_operadoras;

-- =============================================================================
-- Analisa tabelas para otimização
-- =============================================================================
ANALYZE operadoras;
ANALYZE modalidades;
ANALYZE uf;
ANALYZE regioes_comercializacao;

-- =============================================================================
-- Exibe estatísticas
-- =============================================================================
SELECT 'Operadoras importadas:' as info, COUNT(*) as total FROM operadoras;
SELECT 'Modalidades:' as info, COUNT(*) as total FROM modalidades;

-- =============================================================================
-- Fim do script
-- =============================================================================
