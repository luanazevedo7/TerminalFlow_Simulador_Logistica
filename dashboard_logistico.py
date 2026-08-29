import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Simulação Logística", layout="wide")
st.title("🚛 Dashboard: Análise de Gargalos no Terminal")
st.markdown("Visualização dos dados gerados pelo modelo de simulação no SimPy.")

try:
    df = pd.read_csv('resultado_gargalo_balanca.csv')
    
    # ==========================================
    # A MÁGICA DA TRANSFORMAÇÃO DE DADOS AQUI
    # ==========================================
    # 1. Definimos a hora que o turno começa (ex: 08:00 da manhã de hoje)
    hora_inicio_turno = pd.to_datetime('08:00:00')
    
    # 2. Somamos os minutos corridos da simulação a essa hora de início
    df['Hora_Exata_Chegada'] = hora_inicio_turno + pd.to_timedelta(df['Momento_Chegada'], unit='m')
    df['Hora_Exata_Saida'] = hora_inicio_turno + pd.to_timedelta(df['Momento_Saida'], unit='m')
    
    # 3. Formatamos para ficar bonito de ler (Apenas Hora:Minuto)
    df['Chegada_Formatada'] = df['Hora_Exata_Chegada'].dt.strftime('%H:%M')
    df['Saida_Formatada'] = df['Hora_Exata_Saida'].dt.strftime('%H:%M')
    
    # ==========================================

    col1, col2, col3 = st.columns(3)
    
    total_veiculos = len(df)
    tempo_medio_fila = df['Tempo_Fila_min'].mean()
    tempo_maximo_fila = df['Tempo_Fila_min'].max()
    
    col1.metric("Total de Caminhões Atendidos", total_veiculos)
    col2.metric("Tempo Médio na Fila (min)", f"{tempo_medio_fila:.1f}")
    col3.metric("Fila Máxima Registrada (min)", f"{tempo_maximo_fila:.1f}")
    
    st.divider() 
    
    st.subheader("Evolução da Fila ao Longo do Tempo")
    
    # Atualizamos o gráfico para usar a nossa nova coluna formatada no eixo X
    fig = px.bar(
        df, 
        x='Chegada_Formatada', # Agora o eixo X mostra horários como 08:15, 09:30
        y='Tempo_Fila_min',
        hover_data=['Veiculo', 'Tempo_Atendimento_min'],
        labels={'Chegada_Formatada': 'Horário de Chegada', 'Tempo_Fila_min': 'Tempo de Espera na Fila (min)'},
        color='Tempo_Fila_min',
        color_continuous_scale='Reds' 
    )
    
    # Ajuste para as barras não ficarem espremidas e manter a ordem cronológica
    fig.update_xaxes(type='category', tickmode='linear', dtick=10) 
    
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("Ver Base de Dados Bruta"):
        # Mostramos as colunas novas que são mais fáceis de ler
        st.dataframe(df[['Veiculo', 'Chegada_Formatada', 'Tempo_Fila_min', 'Tempo_Atendimento_min', 'Saida_Formatada']])

except FileNotFoundError:
    st.error("O arquivo 'resultado_gargalo_balanca.csv' não foi encontrado. Rode o seu script de simulação primeiro!")