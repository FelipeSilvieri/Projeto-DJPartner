# Importando Bibliotecas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from urllib.parse import quote

# Importanto classes
from model import Bot
from analytics import Analytics

# Inicializando Classe Bot
bot = Bot()

def run():
    session_state = st.session_state

    if 'page' not in session_state:
        session_state.page = 'header'
        session_state.artist = ''
        session_state.df = None
        session_state.set = ''
        session_state.df_set = None
        session_state.ppmean = 0
        session_state.displayable_df_set = None
        session_state.set_name = ''
        session_state.genre = ''

    if session_state.page == 'header':
        show_header(session_state)
    
    elif session_state.page == 'df':
        show_df(session_state)
    
    elif session_state.page == 'analytics':
        bot.get_artist_set_tracks(session_state.artist, session_state.set)
        artist_lista_tracks = session_state.artist.lower()
        artist_lista_tracks = artist_lista_tracks.replace(' ', '_')
        analytics = Analytics(f'{artist_lista_tracks}_{session_state.set}')
        analytics.tratando_dados()
        analytics.get_clusters()
        session_state.df_set = analytics.get_dataframe()
        session_state.dispayable_df_set = session_state.df_set[['Nome','Artistas Originais','Artistas Remix','Label','Playlists Plays','Track Position','Cluster']]
        session_state.set_name = session_state.df.iloc[int(session_state.set)]['name']
        session_state.genre = session_state.df.iloc[int(session_state.set)]['genre']
        session_state.date = session_state.df.iloc[int(session_state.set)]['date']
        session_state.top_tracks = analytics.get_highest_cluster()
        session_state.all_tracks = analytics.get_all_tracks_names()
        

        
        st.markdown('<h1 style="text-align: center; color: #626262;">📈 Resultados da Análise 📉</h1>', unsafe_allow_html=True)
        st.markdown(f'<h4 style="text-align: center; color: darkgrey;">{session_state.set_name}</h4>', unsafe_allow_html=True)
        st.markdown(f'<h5 style="text-align: center; color: darkgrey;">Gênero: {session_state.genre}</h5>', unsafe_allow_html=True)
        st.markdown(f'<h6 style="text-align: center; color: grey;">Data: {session_state.date}</h6>', unsafe_allow_html=True)
        
        st.markdown('<hr>', unsafe_allow_html=True)

        st.markdown('<h3 style="text-align: center; color: darkblue;">Análises Textuais</h3>', unsafe_allow_html=True)
        show_text_analytics(session_state) 
        st.markdown('<hr>', unsafe_allow_html=True)
        
        st.markdown('<h3 style="text-align: center; color: darkblue;">Análises Gráficas</h3>', unsafe_allow_html=True)
        show_analytics(session_state)
        
        st.markdown('<hr>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: darkblue">Tabela com as músicas do Set</h3>', unsafe_allow_html=True)
        show_dataframe(session_state)
        
        st.markdown('<hr>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: darkblue">Todas as tracks com HyperLink (Ordem Decrescente de Playlsits Plays):</h3>', unsafe_allow_html=True)
        list_all_songs(session_state)

def show_header(session_state):
    st.markdown('<h1 style="text-align: center;">BEM VINDO AO DJ PARTNER 🎛️<h1>', unsafe_allow_html=True)
    session_state.artist = st.text_input(label="Digite o nome do artista que deseja analisar:", placeholder='Artist Name')
    
    col1, col2, col3 , col4, col5 = st.columns(5)
    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3 :
        button_clicked = st.button(label="Buscar")
        
    if button_clicked:
        session_state.page = 'df'
        st.experimental_rerun()

def show_df(session_state):
    if session_state.artist:
        
        bot.get_artist_sets(session_state.artist)
        artist_lista_tracks = session_state.artist.lower()
        artist_lista_tracks = artist_lista_tracks.replace(' ', '_')
        session_state.df = pd.read_csv(f'artists_sets/{artist_lista_tracks}.csv')
        session_state.df = session_state.df[['name','date','genre','tracks_identificadas','qtd_tracks','link']]
        st.subheader("DataFrame:")
        st.dataframe(session_state.df)
        session_state.set = st.text_input(label='escolha um set:', placeholder='Set Index')
        
        button2_clicked = st.button(label="Analisar")

        if button2_clicked:
            session_state.page = 'analytics'
            st.experimental_rerun()
            
