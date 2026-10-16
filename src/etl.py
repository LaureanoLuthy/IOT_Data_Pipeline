import os
import pandas as pd
from sqlalchemy import create_engine

# Conexão com o PostgreSQL do Docker (banco iot_db)
# Se a senha do seu postgres for diferente de 'postgres', altere abaixo
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/iot_db"

def carregar_e_tratar_dados(caminho_csv):
    print("📥 Lendo arquivo CSV...")
    if not os.path.exists(caminho_csv):
        raise FileNotFoundError(f"Arquivo não encontrado em: {caminho_csv}")

    # Lê o arquivo CSV usando pandas
    df = pd.read_csv(caminho_csv)
    print(f"✅ Arquivo lido com sucesso. Total de linhas originais: {len(df)}")

    # Padronização de nomes de colunas (deixa tudo minúsculo e troca espaços por _)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Renomeando colunas do Kaggle para nomes mais fáceis de usar
    df.rename(columns={
        'id': 'reading_id',
        'room_id/id': 'device_id',
        'noted_date': 'timestamp',
        'out/in': 'location',
        'temp': 'temperature'
    }, inplace=True)

    # Tratamento de tipos de dados (convertendo texto de data para formato data/hora)
    print("🔄 Tratando tipos de dados e datas...")
    df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True, errors='coerce')
    
    # Remove linhas que tenham dados essenciais faltando
    df.dropna(subset=['timestamp', 'temperature', 'device_id'], inplace=True)

    # Cria colunas extras que vão nos ajudar a montar os gráficos por hora e por dia
    df['hora'] = df['timestamp'].dt.hour
    df['data'] = df['timestamp'].dt.date

    print(f"📊 Dados limpos e prontos. Linhas válidas: {len(df)}")
    return df

def inserir_no_banco(df):
    print("🚀 Conectando ao PostgreSQL...")
    engine = create_engine(DATABASE_URL)

    print("💾 Gravando os dados na tabela 'temperature_readings' do banco...")
    df.to_sql(
        name='temperature_readings',
        con=engine,
        if_exists='replace',  # Se a tabela já existir, substitui
        index=False
    )
    print("🎉 Ingestão de dados concluída com sucesso!")

if __name__ == "__main__":
    # Aponta para o arquivo que está na pasta data
    caminho_csv = os.path.join("data", "IOT-temp.csv")
    try:
        dados_tratados = carregar_e_tratar_dados(caminho_csv)
        inserir_no_banco(dados_tratados)
    except Exception as e:
        print(f"❌ Erro durante o processo: {e}")