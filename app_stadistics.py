import plotly.graph_objects as go
import streamlit as st

def app():
    st.header("Estadísticas generales")

    from utils import (
        cargar_datos_restos,
        cargar_datos_servicios,
        calcular_totales_restos,
        contar_servicios_por_tipo_distrito,
        grafico_barras_totales,
        grafico_barras_servicios
    )


    # URLs de datos
    DATA = st.secrets["data_1_url"]
    DATA_2= st.secrets["data_2_url"]

    # Cargar datos
    gr_locations = cargar_datos_restos(DATA)
    servicios_drogas = cargar_datos_servicios(DATA_2)

    # Revisar si el rango de fechas está definido
    if 'rango_fechas' in st.session_state:
        inicio, fin = st.session_state['rango_fechas']
        gr_locations = gr_locations[(gr_locations['Mes'] >= inicio) & (gr_locations['Mes'] <= fin)]
        # Mostrar el rango de fechas seleccionado
        st.subheader(f"Rango de fechas seleccionado: {inicio.date()} a {fin.date()}")
    else:
        st.warning("No se ha seleccionado un rango de fechas. Mostrando datos completos.")


    #Estadisticos
    total_por_tipo, total_por_barrio, total_por_distrito = calcular_totales_restos(gr_locations)
    servicios_por_tipo_distrito = contar_servicios_por_tipo_distrito(servicios_drogas)

    #Graficos
    fig_tipo = grafico_barras_totales(total_por_tipo,'Restos de consumo por tipo de resto','Tipo','Cantidad')
    fig_barrio = grafico_barras_totales(total_por_barrio, 'Restos de consumo por barrio', 'Barrio', 'Cantidad')
    fig_distrito= grafico_barras_totales(total_por_distrito, 'Restos de consumo por distrito','Distrito', 'Tipo')
    fig_servicios= grafico_barras_servicios(servicios_por_tipo_distrito, 'Distribución de servicios por distrito y tipo de servicio')


    #Muestra los gráficos en Streamlit



    st.subheader('Cantidad de restos de consumo por tipo de resto')
    st.plotly_chart(fig_tipo,use_container_width=True )

    st.subheader('Cantidad de restos de consumo por barrio')
    st.plotly_chart(fig_barrio,use_container_width=True )

    st.subheader('Cantidad de restos de consumo por distrito')
    st.plotly_chart(fig_distrito,use_container_width=True )

    st.subheader('Servicios disponibles por distrito')
    st.plotly_chart(fig_servicios,use_container_width=True )
