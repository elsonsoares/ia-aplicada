
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="IA de Compra", layout="centered")

st.title("🧠 Previsor de Compras com IA")
st.write("Insira os dados do cliente e veja se ele provavelmente compraria.")

# Entradas do usuário
idade = st.number_input("Idade", min_value=0, max_value=100, value=30)
renda = st.number_input("Renda (R$)", min_value=0, max_value=20000, value=5000)
tempo_de_casa = st.number_input("Tempo de casa (anos)", min_value=0, max_value=50, value=3)

if st.button("🔍 Prever"):
    dados = {
        "idade": idade,
        "renda": renda,
        "tempo_de_casa": tempo_de_casa
    }

    try:
        resposta = requests.post("http://127.0.0.1:5000/prever", json=dados)
        if resposta.status_code == 200:
            resultado = resposta.json()
            st.success(f"✅ Resultado: {resultado['interpretacao']}")
            st.write("**Explicação:**")
            for passo in resultado['explicacao']:
                st.write(f"- {passo}")
            st.write(f"**Confiança:** {resultado['grupo_final']['confianca']}")
        else:
            st.error(f"Erro: {resposta.json().get('erro', 'Erro desconhecido')}")
    except Exception as e:
        st.error("⚠️ Não foi possível conectar à API.")
        st.text(str(e))

# Painel gráfico de histórico
st.header("📊 Histórico de Predições")

arquivo_historico = 'historico.csv'
if os.path.exists(arquivo_historico):
    historico = pd.read_csv(arquivo_historico)

    st.subheader("Últimas predições")
    st.dataframe(historico.tail(10))

    compradores = historico['resultado'].sum()
    total_predicoes = historico.shape[0]
    taxa_compradores = (compradores / total_predicoes) * 100

    st.subheader("Estatísticas rápidas")
    st.write(f"Total de predições feitas: **{total_predicoes}**")
    st.write(f"Clientes classificados como compradores: **{taxa_compradores:.2f}%**")

    # Gráfico de linha com histórico
    historico['data_hora'] = pd.to_datetime(historico['data_hora'])
    historico['resultado_cumulativo'] = historico['resultado'].cumsum()
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(historico['data_hora'], historico['resultado_cumulativo'], marker='o', linestyle='-', color='b')
    ax.set_xlabel('Data e Hora')
    ax.set_ylabel('Compradores acumulados')
    ax.set_title('Compradores ao longo do tempo')
    ax.grid(True)

    st.pyplot(fig)

else:
    st.warning("Histórico ainda não disponível. Faça algumas predições para gerar dados.")
