import streamlit as st
from app_mapa_interactivo import app as m_i_app
from app_stadistics import app as std_app

st.title("Análisis de  Consumo y Servicios de Drogas: Mapa y Estadísticas")

# Autenticación
password = st.text_input("Introduce la contraseña para acceder a los datos:", type="password")
 
if password == st.secrets["access_password"]:
    st.success("¡Contraseña correcta! Cargando datos...")

    # Creación de un selector de páginas
    page = st.sidebar.radio("Selecciona una pestaña", ("Mapa", "Estadisticas"))

    if page == "Mapa":
        m_i_app()
    elif page == "Estadisticas":
        std_app()

else:
    st.warning("Introduce la contraseña para ver el contenido.")
