# Obter o nome do DJ a partir do URL
dj_url = 'https://djmag.com/top100djs/2023/84/Le-Twins' 
dj_name = dj_url.rsplit('/', 1)[-1]

print(dj_name)