
import streamlit as st
from database.db import init_db
from services.geo_service import verificar_camadas
from services.legal_engine import avaliar_infracao
from services.report_engine import gerar_relatorio
from services.ai_engine import listar_modelos, gerar_analise_ai

init_db()

st.set_page_config(page_title="Sistema Nacional de Fiscalização Ambiental", layout="wide")

st.title("🛡️ Sistema Nacional de Fiscalização Ambiental")

# ---------------------------
# CONFIGURAÇÃO IA
# ---------------------------

st.sidebar.header("Configuração de IA")

api_key = st.sidebar.text_input("API Key (Google AI / Gemini)", type="password")

modelos = []
modelo_escolhido = None

if api_key:
    try:
        modelos = listar_modelos(api_key)
        if modelos:
            modelo_escolhido = st.sidebar.selectbox("Modelo IA", modelos)
        else:
            st.sidebar.warning("Nenhum modelo encontrado.")
    except Exception as e:
        st.sidebar.error(f"Erro ao listar modelos: {e}")

# ---------------------------
# FORMULÁRIO
# ---------------------------

st.subheader("Identificação da Ocorrência")

local = st.text_input("Local da ocorrência")
lat = st.number_input("Latitude", format="%.6f")
lon = st.number_input("Longitude", format="%.6f")

infrator = st.text_input("Nome do infrator")
descricao = st.text_area("Descrição dos factos observados")

# ---------------------------
# ANÁLISE
# ---------------------------

if st.button("🔎 Analisar Localização"):

    camadas = verificar_camadas(lat, lon)
    regimes = avaliar_infracao(camadas)

    st.subheader("Resultado da análise geográfica")
    st.json(camadas)

    st.subheader("Regimes jurídicos potencialmente aplicáveis")
    st.json(regimes)

    dados = {
        "local": local,
        "lat": lat,
        "lon": lon,
        "descricao": descricao,
        "regimes": regimes
    }

    doc = gerar_relatorio(dados)

    st.download_button(
        "📥 Descarregar Relatório Técnico",
        doc,
        file_name="auto_fiscalizacao_ambiental.docx"
    )

    # ---------------------------
    # ANÁLISE IA
    # ---------------------------

    if api_key and modelo_escolhido:

        st.subheader("Análise jurídica assistida por IA")

        resposta = gerar_analise_ai(
            api_key,
            modelo_escolhido,
            local,
            descricao,
            regimes
        )

        st.write(resposta)
