import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Configuração da página Streamlit
st.set_page_config(
    page_title="Dashboard IoT - Monitoramento de Temperatura",
    page_icon="🌡️",
    layout="wide"
)

# Conexão com o PostgreSQL no Docker
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/iot_db"

@st.cache_data(ttl=60)
def load_data(view_name):
    engine = create_engine(DATABASE_URL)
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)

# Título do Dashboard
st.title("🌡️ Dashboard de Monitoramento IoT & Big Data")
st.markdown("Pipeline de dados processado com **Python, Docker, PostgreSQL, SQLAlchemy e Streamlit**.")
st.divider()

try:
    # Carregando os dados das views SQL
    df_avg_temp = load_data('avg_temp_por_dispositivo')
    df_leituras_hora = load_data('leituras_por_hora')
    df_temp_max_min = load_data('temp_max_min_por_dia')

    # Métricas Principais (KPIs) no topo
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Dispositivos", len(df_avg_temp))
    with col2:
        st.metric("Horas Analisadas", len(df_leituras_hora))
    with col3:
        st.metric("Dias Registrados", len(df_temp_max_min))

    st.divider()

    # Gráfico 1: Média de temperatura por dispositivo
    st.header("1. Média de Temperatura por Dispositivo")
    fig1 = px.bar(
        df_avg_temp, 
        x='device_id', 
        y='avg_temp',
        color='location',
        title="Temperatura Média por Dispositivo e Local (Interno / Externo)",
        labels={'device_id': 'ID do Dispositivo', 'avg_temp': 'Temp. Média (°C)', 'location': 'Local'},
        text_auto=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Gráficos 2 e 3 lado a lado
    col_left, col_right = st.columns(2)

    with col_left:
        st.header("2. Volume de Leituras por Hora")
        fig2 = px.line(
            df_leituras_hora, 
            x='hora', 
            y='contagem',
            markers=True,
            title="Distribuição das Leituras IoT ao Longo do Dia",
            labels={'hora': 'Hora do Dia (0-23h)', 'contagem': 'Qtd de Leituras'}
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_right:
        st.header("3. Variação Térmica Diária")
        fig3 = px.line(
            df_temp_max_min, 
            x='data', 
            y=['temp_max', 'temp_min', 'temp_media'],
            title="Evolução das Temperaturas Mínimas, Máximas e Médias",
            labels={'data': 'Data', 'value': 'Temperatura (°C)', 'variable': 'Métrica'}
        )
        st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados do PostgreSQL: {e}")