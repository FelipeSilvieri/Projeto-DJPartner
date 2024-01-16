# Importando Bibliotecas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
from urllib.parse import quote

# Importanto classes
from model import Bot
from analytics import Analytics


def run():
    # Inicializando Classe Bot
    bot = Bot()
    
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
        session_state.displayable_df_set = session_state.df_set[['Nome','Artistas Originais','Artistas Remix','Label','Playlists Plays','Track Position']]
        session_state.set_name = session_state.df.iloc[int(session_state.set)]['name']
        session_state.genre = session_state.df.iloc[int(session_state.set)]['genre']
        session_state.date = session_state.df.iloc[int(session_state.set)]['date']
        session_state.top_tracks, session_state.top_plays = analytics.get_top_5()
        session_state.all_tracks, session_state.all_plays = analytics.get_all_tracks_names()
        session_state.first_track = None
        session_state.last_track = None
        
        # ------------------------------------------ First Track ----------------------------------------------------
        indice_menor_posicao = session_state.df_set['Track Position'].idxmin()
        artista_min = session_state.df_set.loc[indice_menor_posicao, 'Artista']
        nome_min = session_state.df_set.loc[indice_menor_posicao, 'Nome']
        remix_min = session_state.df_set.loc[indice_menor_posicao, 'Remix']
        session_state.track_position_min = session_state.df_set.loc[indice_menor_posicao, 'Track Position']
        if not math.isnan(remix_min):
            session_state.first_track = f"{artista_min} - {nome_min} ({remix_min})"
        else:
            session_state.first_track = f"{artista_min} - {nome_min}"
        
        # ------------------------------------------ Last Track ----------------------------------------------------
        indice_maior_posicao = session_state.df_set['Track Position'].idxmax()
        artista_max = session_state.df_set.loc[indice_maior_posicao, 'Artista']
        nome_max = session_state.df_set.loc[indice_maior_posicao, 'Nome']
        remix_max = session_state.df_set.loc[indice_maior_posicao, 'Remix']
        if not math.isnan(remix_max):
            session_state.last_track = f"{artista_max} - {nome_max} ({remix_max})"
        else:
            session_state.last_track = f"{artista_max} - {nome_max}"
            
        # ----------------------------------------------------------------------------------------------------------

        st.markdown('<h1 style="text-align: center; color: #626262;">📈 Resultados da Análise 📉</h1>', unsafe_allow_html=True)
        st.markdown(f'<h4 style="text-align: center; color: darkgrey;">{session_state.set_name}</h4>', unsafe_allow_html=True)
        st.markdown(f'<h5 style="text-align: center; color: darkgrey;">Gênero: {session_state.genre}</h5>', unsafe_allow_html=True)
        st.markdown(f'<h6 style="text-align: center; color: grey;">Data: {session_state.date}</h6>', unsafe_allow_html=True)
        
        st.markdown('<hr>', unsafe_allow_html=True)


        text_playlist_plays = """
            <div style="padding: 10px; margin: 16px; border: 1px solid lightgrey; border-radius: 5px;">            
                <h4 style="text-align: center; color: darkblue;">O que são "Playlists Plays"? 🧐</h4>
                <p style="background-color: lightgrey; color: grey; border-radius: 5px; text-align: center;"><strong>Playlists Plays</strong> são basicamente <strong>quantas vezes</strong> tal musica foi tocada <strong>em outros sets!</strong> </p>
                <p style="text-align: center;">(ou seja, o tanto de suporte que essa track teve)</p>
            </div>
        """        
        st.markdown(text_playlist_plays,unsafe_allow_html=True)
        show_text_analytics(session_state) 
        
        text_intro_outro = f"""
            <div style="padding: 10px; margin-top: 16px; border: 1px solid lightgrey; background-color: lightgrey ; border-radius: 5px;">            
                <h4 style="text-align: center; color: darkred;">⏭️ Como começou, e como terminou? ⏮️</h4>
                <p style="background-color: white; color: grey; border-radius: 5px; text-align: center;">
                    A <strong>{session_state.track_position_min}ª</strong> Música tocada foi <strong>{session_state.first_track}</strong>
                </p>
                <p style="background-color: white; color: grey; border-radius: 5px; text-align: center;">
                    A <strong>última</strong> Música listada tocada foi <strong>{session_state.last_track}</strong>
                </p>
            </div>
        """
        
        st.markdown(text_intro_outro,unsafe_allow_html=True)

        st.markdown('<hr>', unsafe_allow_html=True)
        
        st.markdown('<h4 style="text-align: center; color: darkblue; margin-bottom: 16px;">Análise de Playlists Plays ▶️</h4>', unsafe_allow_html=True)
        show_playlists_plays_analytics(session_state)
        
        st.markdown('<h4 style="text-align: center; color: darkblue; margin-bottom: 16px;">Análise de Remixes 📀</h4>', unsafe_allow_html=True)
        show_remix_analytics(session_state)
        
        st.markdown('<h4 style="text-align: center; color: darkblue; margin-bottom: 16px;">Análise de Artistas 👨‍🦱</h4>', unsafe_allow_html=True)
        show_artists_analytics(session_state)
        
        st.markdown('<h4 style="text-align: center; color: darkblue; margin-bottom: 16px;">Análise Temporal Set 🕝</h4>', unsafe_allow_html=True)
        show_set_order(session_state)
                
        st.markdown('<hr>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: darkblue">Tabela com as músicas do Set</h3>', unsafe_allow_html=True)
        st.markdown('<h6 style="text-align: center; background-color: lightgrey; border-radius: 5px;">obs: você pode ordenar cada coluna da maneira desejada, apenas clicando na coluna.</h6>', unsafe_allow_html=True)
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
        st.rerun()

