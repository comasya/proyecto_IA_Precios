"""
Este script de Python utiliza las APIs de Google Gemini y Mercado Libre para comparar precios de productos.
Permite al usuario ingresar un artículo, buscar sus precios en Mercado Libre y obtener un análisis y recomendación de precios utilizando Gemini.

Esta aplicación de Streamlit permite a los usuarios comparar precios de productos en Mercado Libre y obtener un análisis de precios utilizando la API de Google Gemini.
"""
import google.generativeai as genai
import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# Configura la API Key desde una variable de entorno
genai.configure(api_key=st.secrets["API_KEY_GEMINI"])

def obtener_precios_mercado_libre(articulo):
    """Obtiene los nombres y precios de Mercado Libre para un artículo dado."""
    url = f"https://listado.mercadolibre.com.ar/{articulo}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        productos = soup.select("li.ui-search-layout__item")
        resultados = []

        for producto in productos:
            nombre = producto.select_one("h2.ui-search-item__title")
            precio = producto.select_one("span.andes-money-amount__fraction")

            if nombre and precio:
                nombre_texto = nombre.get_text(strip=True)
                precio_texto = precio.get_text(strip=True).replace(".", "")

                try:
                    precio_valor = int(precio_texto)
                    resultados.append({"Nombre": nombre_texto, "Precio": precio_valor})
                except ValueError:
                    continue  # Ignorar si el precio no es numérico

        return sorted(resultados, key=lambda x: x["Precio"])[:10] if resultados else []

    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener precios de Mercado Libre: {e}")
        return []

def main():
    """Aplicación principal en Streamlit."""
    st.title("🔍 Comparador de Precios en Mercado Libre")
    articulo = st.text_input("Ingrese el nombre del artículo a buscar:")

    if st.button("🔎 Buscar Precios"):
        if articulo:
            with st.spinner("Buscando precios..."):
                precios_mercado_libre = obtener_precios_mercado_libre(articulo)
                if precios_mercado_libre:
                    st.subheader("📊 Precios Encontrados")
                    df = pd.DataFrame(precios_mercado_libre)
                    st.table(df[["Nombre", "Precio"]])
                else:
                    st.warning("No se encontraron precios para este artículo.")
        else:
            st.warning("Por favor, ingrese un artículo.")

if __name__ == "__main__":
    main()
