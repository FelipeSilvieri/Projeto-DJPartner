import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def center_alignment():
    """
    Função para centralizar o conteúdo horizontalmente.
    """
    st.markdown(
        """
        <style>
            .stApp {
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    # Aplicar centralização
    center_alignment()

    st.title("Gráfico em Streamlit com Matplotlib")

    # Criar dados de exemplo
    dados = {'X': np.arange(0, 10, 1), 'Y': np.random.randn(10)}
    df = pd.DataFrame(dados)

    # Exibir dados em uma tabela
    st.write("Dados:")
    st.write(df)

    # Criar e exibir um gráfico usando Matplotlib
    fig, ax = plt.subplots()
    ax.plot(df['X'], df['Y'])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    st.pyplot(fig)

if __name__ == "__main__":
    main()
