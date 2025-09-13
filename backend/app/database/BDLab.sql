DROP TABLE IF EXISTS pedido_itens CASCADE;
DROP TABLE IF EXISTS pagamentos CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS produtos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS enderecos CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
-- ==========================
-- Tabela de Usuários
-- ==========================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,  -- armazenar hash
    telefone VARCHAR(20)
);

-- ==========================
-- Tabela de Endereços
-- ==========================
CREATE TABLE enderecos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    rua VARCHAR(150) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    cep VARCHAR(20) NOT NULL
);

-- ==========================
-- Tabela de Categorias
-- ==========================
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- ==========================
-- Tabela de Produtos
-- ==========================
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    estoque INT NOT NULL
);

-- ==========================
-- Tabela de Pedidos
-- ==========================
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id),
    endereco_id INT REFERENCES enderecos(id),
    data_pedido TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'pendente'
);

-- ==========================
-- Tabela de Itens do Pedido
-- ==========================
CREATE TABLE pedido_itens (
    id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES pedidos(id) ON DELETE CASCADE,
    produto_id INT REFERENCES produtos(id),
    quantidade INT NOT NULL,
    preco_unit DECIMAL(10,2) NOT NULL
);

-- ==========================
-- Tabela de Pagamentos
-- ==========================
CREATE TABLE pagamentos (
    id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES pedidos(id) ON DELETE CASCADE,
    valor DECIMAL(10,2) NOT NULL,
    metodo VARCHAR(50),
    status VARCHAR(50) DEFAULT 'aguardando',
    data_pagamento TIMESTAMP
);
