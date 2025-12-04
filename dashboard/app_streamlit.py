# Dashboard Streamlit para Sistema IoT
# Autor: Erik Gastão
# Sistemas Distribuídos - 2025

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# Configuração da página
st.set_page_config(
    page_title="Dashboard IoT - Sensores",
    page_icon="🌡️",
    layout="wide"
)

# URL da API
API_URL = "http://localhost:8080"

# Função para obter ícone e info do sensor
def get_sensor_info(sensor_id):
    if sensor_id.startswith('T'):
        return {'icon': '🌡️', 'name': 'Temperatura', 'unit': '°C'}
    elif sensor_id.startswith('H'):
        return {'icon': '💧', 'name': 'Umidade', 'unit': '%'}
    elif sensor_id.startswith('L'):
        return {'icon': '💡', 'name': 'Luminosidade', 'unit': 'lux'}
    elif sensor_id.startswith('M'):
        return {'icon': '🚶', 'name': 'Movimento', 'unit': ''}
    return {'icon': '📊', 'name': 'Sensor', 'unit': ''}

# Função para buscar resumo dos sensores
def fetch_summary():
    try:
        response = requests.get(f"{API_URL}/api/sensor/summary")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
        return []

# Função para buscar todas as leituras
def fetch_readings(limit=50):
    try:
        response = requests.get(f"{API_URL}/api/sensor/data?limit={limit}")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Erro ao buscar leituras: {e}")
        return []

# Título do Dashboard
st.title("🌡️ Dashboard de Sensores IoT")
st.markdown("Monitoramento em tempo real dos sensores")

# Botão para atualizar manualmente
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🔄 Atualizar"):
        st.rerun()

st.divider()

# Seção de Resumo - Cards com última leitura
st.header("📊 Últimas Leituras")

summary_data = fetch_summary()

if summary_data:
    # Cria colunas para os cards
    cols = st.columns(len(summary_data))
    
    for idx, sensor in enumerate(summary_data):
        info = get_sensor_info(sensor['sensorId'])
        
        with cols[idx]:
            st.metric(
                label=f"{info['icon']} {info['name']}",
                value=f"{sensor['lastValue']:.2f} {info['unit']}",
                delta=sensor['sensorId']
            )
            st.caption(f"Última atualização: {datetime.fromisoformat(sensor['lastTimestamp'].replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M:%S')}")
else:
    st.warning("Nenhum dado disponível. Verifique se a API está rodando.")

st.divider()

# Seção de Tabela - Todas as leituras
st.header("📋 Todas as Leituras")

# Controle de quantos registros mostrar
num_readings = st.slider("Quantidade de leituras:", 10, 100, 50)

readings_data = fetch_readings(num_readings)

if readings_data:
    # Converte para DataFrame
    df = pd.DataFrame(readings_data)
    
    # Adiciona informações do sensor
    df['Tipo'] = df['sensorId'].apply(lambda x: get_sensor_info(x)['name'])
    df['Ícone'] = df['sensorId'].apply(lambda x: get_sensor_info(x)['icon'])
    df['Unidade'] = df['sensorId'].apply(lambda x: get_sensor_info(x)['unit'])
    
    # Formata o valor com unidade
    df['Valor Formatado'] = df.apply(lambda row: f"{row['value']:.2f} {row['Unidade']}", axis=1)
    
    # Formata timestamp
    df['Data/Hora'] = pd.to_datetime(df['timestamp']).dt.strftime('%d/%m/%Y %H:%M:%S')
    
    # Seleciona e renomeia colunas para exibição
    df_display = df[['id', 'Ícone', 'sensorId', 'Tipo', 'Valor Formatado', 'Data/Hora']]
    df_display.columns = ['ID', '📊', 'Sensor ID', 'Tipo', 'Valor', 'Data/Hora']
    
    # Exibe a tabela
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )
    
    # Estatísticas rápidas
    st.subheader("📈 Estatísticas")
    
    stats_cols = st.columns(4)
    
    with stats_cols[0]:
        st.metric("Total de Leituras", len(df))
    
    with stats_cols[1]:
        st.metric("Sensores Ativos", df['sensorId'].nunique())
    
    with stats_cols[2]:
        avg_value = df['value'].mean()
        st.metric("Valor Médio", f"{avg_value:.2f}")
    
    with stats_cols[3]:
        latest_time = pd.to_datetime(df['timestamp']).max()
        st.metric("Última Leitura", latest_time.strftime('%H:%M:%S'))
    
else:
    st.warning("Nenhuma leitura encontrada.")

# Footer
st.divider()
st.markdown("**Status da API:** Online" if summary_data else "**Status da API:** Offline")
st.caption("Dashboard atualiza automaticamente a cada 5 segundos.")

# Auto-refresh a cada 5 segundos
time.sleep(5)
st.rerun()
