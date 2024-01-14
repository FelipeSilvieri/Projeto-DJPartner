import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


def get_dj_data(url):
    df = pd.DataFrame()
    # Enviar uma solicitação GET para a página
    response = requests.get(url)

    # Verificar se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Obter o conteúdo HTML da página
        html_content = response.text

        # Usar BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Encontrar o elemento pelo atributo 'data-drupal-selector-chart'
        chart_element = soup.find('div', {'data-drupal-selector-chart': 'top100-charts-dj-position-chart-line'})

        # Verificar se o elemento foi encontrado
        if chart_element:
            # Obter o conteúdo do atributo 'data-chart'
            chart_data_str = chart_element.get('data-chart')

            # Analisar o JSON
            chart_data = json.loads(chart_data_str)

            # Extrair os vetores "data" e "year"
            data_vector = chart_data['series'][0]['data']
            year_vector = chart_data['xAxis'][0]['categories']

            df['year'] = year_vector
            df['dj_position'] = data_vector
            df['dj_name'] = url.rsplit('/', 1)[-1]
            # Imprimir os vetores
            print("Vetor 'data':", data_vector)
            print("Vetor 'year':", year_vector)
        else:
            print("Elemento não encontrado.")
    else:
        print(f"Falha na solicitação. Código de status: {response.status_code}")
