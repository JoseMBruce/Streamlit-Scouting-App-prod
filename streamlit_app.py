import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Read Google Sheet as DataFrame")
st.markdown("Enter title")

#Establishing a Google Sheets Connection

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="database", usecols=list(range(6)),ttl=5)

st.dataframe(df)