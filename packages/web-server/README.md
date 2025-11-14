# Open Flag — Web Server

Servidor FastAPI para gerenciar feature flags, incluindo criação, edição, remoção, toggle e histórico de uso (timestamps).


## 🚀 Quick Start

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 3. Rodar aplicação
fastapi dev server.py

# 4. Rodar testes
pytest -v
```

O servidor iniciará em: http://localhost:8000


## 📦 Stack
- **Linguagem:** Python 3.10+
- **Framework:** FastAPI
- **Database:** SQLite
- **Testes:** Pytest


## 📁 Estrutura do projeto
```
web-server/
│── server.py        # API FastAPI
│── db.py            # Storage SQLite
│── tests/           # Testes unitários (pytest)
│── requirements.txt
│── README.md
```