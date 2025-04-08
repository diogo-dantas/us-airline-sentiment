from wordcloud import WordCloud, STOPWORDS
import streamlit as st
import pandas as pd  
import numpy as np
import plotly.express as px
import ast
import matplotlib.pyplot as plt


# Dataset utilizado para este projeto: https://www.kaggle.com/crowdflower/twitter-airline-sentiment

st.title('Análise de Sentimentos de Tweets sobre Companhias Aéreas')
st.sidebar.title('Análise de Sentimentos de Tweets sobre Companhias Aéreas')
st.markdown(" Este projeto tem como objetivo analisar sentimentos de tweets sobre companhias aéreas utilizando o Streamlit. ✈️ ")

DATA_URL = ('Tweets.csv')

@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    data['airline_sentiment'] = data['airline_sentiment'].map({'positive': 'positivo', 'negative': 'negativo', 'neutral': 'neutro'})
    return data

data = load_data()

st.sidebar.markdown(f"Este dataset contém {data.shape[0]} linhas e {data.shape[1]} colunas.")

st.sidebar.subheader('Mostrando tweets aleatórios:')
random_tweet = st.sidebar.radio('Selecione o tweet com base no tipo de sentimento:', ('positivo', 'neutro', 'negativo'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0, 0])

st.sidebar.markdown('### Número de tweets por sentimento')
select = st.sidebar.selectbox('Selecione o tipo de visualização:', ['Barplot', 'Pie Chart'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentimento': sentiment_count.index, 'Quantidade': sentiment_count.values})

if not st.sidebar.checkbox('Ocultar', True):
    st.markdown('### Número de tweets por sentimento')
    if select == 'Barplot':
        fig = px.bar(sentiment_count, 
                     x='Sentimento', 
                     y='Quantidade', 
                     color='Sentimento', 
                     height=500,
                     color_discrete_map={'positivo': '#00aa67', 'negativo': '#f55658', 'neutro': '#9074ff'})
        fig.update_layout(
            #showlegend=False,
            yaxis=dict(
                showgrid=False,    # Remove as linhas de grade do eixo Y
                range=[0, 10000],  # Define o intervalo do eixo Y
                dtick=2500,
            ),
            xaxis= dict(showticklabels=False),
            xaxis_title="Tipo de Sentimento",   # Novo título para o eixo x
            yaxis_title="Número de Ocorrências",  # Novo título para o eixo y
            legend_title="Categoria de Sentimento",  # Novo título para a legenda
            legend_title_font_size=14,
            legend_font_size=14,
            legend=dict(title="Sentimentos", x=0.8, y=1),  # Alterando a posição da legenda (opcional)
            title="Distribuição dos Sentimentos"  # Título do gráfico
            )
        fig.update_traces(hovertemplate='Quantidade: %{y}',
                          hoverlabel_font_size=16)

        st.plotly_chart(fig)

    else:
        fig = px.pie(sentiment_count,
                     values='Quantidade',
                     names='Sentimento',
                     color='Sentimento',
                     color_discrete_map={'positivo': '#00aa67', 'negativo': '#f55658', 'neutro': '#9074ff'})
        fig.update_layout(legend_font_size=14)

        fig.update_traces(textfont=dict(size=16,color='white'))

        fig.update_traces(hovertemplate='Quantidade: %{value}',
                          hoverlabel_font_size=16)
         
        st.plotly_chart(fig)
    
st.sidebar.subheader('Quando e onde os tweets foram enviados?')
hour = st.sidebar.slider('Selecione a hora:', 0, 23)
# hour = st.sidebar.number_input('Hora do dia:', min_value=0,max_value=23)
modified_data = data[data['tweet_created'].dt.hour == hour]

modified_data['tweet_coord'] = modified_data['tweet_coord'].fillna('[]')  # substituir NaN por uma lista vazia
modified_data['lat'] = modified_data['tweet_coord'].apply(lambda x: ast.literal_eval(x)[0] if x != '[]' else None)
modified_data['lon'] = modified_data['tweet_coord'].apply(lambda x: ast.literal_eval(x)[1] if x != '[]' else None)
modified_data_map = modified_data.dropna(subset=['lat', 'lon'])

if not st.sidebar.checkbox('Ocultar', True, key='2'):
    st.markdown('### Mapa de Tweets ao longo do dia')
    st.markdown('%i tweets entre %i:00 e %i:00' % (len(modified_data), hour, (hour+1)%24))
    if len(modified_data_map) == 0:
        st.write("Sem tweets com localização disponível.")
    elif len(modified_data_map) < len(modified_data) * 0.1:  # Less than 10% of data has coordinates
        st.markdown(f"**Consideração:** *Somente {len(modified_data_map)} de {len(modified_data)} tweets ({len(modified_data_map)/len(modified_data)*100:.1f}%) tem dados de localização disponíveis. Portanto, o mapa pode não ser preciso.*")

    st.map(modified_data_map)
    if st.sidebar.checkbox('Mostrar dados tabulares'):
        st.write(modified_data)

st.sidebar.subheader('Detalhamento de tweets de companhias aéreas por sentimento')
choice = st.sidebar.multiselect('Selecione as companhias aéreas:', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key='0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    color_map = {'positivo': '#00aa67', 'negativo': '#f55658', 'neutro': '#9074ff'}
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment',
                               facet_col='airline_sentiment', labels={'airline_sentiment': 'Sentimentos'}, height=600, width=800,
                               color_discrete_map=color_map)
    fig_choice.update_layout(
        xaxis_title="Companhia Aérea",
        yaxis_title="Número de Ocorrências",
        legend_title="Sentimentos",
        legend_title_font_size=14,
        legend_font_size=14,
        legend=dict(title="Sentimentos", x=0.8, y=1),
        title="Distribuição dos Sentimentos por Companhia Aérea",
        showlegend=False
    )
    fig_choice.update_traces(hovertemplate='Quantidade: %{y}',
                              hoverlabel_font_size=16)
    
    st.plotly_chart(fig_choice)

st.sidebar.header('Nuvem de palavras')
word_sentiment = st.sidebar.radio('Selecione o sentimento:', ('positivo', 'negativo', 'neutro'))

if not st.sidebar.checkbox('Ocultar', True, key='3'):
    st.header('Nuvem de palavras para %s sentimentos' % (word_sentiment))
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS,
                          background_color='white',
                          width=800,
                          height=640
                          ).generate(processed_words)
    wordcloud.to_file('wordcloud.png')
    st.image('wordcloud.png', width=700)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    plt.show()