def show_df(session_state):
    # Inicializando Classe Bot
    bot = Bot()
    
    if session_state.artist:
        
        bot.get_artist_sets(session_state.artist)
        artist_lista_tracks = session_state.artist.lower()
        artist_lista_tracks = artist_lista_tracks.replace(' ', '_')
        session_state.df = pd.read_csv(f'artists_sets/{artist_lista_tracks}.csv')
        session_state.df = session_state.df[['name','date','genre','tracks_identificadas','qtd_tracks','link']]
        st.subheader(f"Lista de Sets do Artista {session_state.artist}:")
        st.dataframe(session_state.df)
        session_state.set = st.text_input(label='escolha um set:', placeholder='Set Index')
        
        button2_clicked = st.button(label="Analisar")

        if button2_clicked:
            session_state.page = 'analytics'
            st.experimental_rerun()
            
def show_playlists_plays_analytics(session_state):
    if session_state.set:
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))

        sns.set(style="whitegrid")  # Adiciona essa linha para remover a grid do boxplot

        sns.boxplot(data=session_state.df_set, y='Playlists Plays', palette='Blues', ax=axs[0])
        axs[0].set_title('Boxplot de Playlists Plays')

        axs[1].hist(session_state.df_set['Playlists Plays'].dropna(), bins=20, color='skyblue', edgecolor='black')
        axs[1].set_xlabel('Playlist Plays')
        axs[1].set_ylabel('Frequência')
        axs[1].set_title('Histograma de Playlist Plays')

        plt.tight_layout()
        st.pyplot(fig)
        

        # Verifica a existência de outliers
        q1 = session_state.df_set['Playlists Plays'].quantile(0.25)
        q3 = session_state.df_set['Playlists Plays'].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Adiciona análise textual abaixo do plot
        min_value = session_state.df_set['Playlists Plays'].min()
        max_value = session_state.df_set[session_state.df_set['Playlists Plays'] <= upper_bound]['Playlists Plays'].max()
        outliers = session_state.df_set[
            (session_state.df_set['Playlists Plays'] < lower_bound) | (session_state.df_set['Playlists Plays'] > upper_bound)
        ]

        analysis_text = f'<h5 style="text-align: center;">As Playlists Plays do set variam de <br>{int(min_value)} ➖até➖ {int(max_value)}</h5>'
        
        
        if not outliers.empty:
            analysis_text = f'<h5 style="text-align: center;">Quase 100% do set tem Playlists Plays variando de <br><br><strong style="background-color: white; padding-inline:5px; border-radius: 5px; color: #4a7379;">{int(min_value)} a {int(max_value)}</strong></h5>'
            analysis_text += '<p style="text-align: center;">No entanto, existem algumas faixas que são <strong>consideravelmente mais tocadas</strong> do que a média do set. São elas: <br>'
                        
            outlier_info = [f"{artista} - {nome} ({remix}) ({plays} plays)" if pd.notna(remix) else f"{artista} - {nome} ({plays} plays)" for artista, nome, remix, plays in zip(outliers['Artista'], outliers['Nome'], outliers['Remix'], outliers['Playlists Plays'])]

            analysis_text += f"{', '.join(outlier_info)}</p>"
        else:
            analysis_text = f'<h5 style="text-align: center;">O set tem Playlists Plays variando de <br><strong>{int(min_value)} a {int(max_value)}</strong> Plays </h5>'


        # Adiciona análise textual estilizada
        st.markdown(
            f'<div style="background-color: #a9babd; border-radius: 5px; padding: 10px; margin-top: 20px;">{analysis_text}</div>',
            unsafe_allow_html=True
        )

