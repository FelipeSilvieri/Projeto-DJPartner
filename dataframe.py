import streamlit as st
import pandas as pd

# Sample DataFrame
data = {
    'Artista': ['Artist 1', 'Artist 2', 'Artist 3'],
    'Nome': ['Song 1', 'Song 2', 'Song 3'],
    'Link': ['http://link1', 'http://link2', 'http://link3']
}

df = pd.DataFrame(data)

# Format the 'Link' column as HTML with custom styling
df['Link'] = df['Link'].apply(lambda x: f'<a href="{x}" target="_blank" style="color: inherit; text-decoration: none;">{x}</a>')

# Display DataFrame with HTML content
st.write(df.to_html(escape=False), unsafe_allow_html=True)
