import streamlit as st 
import streamlit.components.v1 as components
from utils import generate_answer, cyberleninka_search, search_text_DDGS, YandexSearch, Text2ImageAPI, elibrary_search
from pdfreader import read_all_document, download_read_pdf
from openai import OpenAI
import asyncio
import pandas as pd
import requests
import base64
from io import BytesIO

AI_Client = OpenAI(
    api_key=st.secrets['OPENAI_KEY'], 
    base_url=st.secrets['OPENAI_URL']
)
df_prompt_rus = pd.read_csv('data/df_prompt_rus2.csv')
with st.sidebar:
    st.title('Бот - Ученый')
    st.image('data/bot.png')

    role = st.selectbox(label = 'Выберите роль', options=df_prompt_rus.act_rus.to_list())
    #st.write(df_prompt[df_prompt.act == role].prompt[0])
    #st.write(role)
    base_prompt = df_prompt_rus[df_prompt_rus.act_rus == role]['prompt'].to_list()[0]
    #base_prompt = st.text_area(label = 'Начальный промпт', value = _base_prompt)
    option = st.selectbox(
        "Выберите направление исследований",
        ("Простая генерация ответа", "Выбор литературы из Киберленинки и Elibrary", "Список литературы из Интернета", 'Генерация изображения'),
    index=0,
    placeholder="Выберите метод исследования...",
)

if option == "Простая генерация ответа":

    question = st.text_area(label = 'Введите запрос', height = 300)
    if st.button(label = 'Анализ'):
        rezult = generate_answer(question, base_prompt)
        if rezult:
            st.write(rezult)
            if role == 'Младший веб-разработчик':
                components.html(rezult, width = 600, height = 600, scrolling=True)

if option == 'Выбор литературы из Киберленинки и Elibrary':
    question = st.text_area(label = 'Введите запрос')
    if st.button(label = 'Анализ'):
        articles = cyberleninka_search(keywords=question, max_results=10)
        #rezult = asyncio.run(read_all_document(articles))
        st.write('Киберленинка:')
        for article in articles:
            with st.expander(label = article.get('title', 'Без названия')):
                st.text(article.get('href', 'Нет url'))
                #st.text(article.get('annotation', 'нет аннотации'))
        st.write('Elibrary')
        articles = elibrary_search(query=question, max_results=10)
        for article in articles:
            with st.expander(label = article.get('title', 'Без названия')):
                st.text(article.get('href', 'Нет url'))
        
if option == 'Список литературы из Интернета':
    question = st.text_area(label = 'Введите запрос')
    if st.button(label = 'Анализ'):
        st.write('Результаты поискового сервиса DuckDuckGoSearch')
        
        try:
            articles = search_text_DDGS(keywords=question, max_results=5)
            #rezult = asyncio.run(read_all_document(articles))
            for article in articles:
                with st.expander(label = article.get('title', 'Без названия')):
                    st.text(article.get('href', 'url'))
                    #st.text(article.get('annotation', 'нет аннотации'))
        except:
            st.write('DuckDuckGoSearch Error')
        st.divider()
        st.write('Результаты поискового сервиса YandexSearch')
        
        try:
            articles = YandexSearch(folderid=st.secrets['YANDEX_SEARCH_folderid'], apikey=st.secrets['YANDEX_SEARCH_apikey']).search(query=question)
            for article in articles.items:
                with st.expander(label = article.get('title', 'Без названия')):
                    st.text(article.get('url', 'Нет url'))
                    st.text(article.get('snippet', 'нет аннотации'))
            
        except:
            st.write('YandexSearch Error')
        st.divider()
if option == 'Генерация изображения':
    image_prompt = st.text_area(label = 'Начальный промпт для генерации изображений', value = 'Напишите промпт')
    option_model = st.selectbox('Выберите модель для генерации изображений', ("dall-e-2", 'Kandinsky 3.1'),
        index=None,
        placeholder="Модель генерации изображений...",
)

    if st.button(label = 'Генерация изображения'):
        with st.spinner('Идет генерация изображения'):
            if option_model == "dall-e-2":
                response = AI_Client.images.generate(model="dall-e-2", prompt=image_prompt, n=1, size="256x256")
                image_url = response.data[0].url
                image_response = requests.get(image_url)
                with open('generated_image.png', 'wb') as f:
                    f.write(image_response.content)
                st.write(image_response.content)

            if option_model == "Kandinsky 3.1":
                api = Text2ImageAPI('https://api-key.fusionbrain.ai/', st.secrets['SBER_APIKEY'], st.secrets['SBER_SECRETKEY'])
                model_id = api.get_model()
                uuid = api.generate(image_prompt, model_id)
                images = api.check_generation(uuid)
                bites = BytesIO(base64.b64decode(images[0]))
                st.image(bites)
            
                

