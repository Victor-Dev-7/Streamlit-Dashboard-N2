import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

st.set_page_config(page_title="Pokédex", layout="wide")

def tela_inicial():
    st.markdown("""
        <style>
        .titulo-pokemon {
            font-size: 72px;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            color: #FFCC00;
            text-align: center;
            text-shadow: 2px 2px 5px #000;
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        .button-container button {
            background-color: #FFCC00;
            color: #000;
            border: none;
            padding: 15px 30px;
            font-size: 24px;
            font-family: 'Arial', sans-serif;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 3px 3px 8px #888888;
        }
        .button-container button:hover {
            background-color: #FFD700;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="titulo-pokemon">Pokémon</div>', unsafe_allow_html=True)

    pikachu_image = Image.open('images/pikachu.png')
    st.image(pikachu_image, caption="Pikachu", use_column_width=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Seleção de Pokémon"):
            st.session_state.page = "Seleção de Pokémon"
    with col2:
        if st.button("Comparar Pokémon"):
            st.session_state.page = "Comparar Pokémon"
    with col3:
        if st.button("Dados Gerais"):
            st.session_state.page = "Dados Gerais"

def selecao_pokemon(df):
    st.header("Seleção de Pokémon")
    pokemon_names = sorted(df['name'].unique())
    selected_pokemon = st.selectbox('Escolha um Pokémon:', pokemon_names)
    pokemon_data = df[df['name'] == selected_pokemon].iloc[0]

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        try:
            image_path = f'images/{selected_pokemon.lower()}.png'
            image = Image.open(image_path)
            st.image(image, caption=selected_pokemon, use_column_width=True)
        except:
            st.error(f"Imagem não encontrada para {selected_pokemon}")

    st.header('Informações do Pokémon')

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Número do Pokémon:** {pokemon_data.name}")
        st.write(f"**Tipo:** {pokemon_data['type']}")
        st.write(f"**Espécie:** {pokemon_data['pokemon_species']}")
        st.write(f"**Habilidades:** {pokemon_data['pokemon_abilities']}")
        st.write(f"**Peso:** {pokemon_data['pokemon_weight']}")
        st.write(f"**Altura:** {pokemon_data['pokemon_height']}")

    with col2:
        st.write(f"**Gênero (M/F):** {pokemon_data['pokemon_male']}%/{pokemon_data['pokemon_female']}%")
        st.write(f"**Grupo do Ovo:** {pokemon_data['pokemon_egg']}")

    if st.button("Voltar"):
        st.session_state.page = 'tela_inicial'

def comparar_pokemon(df):
    st.header("Comparar Pokémon")
    pokemon_names = sorted(df['name'].unique())

    col1, col2 = st.columns(2)

    with col1:
        selected_pokemon_1 = st.selectbox('Escolha o primeiro Pokémon:', pokemon_names, key="pokemon1")

    with col2:
        selected_pokemon_2 = st.selectbox('Escolha o segundo Pokémon:', pokemon_names, key="pokemon2")

    pokemon_data_1 = df[df['name'] == selected_pokemon_1].iloc[0]
    pokemon_data_2 = df[df['name'] == selected_pokemon_2].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        try:
            image_path_1 = f'images/{selected_pokemon_1.lower()}.png'
            image_1 = Image.open(image_path_1)
            st.image(image_1, caption=selected_pokemon_1, use_column_width=True)
        except:
            st.error(f"Imagem não encontrada para {selected_pokemon_1}")

    with col2:
        try:
            image_path_2 = f'images/{selected_pokemon_2.lower()}.png'
            image_2 = Image.open(image_path_2)
            st.image(image_2, caption=selected_pokemon_2, use_column_width=True)
        except:
            st.error(f"Imagem não encontrada para {selected_pokemon_2}")

    st.header('Comparação de Status')

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{selected_pokemon_1}")
        st.write(f"**Número do Pokémon:** {pokemon_data_1.name}")
        st.write(f"**Tipo:** {pokemon_data_1['type']}")
        st.write(f"**Espécie:** {pokemon_data_1['pokemon_species']}")
        st.write(f"**Habilidades:** {pokemon_data_1['pokemon_abilities']}")
        st.write(f"**Peso:** {pokemon_data_1['pokemon_weight']}")
        st.write(f"**Altura:** {pokemon_data_1['pokemon_height']}")

    with col2:
        st.subheader(f"{selected_pokemon_2}")
        st.write(f"**Número do Pokémon:** {pokemon_data_2.name}")
        st.write(f"**Tipo:** {pokemon_data_2['type']}")
        st.write(f"**Espécie:** {pokemon_data_2['pokemon_species']}")
        st.write(f"**Habilidades:** {pokemon_data_2['pokemon_abilities']}")
        st.write(f"**Peso:** {pokemon_data_2['pokemon_weight']}")
        st.write(f"**Altura:** {pokemon_data_2['pokemon_height']}")

    st.header("Gráfico de Comparação de Status")

    comparison_data = pd.DataFrame({
        'Atributo': ['Peso', 'Altura'],
        selected_pokemon_1: [pokemon_data_1['pokemon_weight'], pokemon_data_1['pokemon_height']],
        selected_pokemon_2: [pokemon_data_2['pokemon_weight'], pokemon_data_2['pokemon_height']]
    })

    fig = px.bar(comparison_data, x='Atributo', y=[selected_pokemon_1, selected_pokemon_2],
                 barmode='group', title='Comparação de Peso e Altura')
    
    st.plotly_chart(fig)

    if st.button("Voltar"):
        st.session_state.page = 'tela_inicial'

def dados_gerais(df):
    st.header("Dados Gerais da Pokédex")

    st.subheader("Distribuição das Alturas")
    fig_height = px.histogram(df, x="pokemon_height", nbins=30, title="Distribuição de Alturas")
    st.plotly_chart(fig_height)

    st.subheader("Distribuição dos Pesos")
    fig_weight = px.box(df, y="pokemon_weight", title="Distribuição de Pesos")
    st.plotly_chart(fig_weight)

    st.subheader("Quantidade de Pokémon por Tipo")
    type_counts = df['type'].value_counts()
    fig_types = px.pie(type_counts, values=type_counts.values, names=type_counts.index, title="Distribuição de Pokémon por Tipo")
    st.plotly_chart(fig_types)

    st.subheader("Quantidade de Pokémon por Letra Inicial")
    letter_counts = df['name'].str[0].value_counts().sort_index()
    fig_letters = px.bar(letter_counts, x=letter_counts.index, y=letter_counts.values, title="Quantidade de Pokémon por Letra Inicial")
    st.plotly_chart(fig_letters)

    st.subheader("Quantidade de Espécies de Pokémon")
    species_counts = df['pokemon_species'].value_counts()
    fig_species = px.line(species_counts, x=species_counts.index, y=species_counts.values, title="Quantidade de Pokémon por Espécie")
    st.plotly_chart(fig_species)

    if st.button("Voltar"):
        st.session_state.page = 'tela_inicial'

if 'page' not in st.session_state:
    st.session_state.page = 'tela_inicial'

uploaded_files = st.file_uploader("Faça o upload de um ou mais arquivos CSV da Pokédex:", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    dataframes = []
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file, index_col=0)
        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=False)

    if st.session_state.page == 'tela_inicial':
        tela_inicial()
    elif st.session_state.page == 'Seleção de Pokémon':
        selecao_pokemon(combined_df)
    elif st.session_state.page == 'Comparar Pokémon':
        comparar_pokemon(combined_df)
    elif st.session_state.page == 'Dados Gerais':
        dados_gerais(combined_df)
else:
    st.warning("Por favor, faça o upload de um ou mais arquivos CSV.")
