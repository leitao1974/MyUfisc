import streamlit as st
import json
from pathlib import Path
import openai
from io import BytesIO
from pdfminer.high_level import extract_text

st.set_page_config(page_title="Análise Jurídica AI", layout="centered")

st.title("Análise Jurídica Fundamentada")
st.write("Faça upload de um documento legal (TXT ou PDF) e gere uma análise jurídica fundamentada usando IA.")

# Inserir a chave API da OpenAI dinamicamente
openai_api_key = st.text_input("Chave API OpenAI", type="password")

# Upload do arquivo
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

if file_text:
    st.subheader("Conteúdo do Documento")
    st.text_area("", file_text, height=200)

    if openai_api_key and st.button("Gerar Análise Jurídica"):
        with st.spinner('Gerando análise jurídica...'):
            prompt = f"Você é um assistente jurídico especializado. Analise o seguinte documento legal e gere uma análise jurídica fundamentada:\n\n1. Resuma o conteúdo principal, destacando obrigações, direitos e cláusulas críticas.\n2. Identifique referências explícitas à legislação (leis, decretos, regulamentos, códigos).\n3. Explique como cada referência legal se aplica ao contexto do documento.\n4. Destaque possíveis lacunas ou riscos jurídicos.\n5. Apresente a análise de forma clara, em tópicos, citando artigos ou normas relevantes.\n6. Sempre que possível, inclua links ou referências oficiais às normas.\n7. Não gere parecer jurídico definitivo, apenas análise interpretativa baseada na legislação.\n\nDocumento:\n{file_text}"
            try:
                openai.api_key = openai_api_key
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=2000
                )
                analysis = response.choices[0].message.content
                st.subheader("Análise Jurídica Fundamentada")
                st.text_area("", analysis, height=400)
            except Exception as e:
                st.error(f"Erro ao gerar análise: {str(e)}")