def show_analytics(session_state):
    if session_state.set:
        # Contar a ocorrência de valores na coluna 'Remix'
        contagem_remix = session_state.df_set['Remix'].notna().sum()
        contagem_nao_remix = len(session_state.df_set) - contagem_remix

        # Criar uma lista de contagens
        contagens = [contagem_remix, contagem_nao_remix]

        # Rótulos para as categorias
        rotulos = ['Remix', 'Original Mix']

        # Criar o gráfico de pizza
        fig, axs = plt.subplots(1,2,figsize=(12, 4)) # 1 linha, 2 colunas
        axs[0].pie(contagens, labels=rotulos, autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
        axs[0].set_title('Porcentagem de Remix vs. Não Remix')

        sns.boxplot(data=session_state.df_set, y='Playlists Plays', palette='Blues')
        axs[1].set_title('Boxplot de Playlists Plays')

        # Exibindo o gráfico
        plt.show()

        # Mostrar o gráfico usando st.pyplot
        st.pyplot(fig)
                
        # ------------------------------------------------------------------ #]
        
        mais_frequentes = more_frequent_artists(session_state)
        # Criando subplots com 1 linha e 2 colunas
        fig2, axes = plt.subplots(1, 2, figsize=(12, 7))

        # Gráfico 1: Artistas com mais de 1 ocorrência
        sns.barplot(x=mais_frequentes.index, y=mais_frequentes.values, palette='viridis', ax=axes[0])
        axes[0].set_title('Artistas com mais de 1 ocorrência no set')
        axes[0].set_xlabel('Artista')
        axes[0].set_ylabel('Contagem de Ocorrências')

        # Gráfico 2: Contagem de Remix e Não Remix
        unique_values = session_state.df_set['Remix'].unique()
        palette = {value: f'C{i}' for i, value in enumerate(unique_values)}
        sns.countplot(data=session_state.df_set, x='Remix', palette=palette, ax=axes[1])
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha='right')
        axes[1].set_ylabel('Contagem')
        axes[1].set_title('Contagem de Remix e Não Remix')

        plt.tight_layout()
        st.pyplot(fig2)
           
def show_text_analytics(session_state):
    session_state.ppmean = session_state.df_set['Playlists Plays'].mean()
    
    # Usando HTML para formatar o texto com cores
    session_state.text_artist = f'<span style="color: blue;">{session_state.artist}</span>'
    session_state.text_ppmean = f'<span style="color: green;">{int(session_state.ppmean)}</span>'
    
    # Encontrar a música com mais Playlists Plays
    index_musica_mais_popular = session_state.df_set['Playlists Plays'].idxmax()
    musica_mais_popular = f"{session_state.df_set.loc[index_musica_mais_popular, 'Artista']} - {session_state.df_set.loc[index_musica_mais_popular, 'Nome']}"
    max_pp = session_state.df_set['Playlists Plays'].max()

    # Usando HTML para formatar o texto com cores
    session_state.text_musica_p = f'<span style="color: blue;">{musica_mais_popular}</span>'
    session_state.text_pmax_p= f'<span style="color: green;">{int(max_pp)}</span>'
    
    list_html = f"""
        <ul>
            <li>A média de Plays em outros Sets das músicas presentes nesse set de {session_state.text_artist} é de {session_state.text_ppmean}.</li>
            <li>A música mais popular em termos de Playlists Plays é "{session_state.text_musica_p}" com {session_state.text_pmax_p} reproduções.</li>
        </ul>
    """
    
    st.markdown(list_html, unsafe_allow_html=True)
    
    st.markdown('<h6 style="color: darkgrey; text-align: center;">Tracks mais famosas (com base nos Playlists Plays):<h6>',unsafe_allow_html=True)
    
    for track in session_state.top_tracks:
        # Use a função quote para codificar o nome da faixa para URL
        track_yt_url = quote(track)
        
        # Crie a URL do YouTube
        url = f'https://www.youtube.com/results?search_query={track_yt_url}'

        # Crie o texto Markdown com o link e estilo CSS para centralizar horizontalmente
        markdown_text = f"""
            <div style="text-align: center;">
                <a href="{url}" style="display: inline-block;">{track}</a>
            </div>
        """

        # Renderize usando st.markdown
        st.markdown(markdown_text, unsafe_allow_html=True)

def show_dataframe(session_state):
    st.dataframe(session_state.dispayable_df_set)
    
def list_all_songs(session_state):
    for track in session_state.all_tracks:
        # Use a função quote para codificar o nome da faixa para URL
        track_yt_url = quote(track)
        
        # Crie a URL do YouTube
        url = f'https://www.youtube.com/results?search_query={track_yt_url}'

        # Crie o texto Markdown com o link e estilo CSS para centralizar horizontalmente
        markdown_text = f"""
            <div style="text-align: center;">
                <a href="{url}" style="display: inline-block;">{track}</a>
            </div>
        """

        # Renderize usando st.markdown
        st.markdown(markdown_text, unsafe_allow_html=True)
    
def more_frequent_artists(session_state):
    df_exploded = session_state.df_set.explode('Lista Artistas')

    # Contando a ocorrência de músicas por artista
    occurrences = df_exploded['Lista Artistas'].value_counts()

    # Filtrando apenas artistas com mais de uma ocorrência
    occurrences_filtered = occurrences[occurrences > 1]
    return occurrences_filtered
  
if __name__ == "__main__":
    run()
