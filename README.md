# Projeto ETL & Visualização — Spotify Playlists
Este é um projeto prático de ETL (Extração, Transformação e Carga) com foco nos dados musicais do Spotify. Utiliza o Spotify Tracks Dataset do Kaggle e a Spotify Web API para enriquecer dados de faixas com informações.

## Visão Geral

Objetivo: Extrair playlists e faixas do dataset com os audio features, enriquecer com os dados da API de álbuns, transformar os dados e carregá-los numa base de dados relacional.

**Dados:** Spotify Tracks Dataset + API pública do Spotify.

### Fases:

Extração (Semana 1)

Transformação (Semana 2)

Carga (Semana 3)

Visualização (Semana 4 - em progresso/futuramente)

Tecnologias utilizadas: Python, pandas, Spotipy, SQL Server Management Studio, Prefect.

### Arquitetura do Projeto

**Pipeline ETL:**

Leitura do csv estático com os audio features.

Enriquecimento de faixas via Spotify Web API.

Transformação e limpeza dos dados (normalização, merge, limpeza dos valores).

Carga final na base de dados relacional (SQL Server).

**Esquema da Base de Dados:**

Tabela staging: merged_left_raw

Tabelas normalizadas: artists, albums, tracks

### Como executar

**Pré-requisitos:**

Python 3.x + pip

Conta de desenvolvedor Spotify (Client ID / Client Secret)

Conta no Amazon S3 (aws_access_key_id / aws_secret_access_key / region_name)

SQL Server Management Studio

**Etapas:**

Clonar este repositório:

git clone <URL_DO_REPOSITORIO>

Instalar dependências:

pip install -r requirements.txt

Criar arquivo .env com as credenciais da API:

SPOTIPY_CLIENT_ID=SEU_ID
SPOTIPY_CLIENT_SECRET=SEU_SECRET

Configurar a conexão com SQL Server no script load.py (via pyodbc ou string de conexão).

📁 Estrutura do Repositório

├── data/
│ ├── mpd_slice_0_999.json
│ ├── merged_left.csv
│ └── enriched_data.csv (opcional)
│
├── scripts/
│ ├── extract.py
│ ├── transform.py
│ ├── load.py
│
├── airflow/ (opcional)
│ └── spotify_pipeline_dag.py
│
├── notebooks/
│ └── análise_exploratória.ipynb
│
├── app_dashboard/ (futuramente)
│ └── app.py
│
└── README.md

🧠 Possíveis extensões

Adicionar audio features (danceability, energy, etc) via API Spotify.

Criar um dashboard interativo com Dash, Tableau ou Metabase.

Agendar o pipeline com Apache Airflow.

📜 Licença

Este projeto é apenas para fins educacionais. Dados do Spotify usados sob os termos do Spotify Developer Policy.