def show_set_order(session_state):
    # Ordenar o DataFrame pelo 'Track Position'
    df_sorted = session_state.df_set.sort_values('Track Position')

    # Criar uma figura e eixos
    fig, ax = plt.subplots(figsize=(10, 6))

    # Adicionar uma linha para cada música no set
    line = ax.plot(df_sorted['Track Position'], df_sorted['Playlists Plays'], marker='o', label='Playlists Plays')[0]

    # Preencher a área sob a linha com um azul clarinho
    ax.fill_between(df_sorted['Track Position'], df_sorted['Playlists Plays'], color='lightblue', alpha=0.4)

    # Configurar rótulos no eixo x
    positions = [0, len(session_state.df_set) // 2, len(session_state.df_set)]
    labels = ['Inicio Set', 'Metade Set', 'Fim Set']
    ax.set_xticks(positions)
    ax.set_xticklabels(labels)

    # Configurar rótulos e título
    ax.set_xlabel('Posição da Música no Set')
    ax.set_ylabel('Playlists Plays')
    ax.set_title('Playlists Plays em Função da Posição da Música no Set')

    # Adicionar legenda
    ax.legend()

    # Exibir o gráfico
    st.pyplot(fig)

def show_remix_analytics(session_state):
    # Contar a ocorrência de valores na coluna 'Remix'
    contagem_remix = session_state.df_set['Remix'].notna().sum()
    contagem_nao_remix = len(session_state.df_set) - contagem_remix

    # Criar uma lista de contagens
    contagens = [contagem_remix, contagem_nao_remix]

    # Rótulos para as categorias
    rotulos = ['Remix', 'Original Mix']

    # Gráfico 1: Pizza remix
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # Ajuste a altura conforme necessário
    axs[0].pie(contagens, labels=rotulos, autopct='%1.1f%%', colors=['darkgreen', 'lightgreen'])
    axs[0].set_title('Porcentagem de Remix vs. Não Remix')

    # Gráfico 2: Gráfico de Barras
    session_state.df_set['Group'] = np.where(session_state.df_set['Remix'].isna(), 'Not Remix', 'Remix')
    sns.barplot(x=session_state.df_set['Nome'], y='Playlists Plays', hue='Group', data=session_state.df_set, palette={'Not Remix': 'lightgreen', 'Remix': 'darkgreen'}, dodge=False, ax=axs[1])
    axs[1].set_xticks(session_state.df_set['Nome'])
    axs[1].figure.autofmt_xdate(rotation=45)
    axs[1].set_xlabel('Linhas')
    axs[1].set_ylabel('Remixes no set (visualmente)')
    axs[1].set_title('Gráfico de Barras com Cores por Grupo')

    plt.tight_layout()  # Ajusta o layout para evitar sobreposição
    st.pyplot(fig)
 
# def show_artists_analytics(session_state):
#         mais_frequentes = more_frequent_artists(session_state)
#         # Criando subplots com 1 linha e 2 colunas
#         fig, axes = plt.subplots(1, 2, figsize=(12, 5))

#         # Gráfico 1: Artistas com mais de 1 ocorrência
#         sns.barplot(x=mais_frequentes.index, y=mais_frequentes.values, palette='viridis', ax=axes[0])
#         axes[0].set_title('Artistas com mais de 1 ocorrência no set')
#         axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45, ha='right')
#         axes[0].set_xlabel('Artista')
#         axes[0].set_ylabel('Contagem de Ocorrências')
        
#         # Gráfico 2: Contagem de Remix e Não Remix
#         unique_values = session_state.df_set['Remix'].unique()
#         palette = {value: f'C{i}' for i, value in enumerate(unique_values)}
#         sns.countplot(data=session_state.df_set, x='Remix', palette=palette, ax=axes[1])
#         axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha='right')
#         axes[1].set_ylabel('Artistas Remixes')
#         axes[1].set_title('Contagem de Remix e Não Remix')
#         axes[1].set_title('')
        
#         st.pyplot(fig)

def show_artists_analytics(session_state):
    mais_frequentes = more_frequent_artists(session_state)
    
    # Criando uma paleta de tons de vermelho mais escuros
    red_palette = sns.color_palette("Reds", n_colors=len(mais_frequentes))

    # Criando subplots com 1 linha e 2 colunas
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Gráfico 1: Artistas com mais de 1 ocorrência
    sns.barplot(x=mais_frequentes.index, y=mais_frequentes.values, palette=red_palette, ax=axes[0])
    axes[0].set_title('Artistas com mais de 1 ocorrência no set')
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45, ha='right')
    axes[0].set_xlabel('Artista')
    axes[0].set_ylabel('Contagem de Ocorrências')

    # Gráfico 2: Contagem de Remix e Não Remix
    unique_values = session_state.df_set['Remix'].unique()
    red_palette_remix = sns.color_palette("Reds", n_colors=len(unique_values))
    sns.countplot(data=session_state.df_set, x='Remix', palette=red_palette_remix, ax=axes[1])
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha='right')
    axes[1].set_ylabel('Artistas Remixes')
    axes[1].set_title('Contagem de Remix e Não Remix')

    st.pyplot(fig)
       
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
        <div style="display: flex; justify-content: center;">
            <span style="box-shadow: 3px 3px 3px 0px rgba(0, 0, 0, 0.2); border-radius: 5px; padding-inline: 5px;">A média de Playlists Plays nesse set é de {session_state.text_ppmean} Plays.</span>
        </div>
    """
    st.markdown(list_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<h6 style="color: darkgrey; text-align: center;">Tracks mais famosas (com base nos Playlists Plays):<h6>',unsafe_allow_html=True)
    
    for track, plays in zip(session_state.top_tracks, session_state.top_plays):
        # Use a função quote para codificar o nome da faixa para URL
        track_yt_url = quote(track)
        
        # Crie a URL do YouTube
        url = f'https://www.youtube.com/results?search_query={track_yt_url}'

        # Crie o texto Markdown com o link e estilo CSS para centralizar horizontalmente
        markdown_text = f"""
            <div style="text-align: center;">
                <a href="{url}" style="display: inline-block; text-decoration: none; color: #4a7379; background-color: #d0d0d0; border-radius: 5px; margin: 5px; padding-inline: 5px;">▶️ {track}</a><span> {plays}</span>
            </div>
        """

        # Renderize usando st.markdown
        st.markdown(markdown_text, unsafe_allow_html=True)

def get_all_tracks_names_with_links(session_state):
    # Criar uma lista para armazenar as faixas do cluster mais alto
    tracks = []

    # Iterar sobre as linhas do DataFrame
    for index, row in session_state.displayable_df_set.iterrows():
        # Use a função quote para codificar o nome da faixa para URL
        track_yt_url = quote(f"{row['Artista']} - {row['Nome']} {row['Remix']}")

        # Crie a URL do YouTube
        url = f'https://www.youtube.com/results?search_query={track_yt_url}'

        # Crie o texto Markdown com o link e estilo CSS para centralizar horizontalmente
        link_text = f'<a href="{url}" target="_blank" style="color: inherit; text-decoration: none;">{row["Artista"]} - {row["Nome"]} ({row["Remix"]}) ({int(row["Playlists Plays"])} Plays)</a>'

        # Adicionar à lista
        tracks.append(link_text)

    # Exibir a lista
    return tracks

def show_dataframe(session_state):
    # session_state.displayable_df_set['Nome'] = session_state.displayable_df_set.apply(lambda row: get_all_tracks_names_with_links(row), axis=1)
    st.dataframe(session_state.displayable_df_set)
  
def list_all_songs(session_state):
    for track, plays in zip(session_state.all_tracks, session_state.all_plays):
        # Use a função quote para codificar o nome da faixa para URL
        track_yt_url = quote(track)
        
        # Crie a URL do YouTube
        url = f'https://www.youtube.com/results?search_query={track_yt_url}'

        # Crie o texto Markdown com o link e estilo CSS para centralizar horizontalmente
        markdown_text = f"""
            <div style="text-align: center;">
                <a href="{url}" style="display: inline-block; text-decoration: none; color: #4a7379; background-color: #d0d0d0; border-radius: 5px; margin: 5px; padding-inline: 5px;">▶️{track}</a><span> {plays}</span>
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
