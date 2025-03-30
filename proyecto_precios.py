import streamlit as st
import google.generativeai as genai
import pandas as pd
from serpapi import GoogleSearch
import re

# Configura la API Key de Gemini
genai.configure(api_key=st.secrets["API_KEY_GEMINI"])

# API Key de SerpAPI
SERPAPI_KEY = st.secrets["SERPAPI_KEY"]

def obtener_precios_google(articulo):
    """Obtiene los nombres y precios de productos desde Google Shopping usando SerpAPI."""
    params = {
        "q": articulo,
        "hl": "es",
        "gl": "AR",  # Ajusta según el país (AR = Argentina)
        "tbm": "shop",
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    resultados = search.get_dict()

    productos = []

    if "shopping_results" in resultados:
        for item in resultados["shopping_results"][:10]:  # Top 10
            nombre = item.get("title", "Nombre no disponible")
            precio = item.get("price", "Precio no disponible")
            productos.append({"Nombre": nombre, "Precio": precio})

    return productos

def generar_prompt(articulo, precios):
    """Genera un prompt detallado para la API de Gemini."""
    precios_str = ", ".join([f"{p['Nombre']}: {p['Precio']}" for p in precios])
    return (
        f"""Como comprador interesado en el artículo '{articulo}', necesito tu ayuda para analizar los siguientes precios encontrados en Google Shopping: {precios_str}.
        Considera las variaciones de precio, la información disponible y cualquier otro factor relevante para determinar un rango de precio óptimo y proporcionar recomendaciones útiles.
        Proporciona tu respuesta en el siguiente formato:
        Rango de precio óptimo: [Rango de precio]
        Análisis de precios: [Análisis detallado de las variaciones, tendencias, etc.]
        Recomendaciones para el comprador: [Recomendaciones para tomar una decisión informada]
        """
    )

def obtener_respuesta_gemini(prompt):
    """Obtiene una respuesta de la API de Gemini."""
    try:
        # Lista los modelos disponibles
        available_models = genai.list_models()
        print("Modelos Disponibles:")
        for model_info in available_models:
            print(model_info)

        # Intenta usar el modelo 'gemini-pro' o un modelo disponible alternativo
        model_name = 'gemini-pro'
        if not any(model_info.name == model_name for model_info in available_models):
            # encuentra un modelo alternativo que soporte generate content.
            for model_info in available_models:
                if 'generateContent' in model_info.supported_generation_methods:
                    model_name = model_info.name
                    print (f"using model {model_name}")
                    break
            else:
                st.error("No se encontró ningún modelo compatible.")
                return "No se encontró ningún modelo compatible."

        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text if response else "No se obtuvo respuesta de Gemini."
    except Exception as e:
        st.error(f"Error al obtener respuesta de Gemini: {e}")
        return f"No se pudo obtener respuesta debido a un error: {e}"

def main():
    """Aplicación principal en Streamlit."""
    st.set_page_config(layout="wide")

    with st.sidebar:
        st.title("ℹ️ Sobre la App")
        st.write("Esta aplicación busca productos en Google Shopping y muestra los 10 mejores precios. Además, usa la IA de Gemini para analizar tendencias de precios.")

    st.title(" Comparador de Precios en Google Shopping")
    articulo = st.text_input("Ingrese el nombre del artículo a buscar:")

    if st.button(" Buscar Precios"):
        if articulo:
            with st.spinner("Buscando precios..."):
                precios_google = obtener_precios_google(articulo)
                if precios_google:
                    st.subheader(" Precios Encontrados")
                    df = pd.DataFrame(precios_google)
                    st.table(df)

                    # Generar y obtener respuesta de Gemini
                    prompt = generar_prompt(articulo, precios_google)
                    respuesta = obtener_respuesta_gemini(prompt)

                    st.subheader(" Recomendación de Precios")
                    st.write(respuesta)
                else:
                    st.warning("No se encontraron precios para este artículo.")
        else:
            st.warning("Por favor, ingrese un artículo.")

if __name__ == "__main__":
    main()