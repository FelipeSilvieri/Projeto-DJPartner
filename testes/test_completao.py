import requests
from bs4 import BeautifulSoup
import pandas as pd
from test import get_dj_data

# Função para extrair dados de um DJ
# def extract_dj_data(dj_url):
#     response = requests.get(dj_url)
#     if response.status_code == 200:
#         html_content = response.text
#         soup = BeautifulSoup(html_content, 'html.parser')

#         # Encontrar o elemento do gráfico (pode precisar de ajustes dependendo da estrutura da página)
#         chart_element = soup.find('div', {'data-drupal-selector-chart': 'top100-charts-dj-position-chart-line'})

#         if chart_element:
#             chart_data = chart_element.get('data-chart')
#             # Aqui você precisa processar o JSON em chart_data para obter os valores de data e year
#             # Exemplo: chart_data = json.loads(chart_data)
#             data = [42, 15, 8, 10, 10, 7, 9, 11, 10, 9, 10, 7, 8]  # Substitua isso pelos valores reais
#             year = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
#             dj_name = dj_url.rsplit('/', 1)[-1]
            
#             return {'dj':dj_name, 'position': data, 'year': year}
#         else:
#             print(f"Gráfico não encontrado para o DJ: {dj_url}")
#             return None
#     else:
#         print(f"Falha na solicitação para o DJ: {dj_url}. Código de status: {response.status_code}")
#         return None

# URL da página principal
url = 'https://djmag.com/top100djs'

# Enviar uma solicitação GET para a página
response = requests.get(url)

# Verificar se a solicitação foi bem-sucedida (código de status 200)
if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Encontrar o div com id 'views-bootstrap-top-100-dj-djs-grid'
    parent_div = soup.find('div', {'id': 'views-bootstrap-top-100-dj-djs-grid'})

    # Verificar se o elemento foi encontrado
    if parent_div:
        # Encontrar todas as tags <a> que não têm filhos
        dj_urls = [f"https://djmag.com{a.get('href')}" for a in parent_div.find_all(lambda tag: tag.name == 'a' and not tag.find_all())]

        # Criar um DataFrame vazio
        df = pd.DataFrame()

        # Iterar sobre os DJs
        for dj_url in dj_urls:
            dj_data = get_dj_data(dj_url)
            if dj_data:
                # Adicionar dados ao DataFrame
                df = pd.concat([df, pd.DataFrame(dj_data)], ignore_index=True)

        # Exibir o DataFrame
        print(df)

        # Exportar para CSV
        df.to_csv('dados_djs.csv', index=False)

    else:
        print("Elemento pai não encontrado.")
else:
    print(f"Falha na solicitação. Código de status: {response.status_code}")
