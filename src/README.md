# 🌡️ Pipeline de Dados IoT & Monitoramento de Temperatura

Projeto acadêmico desenvolvido para a disciplina/faculdade, implementando um pipeline de engenharia de dados de ponta a ponta utilizando dados reais de sensores IoT do Kaggle, armazenamento em banco de dados relacional conteinerizado e visualização interativa.

---

## 🚀 Tecnologias Utilizadas
- **Python** (Pandas, SQLAlchemy)
- **Docker & PostgreSQL** (Armazenamento e modelagem relacional)
- **Streamlit & Plotly** (Dashboard interativo de Business Intelligence)

---

## 📁 Estrutura do Repositório
```text
IOT_data_pipeline/
│
├── data/
│   └── IOT-temp.csv         # Dataset original baixado do Kaggle
├── docs/                    # Relatório teórico em PDF (Entregável)
├── sql/
│   └── views.sql            # Scripts de criação das 3 views analíticas
├── src/
│   ├── etl.py               # Script de extração, tratamento e carga (ETL)
│   └── dashboard.py         # Aplicação web em Streamlit
├── requirements.txt         # Dependências do projeto Python
└── README.md                # Documentação do projeto