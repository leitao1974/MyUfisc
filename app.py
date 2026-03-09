import streamlit as st
import json
from io import BytesIO
from google.oauth2 import service_account
from googleapiclient.discovery import build
from pdfminer.high_level import extract_text

st.set_page_config(page_title="Análise Jurídica Gemini", layout="centered")

st.title("Análise Jurídica Fundamentada com Google Gemini")
st.write("Faça upload de um documento legal (TXT ou PDF) e gere uma análise jurídica usando modelos Gemini disponíveis na sua conta Google.")

# Inserir chave JSON do Service Account dinamicamente
service_account_json = st.text_area("Chave API Google (JSON do Service Account)", height=200)

uploaded_file = st.file_uploader("Upload de Documento (TXT ou PDF)", type=["txt", "pdf"])

file_text = ''
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        try:
            file_bytes = BytesIO(uploaded_file.read())
            file_text = extract_text(file_bytes)
        except Exception as e:
            st.error(f"Erro ao extrair texto do PDF: {str(e)}")
    elif uploaded_file.type == "text/plain":
        file_text = uploaded_file.read().decode("utf-8")
    else:
        st.error("Formato de arquivo não suportado.")

if service_account_json:
    try:
        key_dict = json.loads(service_account_json)
        credentials = service_account.Credentials.from_service_account_info(key_dict)
        client = build('aiplatform', 'v1', credentials=credentials)

        project_id = key_dict.get('project_id')
        location = 'us-central1'  # Pode tornar dinâmico
        parent = f'projects/{project_id}/locations/{location}'

        # Listar modelos Gemini disponíveis
        request = client.projects().locations().models().list(parent=parent)
        response = request.execute()
        models = response.get('models', [])

        if models:
            st.success(f"Foram encontrados {len(models)} modelos.")
            model_names = {model['displayName']: model['name'] for model in models}
            selected_model = st.selectbox("Selecione o modelo Gemini", list(model_names.keys()))
        else:
            st.warning("Nenhum modelo encontrado neste projeto/localização.")
            selected_model = None

    except Exception as e:
        st.error(f"Erro ao autenticar ou listar modelos: {str(e)}")
        selected_model = None

if file_text and service_account_json and selected_model:
    st.subheader("Conteúdo do Documento")
    st.text_area("", file_text, height=200)

    if st.button("Gerar Análise Jurídica"):
        with st.spinner('Gerando análise jurídica...'):
            prompt = f"Você é um assistente jurídico especializado. Analise o seguinte documento legal e gere uma análise jurídica fundamentada:\n\n1. Resuma o conteúdo principal, destacando obrigações, direitos e cláusulas críticas.\n2. Identifique referências explícitas à legislação (leis, decretos, regulamentos, códigos).\n3. Explique como cada referência legal se aplica ao contexto do documento.\n4. Destaque possíveis lacunas ou riscos jurídicos.\n5. Apresente a análise de forma clara, em tópicos, citando artigos ou normas relevantes.\n6. Sempre que possível, inclua links ou referências oficiais às normas.\n7. Não gere parecer jurídico definitivo, apenas análise interpretativa baseada na legislação.\n\nDocumento:\n{file_text}"
            try:
                # Chamada para o modelo Gemini
                request_body = {
                    "instances": [{"content": prompt}],
                    "parameters": {"temperature": 0.2, "maxOutputTokens": 2000}
                }
                model_full_name = model_names[selected_model]
                prediction = client.projects().locations().models().predict(
                    name=model_full_name,
                    body=request_body
                ).execute()

                analysis = prediction['predictions'][0]['content']
                st.subheader("Análise Jurídica Fundamentada")
                st.text_area("", analysis, height=400)
            except Exception as e:
                st.error(f"Erro ao gerar análise: {str(e)}")
