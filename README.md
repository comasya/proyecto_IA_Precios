#  PriceCheck IA: Comparador de Precios con Gemini AI 

## Descripción

Comparador de Precios IA es una aplicación web desarrollada con Streamlit que utiliza la API de Gemini AI para automatizar la comparación de precios de productos electrónicos
entre Google Shopping y una base de datos interna. La aplicación proporciona análisis detallados y recomendaciones para ayudar a los usuarios a tomar decisiones informadas sobre compras y ventas.

## Funcionalidades Principales

* ** Extracción de Precios de Google Shopping:** Utiliza SerpAPI para obtener los precios de los productos electrónicos buscados en Google Shopping.
* ** Análisis con Gemini AI:** Emplea la API de Gemini AI para analizar las variaciones de precios y generar recomendaciones.
* ** Interfaz de Usuario Intuitiva:** Desarrollada con Streamlit para una experiencia de usuario amigable y eficiente.
* ** Reportes y Visualizaciones:** Presenta los datos de precios y análisis en formatos claros y concisos.

## Tecnologías Utilizadas

* ** Python:** Lenguaje de programación principal.
* ** Streamlit:** Framework para la creación de la interfaz web.
* ** Google Generative AI (Gemini AI):** Para el análisis y generación de recomendaciones.
* ** SerpAPI:** Para la extracción de datos de Google Shopping.
* ** Pandas:** Para el manejo y análisis de datos.

## Requisitos

* Clave de API de Gemini AI.
* Clave de API de SerpAPI.
* Python
* Librerías de Python: `streamlit`, `google-generativeai`, `pandas`, `serpapi`.

## Instalación

1.  Clona el repositorio:

    ```bash
    git clone [https://github.com/sindresorhus/del](https://github.com/sindresorhus/del)
    ```

2.  Instala las dependencias:

    ```bash
    pip install streamlit google-generativeai pandas serpapi
    ```

3.  Configura las claves de API en un archivo `secrets.toml` dentro de la carpeta `.streamlit`:

    ```toml
    API_KEY_GEMINI = "TU_CLAVE_DE_GEMINI"
    SERPAPI_KEY = "TU_CLAVE_DE_SERPAPI"
    ```

4.  Ejecuta la aplicación:

    ```bash
    streamlit run app.py
    ```

## Uso

1.  Ingresa el nombre del artículo a buscar en el campo de texto.
2.  Haz clic en "Buscar Precios" .
3.  Visualiza los precios encontrados y las recomendaciones generadas por Gemini AI .

## Estructura del Proyecto
PriceCheck-IA/
├── .streamlit/
│   └── secrets.toml
├── app.py
├── README.md

## Próximos Pasos

* Optimizar las consultas a la API de Gemini AI para mejorar la precisión y eficiencia.
* ️Implementar funcionalidades adicionales para el análisis de tendencias y la comparación con bases de datos internas.
* Mejorar la interfaz de usuario con visualizaciones más interactivas.
