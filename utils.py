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
    df_agrupado['Mes'] = pd.to_datetime(df_agrupado['Mes'], format= '%m/%y')
    return df_agrupado

def cargar_datos_servicios(url):
    df = pd.read_csv(url)
    return df

def calcular_totales_restos(df):
    #Total por tipo
    total_por_tipo = df.groupby('Tipo')['Cantidad'].sum().sort_values(ascending=False)
     #Total por barrio
    total_por_barrio = df.groupby('Barrio')['Cantidad'].sum().sort_values(ascending=False)
    #Total por distrito
    total_por_distrito = df.groupby('Distrito')['Cantidad'].sum().sort_values(ascending=False)
    return total_por_tipo, total_por_barrio,total_por_distrito

def contar_servicios_por_tipo_distrito(df):
    return df.groupby(['Distrito','Tipo' ]).size().reset_index(name='Cantidad')

#Grafíco barras totales
def grafico_barras_totales(series, titulo, x_label, y_label):
    fig = px.bar(
        x= series.index,
        y= series.values,
        labels={'x':x_label,'y':y_label},
        title=titulo
        )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

#grafico  barras servicios

def grafico_barras_servicios(df, titulo):
    fig = px.bar(
        df,
        x= 'Distrito',
        y = 'Cantidad',
        color= 'Tipo',
        title= titulo,
        labels={'Distrito':'Distritos','Cantidad':'Cantidad de servicios','Tipo':'Tipo de servicio' }
        )
    fig.update_layout(barmode='stack',xaxis={'categoryorder':'total descending'} )
    return fig

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
    colores = px.colors.qualitative.Set3
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