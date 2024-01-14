import requests
from bs4 import BeautifulSoup

# URL da página principal
url = 'https://djmag.com/top100djs'

# Enviar uma solicitação GET para a página
response = requests.get(url)

# Verificar se a solicitação foi bem-sucedida (código de status 200)
if response.status_code == 200:
    # Obter o conteúdo HTML da página
    html_content = response.text

    # Usar BeautifulSoup para analisar o HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Encontrar o div com id 'views-bootstrap-top-100-dj-djs-grid'
    parent_div = soup.find('div', {'id': 'views-bootstrap-top-100-dj-djs-grid'})

    # Verificar se o elemento foi encontrado
    if parent_div:
        # Encontrar todas as tags <a> que não têm filhos
        dj_urls = parent_div.find_all(lambda tag: tag.name == 'a' and not tag.find_all())

        # Imprimir os URLs das tags <a> sem filhos
        for dj_url in dj_urls:
            print(dj_url.get('href'))  # Aqui você pode pegar o atributo 'href' ou qualquer outro atributo que desejar
    else:
        print("Elemento pai não encontrado.")
else:
    print(f"Falha na solicitação. Código de status: {response.status_code}")
