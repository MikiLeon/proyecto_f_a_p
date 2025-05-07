import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def cargar_datos_restos(url):
    df = pd.read_csv(url)
    df['lat'] = df['lat'].astype(float)
    df['lon'] = df['lon'].astype(float)
    df['Observaciones'] = df['Observaciones'].fillna('')
    df_agrupado = df.groupby(['Mes', 'Barrio', 'Distrito', 'lat', 'lon', 'Tipo', 'Observaciones'], as_index=False)['Cantidad'].sum()
    df_agrupado['Tipo'] = pd.Categorical(df_agrupado['Tipo'])
    return df_agrupado

def cargar_datos_servicios(url):
    df = pd.read_csv(url)
    return df


def crear_trazas_consumos(df):
    trazas = []
    tipos = df['Tipo'].unique()
    colores = px.colors.qualitative.D3
    color_map = {tipo: colores[i % len(colores)] for i, tipo in enumerate(tipos)}

    for tipo in tipos:
        df_tipo = df[df['Tipo'] == tipo]
        traza = go.Scattermap(
            lat=df_tipo['lat'],
            lon=df_tipo['lon'],
            mode='markers',
            marker=dict(
                size=df_tipo['Cantidad'],
                color=color_map[tipo],
                sizemode='area',
                sizeref=2.*max(df['Cantidad'])/(40.**2),
                sizemin=4,
                opacity=0.7
            ),
            hovertemplate="<b>%{hovertext}</b><br>Cantidad: %{customdata[0]}<br>Barrio: %{customdata[1]}<br>Distrito: %{customdata[2]}<br>Mes: %{customdata[3]}<br>Observaciones: %{customdata[4]}<extra></extra>",
            hovertext=df_tipo['Tipo'],
            customdata=df_tipo[['Cantidad','Barrio','Distrito','Mes', 'Observaciones']].values,
            name=tipo,
            showlegend=True
        )
        trazas.append(traza)
    return trazas


def crear_trazas_servicios(df):
    trazas = []
    tipos = df['Tipo'].unique()
    colores = px.colors.qualitative.Set1
    color_map = {tipo: colores[i % len(colores)] for i, tipo in enumerate(tipos)}

    for tipo in tipos:
        df_tipo = df[df['Tipo'] == tipo]
        traza = go.Scattermap(
            lat=df_tipo['lat'],
            lon=df_tipo['lon'],
            mode='markers',
            marker=dict(
                size=14,
                color=color_map[tipo],
                symbol='marker',
                opacity=0.8
            ),
            hovertext=df_tipo['Nombre'],
            text=df_tipo['Tipo'],
            hovertemplate="<b>%{hovertext}</b><br>Tipo: %{text}<extra></extra>",
            name=tipo,
            showlegend=True
        )
        trazas.append(traza)
    return trazas