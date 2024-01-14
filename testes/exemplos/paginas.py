import streamlit as st

# Função para a Página Inicial
def pagina_inicial():
    st.title("Página Inicial")
    st.write("Este é o conteúdo da Página Inicial.")

# Função para a Página de Configurações
def pagina_configuracoes():
    st.title("Página de Configurações")
    st.write("Este é o conteúdo da Página de Configurações.")

# Lista de páginas disponíveis
paginas = {
    "Página Inicial": pagina_inicial,
    "Página de Configurações": pagina_configuracoes
}

# Barra lateral para selecionar a página
pagina_selecionada = st.sidebar.selectbox("Selecione a Página", list(paginas.keys()))

# Exibe a página selecionada
paginas[pagina_selecionada]()
