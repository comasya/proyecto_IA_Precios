import requests
import streamlit as st
import google.generativeai as genai
import pandas as pd

# Configura la API Key de Gemini
genai.configure(api_key=st.secrets["API_KEY_GEMINI"])

def obtener_precios_mercado_libre(articulo):
    """Obtiene los nombres y precios de los productos en Mercado Libre."""
    url = f"https://api.mercadolibre.com/sites/MLA/search?q={articulo}&limit=10"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        resultados = []
        for item in data.get("results", []):
            nombre = item.get("title")
            precio = item.get("price")
            if nombre and precio:
                resultados.append({"Nombre": nombre, "Precio": precio})
        
        return resultados if resultados else []

    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener precios de Mercado Libre: {e}")
        return []

def generar_prompt(articulo, precios):
    """Genera un prompt para la API de Gemini basado en los precios obtenidos."""
    precios_str = ", ".join([f"{p['Nombre']}: ${p['Precio']}" for p in precios])
    return (
        f"""El artículo '{articulo}' tiene los siguientes precios en Mercado Libre: {precios_str}.
        Proporciona un análisis de estos precios y recomienda un rango óptimo.""" 
    )

def obtener_respuesta_gemini(prompt):
    """Obtiene una respuesta de la API de Gemini."""
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text if response else "No se obtuvo respuesta."
    except Exception as e:
        st.error(f"Error al obtener respuesta de Gemini: {e}")
        return "No se pudo obtener respuesta debido a un error."

def main():
    """Aplicación principal en Streamlit."""
    st.set_page_config(layout="wide")
    
    with st.sidebar:
        st.title("ℹ️ Sobre la App")
        st.write("Esta aplicación busca productos en Mercado Libre y muestra los 10 mejores precios. Además, usa la IA de Gemini para analizar tendencias de precios.")

    st.title("🔍 Comparador de Precios en Mercado Libre")
    articulo = st.text_input("Ingrese el nombre del artículo a buscar:")

    if st.button("🔎 Buscar Precios"):
        if articulo:
            with st.spinner("Buscando precios..."):
                precios_mercado_libre = obtener_precios_mercado_libre(articulo)
                if precios_mercado_libre:
                    st.subheader("📊 Precios Encontrados")
                    df = pd.DataFrame(precios_mercado_libre)
                    st.table(df)

                    # Generar y obtener respuesta de Gemini
                    prompt = generar_prompt(articulo, precios_mercado_libre)
                    respuesta = obtener_respuesta_gemini(prompt)

                    st.subheader("💡 Recomendación de Precios")
                    st.write(respuesta)
                else:
                    st.warning("No se encontraron precios para este artículo.")
        else:
            st.warning("Por favor, ingrese un artículo.")

if __name__ == "__main__":
    main()
