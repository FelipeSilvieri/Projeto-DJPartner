import streamlit as st
import pandas as pd

# Exemplo de dataset fictício
data = {
    'Nome da Música': ['Música 1', 'Música 2', 'Música 3'],
    'Nome do Artista': ['Artista 1', 'Artista 2', 'Artista 3'],
    'Link da Música': ['http://link1.com', 'http://link2.com', 'http://link3.com']
}

df = pd.DataFrame(data)

# Aplicativo Streamlit
st.title("Lista de Músicas")

# Itera sobre as linhas do DataFrame
for index, row in df.iterrows():
    st.write(f"Checkbox: {st.checkbox('')}, Artista: {row['Nome do Artista']}, Link: {row['Link da Música']}")
