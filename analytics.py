import pandas as pd
import re
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from urllib.parse import quote

class Analytics:

    def __init__(self, dataset) -> None:
        self.dataframe = pd.read_csv(f'artists/{dataset}.csv')
    
    def tratando_dados(self):
        self.dataframe = self.dataframe.sort_values(by='Playlists Plays', ascending=False)
        self.dataframe = self.dataframe.reset_index(drop=True)
        self.dataframe = self.dataframe[self.dataframe['Track Position'] != 'w/']
        self.dataframe.dropna(subset=['Playlists Plays', 'Artista', 'Nome'], inplace=True)
        self.dataframe = self.dataframe.reset_index(drop=True)
        
        # Dividindo a coluna 'Artista' em uma lista de artistas
        self.dataframe['Artistas Originais'] = self.dataframe['Artista'].apply(lambda x: re.split(r' & | vs. | ft. | feat | feat. | X | x ', x))
        
        # Removendo as palavras reservadas da coluna 'Remix'
        self.dataframe['Artistas Remix'] = self.dataframe['Remix'].str.replace(r'\s*(Remix|Mix|Mashup|Edit|Bootleg|Re-Mix|Re-mix|Deluxe Remix|Deluxe Edit|Deluxe|Vip Remix|Vip Edit|Vip)\s*$', '', regex=True)
        
        # Tratando valores nulos na coluna 'Artistas Remix'
        self.dataframe['Artistas Remix'] = self.dataframe['Artistas Remix'].apply(lambda x: [] if pd.isna(x) else re.split(r' & | vs. | ft. | feat | feat. | X | x ', x))
        
        # Criando a coluna 'Lista Artistas' com a combinação de 'Artistas Originais' e 'Artistas Remix'
        self.dataframe['Lista Artistas'] = self.dataframe.apply(lambda row: [item for sublist in [row['Artistas Originais'], row['Artistas Remix']] if isinstance(sublist, list) for item in sublist], axis=1)
        
        # Exibindo o DataFrame com as colunas adicionadas
        self.dataframe = self.dataframe[['Nome', 'Artista', 'Artistas Originais', 'Remix', 'Artistas Remix', 'Lista Artistas', 'Label', 'Playlists Plays', 'Track Position']]
        
    def get_dataframe(self):
        return self.dataframe
    
    def get_clusters(self):

        # Selecionar as colunas relevantes para a clusterização
        features = self.dataframe[['Playlists Plays']]

        # Padronizar as features (importante para o K-means)
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)

        n_clusters = 3

        # Aplicar o algoritmo K-means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.dataframe['Cluster'] = kmeans.fit_predict(features_scaled)
        
        cluster_means = self.dataframe.groupby('Cluster')['Playlists Plays'].mean().sort_values().index
        mapping = {cluster: i for i, cluster in enumerate(cluster_means)}
        self.dataframe['Cluster'] = self.dataframe['Cluster'].map(mapping)

    def get_highest_cluster(self):
        # Encontrar o número do cluster mais alto
        cluster_mais_alto = self.dataframe['Cluster'].max()

        # Criar uma lista para armazenar as faixas do cluster mais alto
        faixas_cluster_mais_alto = []

        # Iterar sobre as linhas do DataFrame
        for index, row in self.dataframe.iterrows():
            # Verificar se a faixa pertence ao cluster mais alto
            if row['Cluster'] == cluster_mais_alto:
                # Adicionar ('Artista' - 'Nome') à lista
                if pd.notna(row['Remix']):
                    faixas_cluster_mais_alto.append(f"{row['Artista']} - {row['Nome']} ({row['Remix']}) ({int(row['Playlists Plays'])} Plays)")
                else:
                    faixas_cluster_mais_alto.append(f"{row['Artista']} - {row['Nome']} ({int(row['Playlists Plays'])} Plays)")

        # Exibir a lista
        return faixas_cluster_mais_alto

    def get_top_5(self):
        # Ordenar o DataFrame com base nas "Playlists Plays" em ordem decrescente
        sorted_df = self.dataframe.sort_values(by='Playlists Plays', ascending=False)

        # Criar listas para armazenar os dados do artista, nome, remix e plays
        artist_name_remix = []
        plays = []

        # Iterar sobre as top tracks
        for index, row in sorted_df.head(5).iterrows():
            if pd.notna(row['Remix']):
                track_info = f"{row['Artista']} - {row['Nome']} ({row['Remix']})"
            else:
                track_info = f"{row['Artista']} - {row['Nome']}"
            artist_name_remix.append(track_info)
            
            plays_info = f"({int(row['Playlists Plays'])} Plays)"
            plays.append(plays_info)

        return artist_name_remix, plays

    def get_all_tracks_names(self):
        # Ordenar o DataFrame com base nas "Playlists Plays" em ordem decrescente
        sorted_df = self.dataframe.sort_values(by='Playlists Plays', ascending=False)

        # Criar listas para armazenar os dados do artista, nome, remix e plays
        artist_name_remix = []
        plays = []

        # Iterar sobre as top tracks
        for index, row in sorted_df.iterrows():
            if pd.notna(row['Remix']):
                track_info = f"{row['Artista']} - {row['Nome']} ({row['Remix']})"
            else:
                track_info = f"{row['Artista']} - {row['Nome']}"
            artist_name_remix.append(track_info)
            
            plays_info = f"({int(row['Playlists Plays'])} Plays)"
            plays.append(plays_info)

        return artist_name_remix, plays
    
    
