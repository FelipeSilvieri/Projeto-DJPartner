# Projeto-DJPartner
Repositório referente ao projeto DJPartner (análise automática de dados de sets de DJS, guiada por WebScraping, Data Engineering | Analytics, DataViz)

----
## Inicializando o App
Para inicializar o app para poder rodar no navegador através da biblioteca "streamlit", será necessário criar um ambiente virtual na raiz do projeto
Execute o comando a seguir para inciar o ambiente virtual:
```
python -m venv venv
```
Depois, ative o mesmo com o comando:
```
venv\Scripts\activate
```

** Obs: se ocorrer um erro de permissão ao executar o script de ativação, execute o seguinte comando:
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
---
## Executando o app.py com streamlit
Após ativado o script do ambiente virtual, é possivel rodar o app.py com streamlit para acessar as funcionalidades pelo navegador:
Execute o seguinte comando **na raiz do projeto**:
```
streamlit run app.py
```
