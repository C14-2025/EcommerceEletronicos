# 🛒 E-commerce de Eletrônicos

## Table of Contents

<details>

   <summary>Contents</summary>

1. [📌 Descrição](#-descrio)
1. [⚙️ Instalação e Requisitos](#-instalao-e-requisitos)
   1. [Pré-requisitos](#pr-requisitos)
   1. [Dependências](#dependncias)
   1. [Instalação](#instalao)
1. [🧪 Testes Unitários](#-testes-unitrios)
   1. [Estrutura da suíte](#estrutura-da-sute)
   1. [Execução dos testes](#execuo-dos-testes)
1. [✅ Conclusão](#-concluso)

</details>

## 📌 Descrição
API desenvolvida em **Python + FastAPI** com integração ao **PostgreSQL** para gerenciamento de um sistema de e-commerce de eletrônicos.  
Permite cadastro de usuários, produtos, pedidos e pagamentos de forma simples e objetiva.

---

## ⚙️ Instalação e Requisitos

### Pré-requisitos
- Python 3.10+ (recomendado 3.11 ou superior)
- PostgreSQL 15+
- Ambiente virtual configurado (venv)

### Dependências
As principais bibliotecas utilizadas no projeto são:
- **FastAPI** → criação da API.
- **Uvicorn** → servidor ASGI.
- **psycopg2-binary** → conexão com PostgreSQL.
- **pytest** → execução dos testes unitários.

### Instalação
Clone o repositório e instale as dependências:

```bash
git clone https://github.com/C14-2025/EcommerceEletronicos.git
cd EcommerceEletronicos/ecommerce

# Crie e ative o ambiente virtual (Windows)
python -m venv venv
venv\Scripts\activate

# Ou no Linux/Mac
python -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r backend/requirements.txt
```

Arquivo `requirements.txt` sugerido:

```
fastapi
uvicorn
psycopg2-binary
pytest
```

---

## 🧪 Testes Unitários

### Estrutura da suíte
Foi criada uma suíte de **testes unitários** usando **pytest**, cobrindo os principais módulos:  

- ✅ **Rotas básicas** (`/`, `/usuarios/`, `/produtos/`)  
- ✅ **Status da API** (200 OK nas rotas)  
- ✅ **Validação de retorno esperado** (JSON correto)  

### Execução dos testes
Para rodar os testes, ative o ambiente virtual e utilize:

```bash
pytest backend/tests -v
```

Exemplo de saída esperada:

```
collected 3 items

tests/test_api.py::test_root PASSED
tests/test_api.py::test_listar_usuarios PASSED
tests/test_api.py::test_listar_produtos PASSED

====================== 3 passed in 0.58s ======================
```

---

## ✅ Conclusão
A aplicação:
- Fornece endpoints para usuários, produtos, pedidos e pagamentos.  
- Garante integração com PostgreSQL.  
- Está coberta por testes unitários básicos para garantir estabilidade.  

---
