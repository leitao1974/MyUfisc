
import google.generativeai as genai

def listar_modelos(api_key):

    genai.configure(api_key=api_key)

    modelos = []

    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            modelos.append(m.name.replace("models/", ""))

    return modelos


def gerar_analise_ai(api_key, modelo, local, descricao, regimes):

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(modelo)

    prompt = f'''
    Age como jurista especialista em direito do ambiente.

    LOCAL: {local}

    DESCRIÇÃO DOS FACTOS:
    {descricao}

    REGIMES IDENTIFICADOS:
    {regimes}

    Produz:
    1) enquadramento jurídico
    2) possível infração ambiental
    3) medidas de reposição
    '''

    response = model.generate_content(prompt)

    if hasattr(response, "text"):
        return response.text

    return str(response)
