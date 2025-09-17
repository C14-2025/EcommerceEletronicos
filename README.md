# 🛒 E-commerce de Eletrônicos

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)  
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi)  
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-336791?logo=postgresql)  
![Tests](https://img.shields.io/badge/tests-pytest-green?logo=pytest)

---

## 📑 Sumário

<details>
<summary>Clique para expandir</summary>

1. [📌 Descrição](#-descrição)  
2. [⚙️ Instalação e Requisitos](#-instalação-e-requisitos)  
   - [Pré-requisitos](#pré-requisitos)  
   - [Dependências](#dependências)  
   - [Instalação](#instalação)  
3. [📂 Estrutura do Projeto](#-estrutura-do-projeto)  
4. [🧪 Testes Unitários](#-testes-unitários)  
   - [Estrutura da suíte](#estrutura-da-suíte)  
   - [Execução dos testes](#execução-dos-testes)  
5. [🚀 Endpoints Principais](#-endpoints-principais)  
6. [👨‍💻 Contribuidores](#-contribuidores)  
7. [✅ Conclusão](#-conclusão)

</details>

---

## 📌 Descrição

API desenvolvida em **Python + FastAPI** integrada ao **PostgreSQL** para gerenciamento de um sistema de e-commerce de eletrônicos.  

Funcionalidades principais:  
- 👤 Cadastro e gerenciamento de **usuários**  
- 📦 CRUD de **produtos**  
- 🧾 Criação de **pedidos** com múltiplos itens  
- 💳 Processamento de **pagamentos**  

---

## ⚙️ Instalação e Requisitos

### Pré-requisitos
- Python **3.10+** (recomendado **3.11+**)  
- PostgreSQL **15+**  
- Ambiente virtual configurado (**venv**)

### Dependências
As principais bibliotecas utilizadas no projeto são:
- [FastAPI](https://fastapi.tiangolo.com/) → framework da API  
- [Uvicorn](https://www.uvicorn.org/) → servidor ASGI  
- [SQLAlchemy](https://www.sqlalchemy.org/) → ORM para PostgreSQL  
- [psycopg2-binary](https://www.psycopg.org/) → driver PostgreSQL  
- [pytest](https://docs.pytest.org/) → testes unitários  

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

📄 Exemplo de `requirements.txt`:

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pytest
httpx
```

---

## 📂 Estrutura do Projeto

```
ecommerce/
│── backend/
│   ├── app/
│   │   ├── database/     # Conexão e modelos do banco
│   │   ├── routes/       # Rotas da API (usuários, produtos, pedidos, pagamentos)
│   │   ├── schemas/      # Schemas Pydantic
│   │   └── main.py       # Ponto de entrada da aplicação FastAPI
│   ├── tests/            # Suíte de testes unitários
│   └── requirements.txt
└── README.md
```

---

## 🧪 Testes Unitários

### Estrutura da suíte
A suíte foi construída com **pytest** e cobre os módulos principais:

- ✅ Rotas de **usuários**  
- ✅ Rotas de **produtos**  
- ✅ Rotas de **pedidos**  

### Execução dos testes
Para rodar os testes, utilize:

```bash
pytest backend/tests -v
```

📌 Exemplo de saída:

```
collected 3 items

tests/test_usuario.py::test_criar_usuario PASSED
tests/test_produtos.py::test_criar_produto PASSED
tests/test_pedidos.py::test_criar_pedido PASSED

====================== 3 passed in 0.58s ======================
```

---

## 🚀 Endpoints Principais

Após rodar a aplicação com:

```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa no Swagger:

👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Exemplos de rotas:  
- `POST /usuarios/` → cria usuário  
- `GET /produtos/` → lista produtos  
- `POST /pedidos/` → cria pedido  

---

## 👨‍💻 Contribuidores

| Nome                                   | GitHub |
|----------------------------------------|--------|
| Donatto Pieve Costa Campos             | [DonattoPieve](https://github.com/DonattoPieve) |
| Jessica Guerzoni                       | [jessguerzoni](https://github.com/jessguerzoni) |
| Lucas Cinquetti Moreira                | [cinquetti](https://github.com/cinquetti) |
| Luiz Gustavo Domingues de Carvalho     | [LuizGustavoDCarvalho](https://github.com/LuizGustavoDCarvalho) |

---

## ✅ Conclusão

O projeto:  
✔️ Fornece endpoints completos para usuários, produtos, pedidos e pagamentos  
✔️ Integração robusta com PostgreSQL via SQLAlchemy  
✔️ Suíte de testes unitários para estabilidade da API  
✔️ Estrutura modular, facilitando manutenção e expansão futura  

<<<<<<< HEAD
💡 Contribuições são bem-vindas! Abra uma **issue** ou envie um **pull request**.
=======
💡 Contribuições são bem-vindas! Abra uma **issue** ou envie um **pull request**.
>>>>>>> origin/main
