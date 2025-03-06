import streamlit as st
import streamlit_app

# Cargar usuarios desde los secretos
USERS = st.secrets["auth"]

# Inicializar estado de sesión
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    # Contenedor principal centrado
    col1, col2, col3 = st.columns([1, 3, 1])  # Usamos 3 columnas, con la del medio más ancha

    with col2:  # Centrado en la columna del medio
        # Agregar logo del club
        st.image("logo.png", width=150)  # Ajusta el tamaño del logo según sea necesario

        # Caja de login
        st.title("Plataforma Scouting")

        username = st.text_input("Usuario", placeholder="Ingresa tu usuario")
        password = st.text_input("Contraseña", type="password", placeholder="••••••••")

        if st.button("Iniciar sesión", use_container_width=True):
            if username in USERS and USERS[username] == password:
                st.session_state["authenticated"] = True
                st.session_state["user"] = username
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")

if st.session_state["authenticated"]:
    streamlit_app.run_app()
else:
    login()

