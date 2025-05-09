import plotly.graph_objects as go
import streamlit as st



def app():
    st.header("Mapa de consumo y servicio de drogas en Barcelona")

    from utils import (
        cargar_datos_restos,
        cargar_datos_servicios,
        crear_trazas_consumos,
        crear_trazas_servicios
    )


    # URLs de datos
    DATA = st.secrets["data_1_url"]

    DATA_2= st.secrets["data_2_url"]

    # Cargar datos
    gr_locations = cargar_datos_restos(DATA)
    servicios_drogas = cargar_datos_servicios(DATA_2)


    # Crear Mapa
    fig = go.Figure()

    # Añadir trazas de consumos
    trazas_consumos = crear_trazas_consumos(gr_locations)
    for traza in trazas_consumos:
        fig.add_trace(traza)
    num_capa_consumos = len(trazas_consumos)

    # Añadir trazas de servicios
    trazas_servicios = crear_trazas_servicios(servicios_drogas)
    for traza in trazas_servicios:
        fig.add_trace(traza)
    total_trazas = num_capa_consumos + len(trazas_servicios)



    fig.update_layout(
        updatemenus=[
            #Menu cambiar variables 
            dict(
                buttons=list([
                    dict(label="Mostrar todo",
                        method="update",
                        args=[{"visible": [True]*total_trazas}]),
                    dict(label="Mostrar solo consumos",
                        method="update",
                        args=[{"visible": [True]*num_capa_consumos + [False]*(total_trazas - num_capa_consumos)}]),
                    dict(label="Mostrar solo servicios",
                        method="update",
                        args=[{"visible": [False]*num_capa_consumos + [True]*(total_trazas - num_capa_consumos)}]),
                    
                ]),
                direction="down",
                showactive=True,
                x=0.01,
                xanchor="left",
                y=1.05,
                yanchor="top"
            ),

            # Menú 2: Cambiar estilo de mapa
            dict(
                buttons=[
                    dict(label="Carto Positron",
                        method="relayout",
                        args=[{"map.style": "carto-positron"}]),
                    dict(label="OpenStreetMap",
                        method="relayout",
                        args=[{"map.style": "open-street-map"}])
                ],
                direction="down",
                showactive=True,
                x=0.25,  # Ajusta posición para que no se solape
                xanchor="left",
                y=1.05,
                yanchor="top"
            )


        ],


    # Añadir capa de contorno 

        map=dict(
            style="carto-positron", # Mapa inicial
            center={'lat':41.405529,'lon':2.168878}, # coordenadas iniciales
            zoom=10 # Nivel de zoom inicial
        ),
        height=800,  # Altura personalizada
        width=1200 # anchura personalizada
    )
    #Mostrar mapa en Streamlit
    st.plotly_chart(fig,use_container_width=True)



