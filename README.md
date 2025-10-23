# 🛒 E-commerce de Eletrônicos

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)  
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi)  
![Django](https://img.shields.io/badge/Django-5.0%2B-092E20?logo=django)  
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
   - [Instalação do Backend (FastAPI)](#instalação-do-backend-fastapi)  
   - [Instalação do Frontend (Django)](#instalação-do-frontend-django)  
3. [📂 Estrutura do Projeto](#-estrutura-do-projeto)  
4. [🧪 Testes Unitários](#-testes-unitários)  
5. [🚀 Endpoints e Fluxo de Autenticação](#-endpoints-e-fluxo-de-autenticação)  
6. [💻 Interface Web (Frontend Django)](#-interface-web-frontend-django)  
7. [👨‍💻 Contribuidores](#-contribuidores)  
8. [✅ Conclusão](#-conclusão)

</details>

---

## 📌 Descrição

O projeto é uma aplicação completa de **e-commerce de eletrônicos**, com:

- **Backend:** desenvolvido em **FastAPI**, responsável por gerenciar toda a lógica da API, persistência de dados e autenticação.  
- **Frontend:** desenvolvido em **Django**, responsável pela interface web, autenticação visual de usuários e comunicação com a API FastAPI.  
- **Banco de Dados:** PostgreSQL.

O sistema permite:
- 👤 Cadastro e autenticação de **usuários** (com suporte a administradores)  
- 📦 CRUD de **produtos**  
- 🧾 Criação e listagem de **pedidos**  
- 💳 Processamento de **pagamentos**  
- 🌐 Interface web funcional para login, cadastro e navegação  

---

## ⚙️ Instalação e Requisitos

### Pré-requisitos
- Python **3.10+** (recomendado **3.11+**)  
- PostgreSQL **15+**  
- Ambiente virtual configurado (**venv**)
- Git instalado  

### Dependências
As principais bibliotecas utilizadas no projeto são:
- [FastAPI](https://fastapi.tiangolo.com/) → framework da API  
- [Django](https://www.djangoproject.com/) → framework da API  
- [Uvicorn](https://www.uvicorn.org/) → servidor ASGI  
- [SQLAlchemy](https://www.sqlalchemy.org/) → ORM para PostgreSQL  
- [psycopg2-binary](https://www.psycopg.org/) → driver PostgreSQL  
- [pytest](https://docs.pytest.org/) → testes unitários  

### Instalação

## Configurando um ambiente virtual do Python

Primeiramente, é importante clonar o repositório e criar uma venv:

```bash
git clone https://github.com/C14-2025/EcommerceEletronicos.git
cd EcommerceEletronicos/

# Crie e ative o ambiente virtual (Windows)
python -m venv venv
venv\Scripts\activate

# Ou no Linux/Mac
python -m venv venv
source venv/bin/activate
```

## Instalação do Backend
Instale as dependências do backend:

```bash
# Instale as dependências
pip install -r backend/requirements.txt
```
## Instalação do frontend
Clone o repositório e instale as dependências:

```bash
# Instale as dependências
pip install -r frontend/requirements.txt
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
│── frontend/
│   ├── ecommerce/        # Configuração do Django
│   ├── static/           # Imagens, botões e configurações de estilo do site
│   ├── store/            # App da loja (onde vai ficar os produtos, carrinho, pedidos, etc.)
│   ├── users/            # App de usuários (Aqui consiste no sistema de cadastro, login e autenticação de usuários)
│   ├── manage.py         # Arquivo para rodar a aplicação Django
│   └── requirements.txt
└── README.md
```

---

## 🚀 Rodando a aplicação

### Backend

Para rodar o backend, basta rodar o seguinte comando:

```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa no Swagger:

👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Frontend

Para rodar o backend, basta rodar o seguinte comando:

```bash
python manage.py runserver 8001
```

*Obs:* Como o **Django** define a porta padrão como 8000 e ela já está sendo usada pelo backend, é necessário rodar a aplicação em outra porta. No nosso caso, escolhemos a porta 8001.

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
✔️ Backend robusto em FastAPI conectado ao PostgreSQL
✔️ Frontend em Django com templates e consumo da API
✔️ Suíte de testes separada para garantir estabilidade
✔️ Pipeline CI/CD com GitHub Actions

💡 Contribuições são bem-vindas! Abra uma **issue** ou envie um **pull request**.
