from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize

from time import sleep
import random
import glob
import pandas as pd
import re
import time

class Bot():  
    def __init__(self) -> None:
        servico = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = "A:\Program Files\Google\Chrome\Application\Chrome.exe"
        chrome_options.add_argument("--headless")
        self.navegador = webdriver.Chrome(service=servico,options=chrome_options)
        self.navegador.get('https://www.1001tracklists.com/')
        self.setlists = pd.DataFrame()
    
    def search(self,artist):
        input_artist = self.navegador.find_element(By.XPATH,'//*[@id="sBoxInput"]')
        input_artist.send_keys(artist)
        
    def submit(self):
        search_button = self.navegador.find_element(By.XPATH,'//*[@id="sBoxBtn"]')
        search_button.click()
        
    def checks(self):
        soundcloud = self.navegador.find_element(By.XPATH,'//*[@id="left"]/div[3]/div[5]/label[1]')
        youtube = self.navegador.find_element(By.XPATH,'//*[@id="left"]/div[3]/div[5]/label[2]')
        livesets = self.navegador.find_element(By.XPATH,'//*[@id="left"]/div[3]/div[9]/label[2]')
        search = self.navegador.find_element(By.XPATH,'//*[@id="left"]/div[3]/div[10]/button')
        soundcloud.click()
        sleep(.5)
        youtube.click()
        sleep(.6)
        livesets.click()
        sleep(.8)
        search.click()
        sleep(1)

    def list_sets(self):
        names = []
        links = []
        dates = []
        genres = []
        setsizes = []
        
        self.sets = self.navegador.find_elements(By.CLASS_NAME, 'bItm.action.oItm')
        
        for set in self.sets:            
            # Pegando Link
            link_element = set.find_element(By.XPATH, './/div[@class="bTitle"]/a')
            href_content = (link_element.get_attribute('outerHTML'))
            match = re.search(r'href="([^"]+)"', href_content)
            if match:
                href_value = match.group(1)
                link = f'https://www.1001tracklists.com{href_value}'
            else:
                link = ''
            links.append(link)
            # --------------------
            
            # Pegando Nome
            name = link_element.text
            names.append(name)
            # --------------------
            
            # # Pegando Data
            date_element = set.find_element(By.XPATH,'.//div[@title="tracklist date"]')
            date = date_element.text
            dates.append(date)
            # # --------------------
            
            # # Pegando Gênero
            genre_element = set.find_element(By.XPATH,'.//div[@title="musicstyle(s)"]')
            genre = genre_element.text
            genres.append(genre)
            # # --------------------
            
            # # Pegando Tamanho set
            setsize_element = set.find_element(By.XPATH,'.//div[@title="IDed tracks / total tracks"]')
            setsize = setsize_element.text
            setsizes.append(str(setsize))
            # # --------------------
            
        
        self.setlists['name'] = names
        self.setlists['link'] = links
        self.setlists['date'] = dates
        self.setlists['date'] = pd.to_datetime(self.setlists['date'])
        self.setlists['genre'] = genres
        self.setlists['setsize'] = setsizes

        # Separar os valores da coluna 'setsize'
        def get_identificados(row):
            partes = row.split('/')
            if 'all' in partes[0]:
                return partes[1], partes[1]
            else:
                return partes[0], partes[1]
        
        
        # Aplicar a função à coluna 'setsize'
        self.setlists[['tracks_identificadas', 'qtd_tracks']] = self.setlists['setsize'].apply(get_identificados).apply(pd.Series)

        # Remover a coluna 'setsize' original
        self.setlists = self.setlists.drop('setsize', axis=1)
          
    def export_to_csv(self,artist):
        artist_name = artist.replace(' ', '_')
        artist_name = artist_name.lower()
        self.setlists.to_csv(f'artists_sets/{artist_name}.csv', index=False)
        
    def get_charts(self,year,week):
        self.navegador.get(f'https://www.1001tracklists.com/charts/weekly/{year}/{week}/index.html')
        self.tracks = self.navegador.find_elements(By.CLASS_NAME, 'bItm.oItm, bItm.oItm.con')
        
        artistas = []
        nomes = []
        crescimentos = []
        suportes = []
        links = []       
        dataframe = pd.DataFrame()
        
        for div in self.tracks:
            # Aguardar até que o elemento de nome da track seja visível
            nome_track_element = div.find_element(By.XPATH, './/div[@class="fontL"]/a')
            
            try:
                crescimento_div = div.find_element(By.XPATH, './/div[@class="bPlay"]/div[@class="greenTxt"] | .//div[@class="bPlay"]/div[@class="redTxt"] | .//div[@class="bPlay"]/div[@class="blueTxt"]')
                # # Pegar o valor atribuído ao crescimento da track
                # crescimento_div = div.find_element(By.XPATH, './/div[@class="bPlay"]/div[@class="bRank"]')
                crescimento_valor = crescimento_div.text
                if crescimento_valor[0] == '+':
                    # Remover o primeiro caractere
                    crescimento_valor = crescimento_valor[1:]
                crescimento_valor = int(crescimento_valor)
            except:
                crescimento_valor = 'New or Nonchange'
            
            support = div.find_element(By.XPATH, './/div[@class="ml5"]/div[@class="mt5"]/span[@class="badge playC iB spL"]')
            support_text = support.text
            
            # Pegar o nome da track
            nome_track = nome_track_element.text
            track_link = nome_track_element.get_attribute('href')
            
            # Dividir a string usando o caractere '-'
            partes = nome_track.split('-')

            # Remover espaços em branco adicionais ao redor das partes
            artista = partes[0].strip()
            nome_musica = partes[1].strip()

            # Imprimir as informações coletadas
            print(f"Artista(s):{artista} ; Nome Música: {nome_musica} ; crescimento: {crescimento_valor} ; suporte: {support_text} ; link: {track_link}")
            
            artistas.append(artista)
            nomes.append(nome_musica)
            crescimentos.append(crescimento_valor)
            suportes.append(support_text)
            links.append(track_link)            

        dataframe['Artista(s)'] = artistas
        dataframe['Nome Música'] = nomes
        dataframe['Crescimento'] = crescimentos
        dataframe['Suporte'] = suportes
        dataframe['Links'] = links
        
        dataframe.to_csv(f'charts_{year}_{week}.csv', index=False)
        return(dataframe)
    
    def gera_grafico(self,qtd_tracks,inicio,fim):
        
        # Lista para armazenar os DataFrames de cada semana
        dfs = []

        # Lista de arquivos CSV que você deseja juntar
        arquivos_csv = [f'charts/charts_2023_{i:02d}.csv' for i in range(inicio, fim)]

        # Lê cada arquivo CSV e armazena em uma lista de DataFrames
        for arquivo in arquivos_csv:
            df = pd.read_csv(arquivo)
            dfs.append(df)

        # Concatena todos os DataFrames em um único DataFrame
        df_final = pd.concat(dfs, ignore_index=True)

        # Agrupa por nome da música e nome dos artistas
        df_final_agrupado = df_final.groupby(['Nome Música', 'Artista(s)']).agg({
            'Suporte': 'mean',
            'Links': 'first'  # Assume que o valor do link é o mesmo para todas as entradas do mesmo grupo
        }).reset_index()
        
        df_final_agrupado['Suporte'] = df_final_agrupado['Suporte'].round().astype(int)
        # Salva o DataFrame final em um novo arquivo CSV
        df_final_agrupado.to_csv(f'graphs/grafico_{inicio}_{fim}_{qtd_tracks}.csv', index=False)
        
        # --------------------------------------------------------------------------------------
        
        charts_total = pd.read_csv(f'graphs/grafico_{inicio}_{fim}_{qtd_tracks}.csv')
        charts_total = charts_total.sort_values(by='Suporte',ascending=False).reset_index()
        charts_total = charts_total.drop('index',axis=1)
        
        # Selecione as primeiras 20 tracks do DataFrame 'charts_total'
        df_primeiras_x_tracks = charts_total.head(qtd_tracks)

        # Normalizar os valores para o intervalo [0, 1]
        norm = Normalize(vmin=df_primeiras_x_tracks['Suporte'].min(), vmax=df_primeiras_x_tracks['Suporte'].max())

        # Escolher um colormap, por exemplo, 'viridis'
        cmap = cm.viridis

        # Criar o gráfico de barras com cores variadas
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.bar(
            [f'{artista} - {musica}' for artista, musica in zip(df_primeiras_x_tracks['Artista(s)'], df_primeiras_x_tracks['Nome Música'])],
            df_primeiras_x_tracks['Suporte'],
            color=cmap(norm(df_primeiras_x_tracks['Suporte']))
        )
        # bars = ax.bar(df_primeiras_x_tracks['Nome Música'], df_primeiras_x_tracks['Suporte'], color=cmap(norm(df_primeiras_x_tracks['Suporte'])))

        # Adicionar rótulos e título
        ax.set_xlabel('Nome da Música')
        ax.set_ylabel('Suporte')
        ax.set_title('Suporte por Música')

        # Rotacionar os rótulos no eixo x para melhor ajuste
        plt.xticks(rotation=90, ha='center')

        # Adicionar barra de cores
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm)

        # Adicionar valores nas barras
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

        # Exibir o gráfico
        plt.tight_layout()
        plt.show()

    def lista_tracks(self,artist,set):
        artistas = []
        nomes = []
        gravadoras = []
        playlist_plays_array = []
        track_positions = []
        remixes = []
        df = pd.DataFrame()
        
        set_number = set
        artist_df = pd.read_csv(f'artists_sets/{artist.lower()}.csv')
        set_link = artist_df.loc[set-1,'link']
        set_name = artist_df.loc[set-1,'name']
        nome_limpo = re.sub(r'[\/:*?"<>|]', '-', set_name)
        nome_limpo = nome_limpo.lower()
        str_set = str(set_link)
        print(str_set)
        self.navegador.get(str_set)
        sleep(1)
        sets = self.navegador.find_elements(By.CSS_SELECTOR, ".tlpTog.bItm.tlpItem")
        for set in sets:
            try:
                artista = set.find_element(By.XPATH, './/div[@class="bCont tl"]//*[@itemprop="tracks"]/span[contains(@class, "trackValue notranslate")]/span[contains(@class, "notranslate")]').text.strip()
            except:
                artista = 'n/a'
            artistas.append(artista)
            
            try:
                nome = set.find_element(By.XPATH, './/div[@class="bCont tl"]//*[@itemprop="tracks"]/span[contains(@class, "trackValue notranslate")]/span[@class = "blueTxt"]/span[@class = "notranslate"]').text.strip()
            except:
                nome = 'n/a'
            nomes.append(nome)
            
            try:
                gravadora = set.find_element(By.XPATH, './/div[@class="bCont tl"]//*[@itemprop="tracks"]/span[contains(@class, "iBlock")]/span[contains(@class, "trackLabel blueTxt")]').text.strip()
            except:
                gravadora = 'n/a'
            gravadoras.append(gravadora)
 
            try:
                playlist_plays = set.find_element(By.XPATH, './/div[@class="bCont tl"]//div[@class="wRow halfOpacity mt5"]/span[@class="badge playC"]/span').text.strip()
            except:
                playlist_plays = 'n/a'
            playlist_plays_array.append(playlist_plays)
            
            try:
                remix = set.find_element(By.XPATH, './/div[@class="bCont tl"]//*[@itemprop="tracks"]/span[contains(@class, "trackValue notranslate")]/span[@class = "notranslate"]/span[@class = "blueTxt"]').text.strip()
                remix_2 = set.find_element(By.XPATH, './/div[@class="bCont tl"]//*[@itemprop="tracks"]/span[contains(@class, "trackValue notranslate")]/span[@class = "notranslate"]/span[@class = "remixValue blueTxt"]').text.strip()
                remix = str(remix) + ' ' + str(remix_2)
            except:
                remix = 'n/a'
            remixes.append(remix)
                
            track_position = set.find_element(By.XPATH, './/div[@class="bPlay"]/span[@class="fontXL"]').text.strip()
            track_positions.append(track_position)
            
            
            print(f'{artista} - {nome} [{gravadora}]\nPlays: {playlist_plays}')
        
        set_tracks = artist_df.loc[set_number-1,'qtd_tracks']

        df['Artista'] = artistas
        df['Nome'] = nomes
        df['Label'] = gravadoras
        df['Playlists Plays'] = playlist_plays_array
        df['Track Position'] = track_positions
        df['Remix'] = remixes
        df.to_csv(f'artists/{artist}_{set_number-1}.csv', index=False)
    
    def get_artist_sets(self,artist):
         
        self.search(artist)  
        sleep(2)
        self.submit()
        sleep(2)
        # bot.checks()
        sleep(2)
        self.list_sets()
        self.export_to_csv(artist)
        
    def get_artist_set_tracks(self,artist,set):
        artist_lista_tracks = artist.lower()
        artist_lista_tracks = artist_lista_tracks.replace(' ', '_')
        print(artist_lista_tracks)
        self.lista_tracks(artist_lista_tracks,int(set)+1)

bot = Bot()

# ------------------------- Get Charts ------------------------- #

# year = 2023
# primeira_semana = 24
# ultima_semana = 52
# weeks = [f'{i:02d}' for i in range(primeira_semana, ultima_semana)]

# for week in weeks:
#     bot.get_charts(year,week)

# bot.gera_grafico(20,5,10)

# -------------------- Get Artist Sets -------------------- #

# bot.search(artist)  
# sleep(2)
# bot.submit()
# sleep(2)
# # bot.checks()
# sleep(2)
# bot.list_sets()
# bot.export_to_csv(artist)

# -------------------- Get Artist Set Tracks -------------------- #

# artist_lista_tracks = artist.lower()
# artist_lista_tracks = artist_lista_tracks.replace(' ', '_')
# print(artist_lista_tracks)


# bot.lista_tracks(artist_lista_tracks,9)

