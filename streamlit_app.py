import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configura la página para usar el modo ancho
st.set_page_config(layout="wide")

#Establishing a Google Sheets Connection

conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(worksheet="database")

columna1,columna2,columna3, = st.columns([1,3,1])
with columna1:
    # Muestra el logo usando el nuevo parámetro
    st.image("logo.png", width=120)

with columna2:
    # Título de la aplicacións
    st.title('Club Deportivo Concón National')
    # Subtítulo
    st.subheader('Plataforma Área de Scouting')
    st.write("")  # Primer salto de línea
    st.write("")  # Segundo salto de línea


# Filtros interactivos
# Crear columnas para los filtros
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Filtrar por Equipo

    equipo = st.multiselect('Selecciona el Equipo', options=data['2025_Equipo'].unique())


with col2:
    # Filtrar por Nacionalidad
    nacionalidad = st.multiselect('Selecciona la Nacionalidad', options=data['Nacionalidad'].unique())

with col3:
    # Filtrar por Posición
    posicion = st.multiselect('Selecciona la Posición', options=data['Posicion'].unique())

with col4:

     # Filtrar por Edad
    edad_min = int(data['Edad_x'].min())
    edad_max = int(data['Edad_x'].max())

    edad_filtro = st.slider(
        'Selecciona el rango de Edad',
        min_value=edad_min,
        max_value=edad_max,
        value=(edad_min, edad_max),
        step=1
    )

fil1, fil2, fil3, fil4 = st.columns(4)

with fil1:
    division = st.multiselect('Selecciona la División', options=data['2025_Liga'].unique())


# Aplicar filtros
filtered_data = data.copy()

# Filtrar los datos


if equipo:
    filtered_data = filtered_data[filtered_data['Equipo_x'].isin(equipo)]

if nacionalidad:
    filtered_data = filtered_data[filtered_data['Nacionalidad_x'].isin(nacionalidad)]

if posicion:
    filtered_data = filtered_data[filtered_data['Posicion'].isin(posicion)]

if division:
    filtered_data = filtered_data[filtered_data['2025_Liga'].isin(division)]

# Filtrar por Edad, incluyendo los valores None
filtered_data = filtered_data[
    (pd.isna(filtered_data['Edad_x'])) | 
    ((filtered_data['Edad_x'] >= edad_filtro[0]) & (filtered_data['Edad_x'] <= edad_filtro[1]))
]


st.write("")  # Primer salto de línea
st.write("")  # Segundo salto de línea

columna1,columna2,columna3, = st.columns([1,3,1])

with columna1:
    st.metric(label="Cantidad total de jugadores", value=len(filtered_data))

with columna2:
# Mostrar datos filtrados
    columnas_seleccionadas = ["Nombre Jugador","Posicion","Posicion Secundaria","Edad_x","Nacionalidad_x","Equipo","2025_Liga","Valor de Mercado","Link Jugador"]
    st.subheader("Tabla con vista detallada")
st.dataframe(filtered_data)