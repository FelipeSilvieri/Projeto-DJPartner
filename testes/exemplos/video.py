import streamlit as st

def embed_youtube_video(video_url):
    """
    Função para incorporar um vídeo do YouTube.
    """
    video_id = video_url.split("v=")[1]
    embed_code = f'<iframe width="671" height="385" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
    st.components.v1.html(embed_code, height=400)

def main():
    st.title("Incorporar Vídeo do YouTube no Streamlit")

    # Inserir o link do vídeo do YouTube
    youtube_url = st.text_input("Insira o link do vídeo do YouTube:")
    
    if youtube_url:
        # Incorporar o vídeo
        embed_youtube_video(youtube_url)

if __name__ == "__main__":
    main()
