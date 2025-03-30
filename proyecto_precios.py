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
        f"""Analiza los siguientes precios del artículo '{articulo}' encontrados en Google Shopping: {precios_str}.
        Considera las variaciones de precio y la información disponible para determinar un rango de precio óptimo para este producto.
        Proporciona tu respuesta en el siguiente formato, indicando el rango de precio optimo, y luego un breve análisis.
        Rango de precio optimo:
        Analisis:
        """
    )

def obtener_respuesta_gemini(prompt):
    """Obtiene una respuesta de la API de Gemini."""
    try:
        model = genai.GenerativeModel('gemini-pro')
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