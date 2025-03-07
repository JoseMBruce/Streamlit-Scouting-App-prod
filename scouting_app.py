import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import matplotlib.pyplot as plt

def run_app():

    # Configura la página para usar el modo ancho
    st.set_page_config(layout="wide")

    #Establishing a Google Sheets Connection

    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(worksheet="database")

    # Columna para el logo y el título
    columna1, columna2, columna3 = st.columns([2, 1, 1])


    with columna1:
        st.title('Club Deportivo Concón National')
        st.subheader('Plataforma Área de Scouting')
        st.write("")  # Primer salto de línea
        st.write("")  # Segundo salto de línea
    with columna3:
        st.image("logo.png", width=120)

    
    # Agregar botón de cerrar sesión en la sidebar
    with st.sidebar:
        st.write(f"**Usuario:** {st.session_state.get('user', 'Desconocido')}")
        if st.button("Cerrar sesión"):
            st.session_state["authenticated"] = False
            st.rerun()  # Recargar la app para volver al login

    # Filtros interactivos en la barra lateral
    st.sidebar.header("Filtros para buscar Jugadores")

    # Filtros en la barra lateral
    equipo = st.sidebar.multiselect('Selecciona el Equipo', options=data['Equipo'].unique())
    st.sidebar.markdown("\n")  # Espacio entre filtros
    liga = st.sidebar.multiselect('Selecciona la Liga', options=data['2025_Liga'].unique())
    st.sidebar.markdown("\n")  # Espacio entre filtros
    nacionalidad = st.sidebar.multiselect('Selecciona la Nacionalidad', options=data['Nacionalidad'].unique())
    st.sidebar.markdown("\n")  # Espacio entre filtros
    posicion = st.sidebar.multiselect('Selecciona la Posición', options=data['Posición'].unique())
    st.sidebar.markdown("\n")  # Espacio entre filtros
    valoracion_scouting = st.sidebar.multiselect('Selecciona la Valoración Scouting', options=data['Valoracion Scouting'].unique())
    st.sidebar.markdown("\n")  # Espacio entre filtros

    edad_min = int(data['Edad'].min())
    edad_max = int(data['Edad'].max())

    edad_filtro = st.sidebar.slider(
        'Selecciona el rango de Edad',
        min_value=edad_min,
        max_value=edad_max,
        value=(edad_min, edad_max),
        step=1
    )

    # Aplicar filtros
    filtered_data = data.copy()

    if equipo:
        filtered_data = filtered_data[filtered_data['Equipo'].isin(equipo)]

    if liga:
        filtered_data = filtered_data[filtered_data['2025_Liga'].isin(liga)]

    if nacionalidad:
        filtered_data = filtered_data[filtered_data['Nacionalidad'].isin(nacionalidad)]

    if posicion:
        filtered_data = filtered_data[filtered_data['Posición'].isin(posicion)]

    # Filtro de Valoración Scouting
    if valoracion_scouting:
        filtered_data = filtered_data[filtered_data['Valoracion Scouting'].isin(valoracion_scouting)]



    filtered_data = filtered_data[
        (pd.isna(filtered_data['Edad'])) | 
        ((filtered_data['Edad'] >= edad_filtro[0]) & (filtered_data['Edad'] <= edad_filtro[1]))
    ]


    columna1,columna2,columna3 = st.columns([2,1,6])

    with columna1:
        st.metric(label="Cantidad total de jugadores", value=len(filtered_data))
        st.write("")  # Segundo salto de línea
        st.write("")  # Segundo salto de línea
        # Crear un selectbox para seleccionar un jugador
        jugadores = filtered_data["Nombre Jugador"].tolist()

        st.markdown(f"#### Obtener vista detallada sobre un jugador")

        # Usar el selectbox para seleccionar un jugador
        jugador_seleccionado = st.selectbox("Selecciona un jugador para ver más detalles:", jugadores)

        # Filtrar el dataframe para obtener solo el jugador seleccionado
        jugador_seleccionado_data = filtered_data[filtered_data["Nombre Jugador"] == jugador_seleccionado]


        if not filtered_data.empty:
            pk_seleccionado = jugador_seleccionado_data["soccerway_pk"].values[0]
        else:
            # Maneja el caso en el que no se encuentra el jugador
            pk_seleccionado = None  # O algún valor predeterminado
            st.error("El jugador seleccionado no fue encontrado.")

        # Botón para mostrar detalles del jugador
        if st.button("Ver detalles del jugador"):
            # Al presionar el botón, almacenamos la clave primaria en st.session_state
            st.session_state.soccerway_pk_seleccionado = pk_seleccionado

        st.markdown(f"#### Comparar dos jugadores")

        # Crear un selectbox para seleccionar el primer jugador
        jugadores = filtered_data["Nombre Jugador"].tolist()

        jugador_seleccionado_1 = st.selectbox("Selecciona el primer jugador para ver más detalles:", jugadores)

        # Crear un selectbox para seleccionar el segundo jugador
        jugador_seleccionado_2 = st.selectbox("Selecciona el segundo jugador para ver más detalles:", jugadores)

        # Filtrar el dataframe para obtener solo el jugador seleccionado
        jugador_seleccionado_data_1 = filtered_data[filtered_data["Nombre Jugador"] == jugador_seleccionado_1]
        # Filtrar el dataframe para obtener solo el jugador seleccionado
        jugador_seleccionado_data_2 = filtered_data[filtered_data["Nombre Jugador"] == jugador_seleccionado_2]

        # Verificar si los jugadores existen antes de acceder a los valores
        if not filtered_data.empty:
            pk_seleccionado_1 = jugador_seleccionado_data_1["soccerway_pk"].values[0]
        else:
            pk_seleccionado_1 = None
            st.error(f"No se encontró el jugador: {jugador_seleccionado_1}")

        if not filtered_data.empty:
            pk_seleccionado_2 = jugador_seleccionado_data_2["soccerway_pk"].values[0]
        else:
            pk_seleccionado_2 = None
            st.error(f"No se encontró el jugador: {jugador_seleccionado_2}")

        # Botón para mostrar detalles de los dos jugadores seleccionados
        if st.button("Comparar jugadores"):
            if pk_seleccionado_1 is not None and pk_seleccionado_2 is not None:
                # Al presionar el botón, almacenamos las claves primarias en st.session_state
                st.session_state.soccerway_pk_seleccionado_1 = pk_seleccionado_1
                st.session_state.soccerway_pk_seleccionado_2 = pk_seleccionado_2
            else:
                st.warning("No se pueden comparar jugadores si alguno no fue encontrado.")

        
    with columna3:  
    # Mostrar datos filtrados
        columnas_seleccionadas = ["Nombre Jugador","Posición","Posicion Secundaria","Edad","Nacionalidad","Equipo","Valoracion Scouting"]
        st.subheader("Tabla con vista preeliminar")
        st.write("")  # Segundo salto de línea
        st.dataframe(filtered_data[columnas_seleccionadas])


    columna1,columna2,columna3 = st.columns([1,3,1])

    with columna2:
        if 'soccerway_pk_seleccionado' in st.session_state:
            # Obtener los detalles completos del jugador usando la clave primaria (soccerway_pk)
            jugador_detalles = data[data["soccerway_pk"] == st.session_state.soccerway_pk_seleccionado]
            
            # Si los detalles del jugador están disponibles
            if not jugador_detalles.empty:
                jugador_info = jugador_detalles.iloc[0]  # Selecciona el primer registro (debe ser único)
                
                # Título de la vista de detalles
                st.subheader(f"Detalles de {jugador_info['Nombre Jugador']}")

                # Usar columnas para organizar la información
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.write("")  # Segundo salto de línea
                    st.write(f"**Posición:** {jugador_info['Posición']}")
                    st.write(f"**Edad:** {jugador_info['Edad']}")
                    st.write(f"**Altura:** {jugador_info['Altura']}")
                    st.write(f"**Peso:** {jugador_info['Peso']}")
                    st.write(f"**Pie dominante:** {jugador_info['Pie']}")
                    st.write(f"**Valoración Scouting:** {jugador_info['Valoracion Scouting']}")
                
                with col2:
                    st.write("")  # Segundo salto de línea
                    st.write(f"**Posición Secundaria:** {jugador_info['Posicion Secundaria']}")
                    st.write(f"**Equipo actual:** {jugador_info['Equipo']}")
                    st.write(f"**Nacionalidad:** {jugador_info['Nacionalidad']}")
                    st.write(f"**Fecha de nacimiento:** {jugador_info['Fecha de nacimiento']}")
                    st.write(f"**Score:** {jugador_info['ELO']}")
                    # Agregar selectbox para valoración del scouting
                    opciones_valoracion = ["Seguir", "Sin interés","Predeterminada"]
                    valoracion_actual = jugador_info.get("Valoracion Scouting","Predeterminada")  # Valor por defecto
                    valoracion_seleccionada = st.selectbox(
                        "Para cambiar valoración seleccione una opción:",
                        opciones_valoracion,
                        index=opciones_valoracion.index(valoracion_actual)
                    )

                    # Botón para guardar cambios en Google Sheets
                    if st.button("Guardar Cambios"):
                        try:
                            # Leer el DataFrame original desde Google Sheets
                            df_original = conn.read(worksheet="database")

                            # Asegurarse de que los datos están indexados correctamente por la llave primaria
                            df_original.set_index('soccerway_pk', inplace=True)

                            # Actualizar solo la fila correspondiente si el valor cambia
                            if jugador_info["soccerway_pk"] in df_original.index:
                                df_original.loc[jugador_info["soccerway_pk"], "Valoracion Scouting"] = valoracion_seleccionada 

                                # Subir el DataFrame actualizado a Google Sheets
                                conn.update(worksheet="database", data=df_original.reset_index())

                                st.success("¡Datos actualizados en Google Sheets!")
                                # **Forzar la recarga de la página para actualizar los datos**
                                st.rerun()
                            else:
                                st.error("No se encontró el jugador en la base de datos.")
                        except Exception as e:
                            st.error(f"Error al actualizar los datos en Google Sheets: {e}")
            
                # Estadísticas por temporada
                st.subheader("Estadísticas por Temporada")
                
                # Datos de estadísticas de 2025 y 2024
                stats_2025 = {
                    "Temporada": jugador_info['2025_Temporada'],
                    "Minutos Jugados": jugador_info['2025_Minutos Jugados'],
                    "Apariciones": jugador_info['2025_Apariciones'],
                    "Goles": jugador_info['2025_Gol'],
                    "Amarillas": jugador_info['2025_Amarilla'],
                    "Rojas": jugador_info['2025_Roja']
                }

                stats_2024 = {
                    "Temporada": jugador_info['2024_Temporada'],
                    "Minutos Jugados": jugador_info['2024_Minutos Jugados'],
                    "Apariciones": jugador_info['2024_Apariciones'],
                    "Goles": jugador_info['2024_Gol'],
                    "Amarillas": jugador_info['2024_Amarilla'],
                    "Rojas": jugador_info['2024_Roja']
                }

                # Crear DataFrames para las temporadas 2025 y 2024
                df_2025 = pd.DataFrame(stats_2025, index=[0])
                df_2024 = pd.DataFrame(stats_2024, index=[0])

                # Unir ambos DataFrames verticalmente
                df_combined = pd.concat([df_2025, df_2024], ignore_index=True)

                # Mostrar el DataFrame combinado
                st.write(df_combined)

                            # Mostrar información adicional como Valor de Mercado, Agente, Fichado, Contrato Hasta
                st.write("")  # Segundo salto de línea
                st.subheader("Información adicional:")
                st.write(f"**Valor de Mercado:** {jugador_detalles['Valor de Mercado'].values[0]}")
                st.write(f"**Agente:** {jugador_detalles['Agente'].values[0]}")
                st.write(f"**Fichado:** {jugador_detalles['Fichado'].values[0]}")
                st.write(f"**Contrato Hasta:** {jugador_detalles['Contrato Hasta'].values[0]}")

                # Mostrar las habilidades de scouting si las tienes
                st.subheader("Evaluación y Habilidades")
                
                habilidades = {
                    'Ritmo': jugador_info['Ritmo'],
                    'Tiro': jugador_info['Tiro'],
                    'Pase': jugador_info['Pase'],
                    'Regate': jugador_info['Regate'],
                    'Defensa': jugador_info['Defensa'],
                    'Físico': jugador_info['Físico'],
                    'Salto': jugador_info['Salto'],
                    'Estirada': jugador_info['Estirada'],
                    'Paradas': jugador_info['Paradas'],
                    'Saques': jugador_info['Saques'],
                    'Colocación': jugador_info['Colocación'],
                    'Reflejos': jugador_info['Reflejos']
                }
                
                # Convertir el diccionario a un DataFrame y reemplazar valores faltantes con 0
                df_habilidades = pd.DataFrame(habilidades, index=[0]).fillna(0)

                # Asegurar que todos los valores sean numéricos para evitar errores en comparaciones
                df_habilidades = df_habilidades.apply(pd.to_numeric, errors="coerce").fillna(0)

                # Filtrar habilidades con valores mayores a 0
                df_habilidades_filtrado = df_habilidades.loc[:, df_habilidades.iloc[0] > 0]

                # Mostrar el DataFrame
                st.write(df_habilidades_filtrado)
                
                # Crear gráfico de barras vertical
                fig, ax = plt.subplots(figsize=(6, 4))

                # Plot vertical
                ax.bar(df_habilidades_filtrado.columns, df_habilidades_filtrado.iloc[0])

                # Establecer título y etiquetas
                ax.set_title('Habilidades del Jugador')
                ax.set_xlabel('Habilidades')
                ax.set_ylabel('Puntuación')

                # Mostrar gráfico
                st.pyplot(fig)

        if 'soccerway_pk_seleccionado_1' in st.session_state and 'soccerway_pk_seleccionado_2' in st.session_state:
            # Obtener los detalles completos de ambos jugadores usando las claves primarias (soccerway_pk)
            jugador_detalles_1 = data[data["soccerway_pk"] == st.session_state.soccerway_pk_seleccionado_1]
            jugador_detalles_2 = data[data["soccerway_pk"] == st.session_state.soccerway_pk_seleccionado_2]
            
            # Verificar si los detalles de ambos jugadores están disponibles
            if not jugador_detalles_1.empty and not jugador_detalles_2.empty:
                jugador_info_1 = jugador_detalles_1.iloc[0]  # Primer jugador
                jugador_info_2 = jugador_detalles_2.iloc[0]  # Segundo jugador

                # Título de la vista de comparación
                st.subheader(f"Comparación entre {jugador_info_1['Nombre Jugador']} y {jugador_info_2['Nombre Jugador']}")

                # Usar columnas para organizar la información de ambos jugadores
                col1, col2 = st.columns([1, 1])

                # Mostrar detalles del primer jugador
                with col1:
                    st.write(f"**Posición:** {jugador_info_1['Posición']}")
                    st.write(f"**Edad:** {jugador_info_1['Edad']}")
                    st.write(f"**Altura:** {jugador_info_1['Altura']}")
                    st.write(f"**Peso:** {jugador_info_1['Peso']}")
                    st.write(f"**Pie dominante:** {jugador_info_1['Pie']}")
                    st.write(f"**Score:** {jugador_info_1['ELO']}")

                # Mostrar detalles del segundo jugador
                with col2:
                    st.write(f"**Posición:** {jugador_info_2['Posición']}")
                    st.write(f"**Edad:** {jugador_info_2['Edad']}")
                    st.write(f"**Altura:** {jugador_info_2['Altura']}")
                    st.write(f"**Peso:** {jugador_info_2['Peso']}")
                    st.write(f"**Pie dominante:** {jugador_info_2['Pie']}")
                    st.write(f"**Score:** {jugador_info_2['ELO']}")

                # Estadísticas por temporada
                st.subheader("Estadísticas por Temporada")

                # Crear DataFrames para las temporadas 2025 y 2024 de ambos jugadores
                stats_2025_1 = {
                    "Temporada": jugador_info_1['2025_Temporada'],
                    "Minutos Jugados": jugador_info_1['2025_Minutos Jugados'],
                    "Apariciones": jugador_info_1['2025_Apariciones'],
                    "Goles": jugador_info_1['2025_Gol'],
                    "Amarillas": jugador_info_1['2025_Amarilla'],
                    "Rojas": jugador_info_1['2025_Roja']
                }

                stats_2025_2 = {
                    "Temporada": jugador_info_2['2025_Temporada'],
                    "Minutos Jugados": jugador_info_2['2025_Minutos Jugados'],
                    "Apariciones": jugador_info_2['2025_Apariciones'],
                    "Goles": jugador_info_2['2025_Gol'],
                    "Amarillas": jugador_info_2['2025_Amarilla'],
                    "Rojas": jugador_info_2['2025_Roja']
                }

                stats_2024_1 = {
                    "Temporada": jugador_info_1['2024_Temporada'],
                    "Minutos Jugados": jugador_info_1['2024_Minutos Jugados'],
                    "Apariciones": jugador_info_1['2024_Apariciones'],
                    "Goles": jugador_info_1['2024_Gol'],
                    "Amarillas": jugador_info_1['2024_Amarilla'],
                    "Rojas": jugador_info_1['2024_Roja']
                }

                stats_2024_2 = {
                    "Temporada": jugador_info_2['2024_Temporada'],
                    "Minutos Jugados": jugador_info_2['2024_Minutos Jugados'],
                    "Apariciones": jugador_info_2['2024_Apariciones'],
                    "Goles": jugador_info_2['2024_Gol'],
                    "Amarillas": jugador_info_2['2024_Amarilla'],
                    "Rojas": jugador_info_2['2024_Roja']
                }

                # Crear DataFrames para las temporadas 2025 y 2024 para ambos jugadores
                df_2025_1 = pd.DataFrame(stats_2025_1, index=[0])
                df_2025_2 = pd.DataFrame(stats_2025_2, index=[0])

                df_2024_1 = pd.DataFrame(stats_2024_1, index=[0])
                df_2024_2 = pd.DataFrame(stats_2024_2, index=[0])

                # Unir ambos DataFrames verticalmente
                df_combined_2025 = pd.concat([df_2025_1, df_2025_2], ignore_index=True)
                df_combined_2024 = pd.concat([df_2024_1, df_2024_2], ignore_index=True)

                # Mostrar los DataFrames combinados
                st.write("Estadísticas 2025:")
                st.write(df_combined_2025)

                st.write("Estadísticas 2024:")
                st.write(df_combined_2024)

                # Comparación de habilidades
                st.subheader("Evaluación y Habilidades")

                habilidades_1 = {
                    'Ritmo': jugador_info_1['Ritmo'],
                    'Tiro': jugador_info_1['Tiro'],
                    'Pase': jugador_info_1['Pase'],
                    'Regate': jugador_info_1['Regate'],
                    'Defensa': jugador_info_1['Defensa'],
                    'Físico': jugador_info_1['Físico'],
                    'Salto': jugador_info_1['Salto'],
                    'Estirada': jugador_info_1['Estirada'],
                    'Paradas': jugador_info_1['Paradas'],
                    'Saques': jugador_info_1['Saques'],
                    'Colocación': jugador_info_1['Colocación'],
                    'Reflejos': jugador_info_1['Reflejos']
                }

                habilidades_2 = {
                    'Ritmo': jugador_info_2['Ritmo'],
                    'Tiro': jugador_info_2['Tiro'],
                    'Pase': jugador_info_2['Pase'],
                    'Regate': jugador_info_2['Regate'],
                    'Defensa': jugador_info_2['Defensa'],
                    'Físico': jugador_info_2['Físico'],
                    'Salto': jugador_info_2['Salto'],
                    'Estirada': jugador_info_2['Estirada'],
                    'Paradas': jugador_info_2['Paradas'],
                    'Saques': jugador_info_2['Saques'],
                    'Colocación': jugador_info_2['Colocación'],
                    'Reflejos': jugador_info_2['Reflejos']
                }

                # Convertir los diccionarios a DataFrames
                df_habilidades_1 = pd.DataFrame(habilidades_1, index=[0]).fillna(0)
                df_habilidades_2 = pd.DataFrame(habilidades_2, index=[0]).fillna(0)

                # Asegurar que todos los valores sean numéricos para evitar errores en comparaciones
                df_habilidades_1 = df_habilidades_1.apply(pd.to_numeric, errors="coerce").fillna(0)
                df_habilidades_2 = df_habilidades_2.apply(pd.to_numeric, errors="coerce").fillna(0)

                # Filtrar habilidades con valores mayores a 0
                df_habilidades_1_filtrado = df_habilidades_1.loc[:, df_habilidades_1.iloc[0] > 0]
                df_habilidades_2_filtrado = df_habilidades_2.loc[:, df_habilidades_2.iloc[0] > 0]

                # Mostrar los DataFrames de habilidades filtrados
                st.write("Habilidades del Primer Jugador:")
                st.write(df_habilidades_1_filtrado)

                st.write("Habilidades del Segundo Jugador:")
                st.write(df_habilidades_2_filtrado)
