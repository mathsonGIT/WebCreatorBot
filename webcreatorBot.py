import streamlit as st 
import streamlit.components.v1 as components
from openai import OpenAI
import pandas as pd

AI_Client = OpenAI(
    api_key=st.secrets['OPENAI_KEY'], 
    base_url=st.secrets['OPENAI_URL']
)
def generate_answer(question, prompt):
    messages = []
    messages.append({"role": "system", "content": prompt})
    messages.append({"role": "user", "content": question})
    response = AI_Client.chat.completions.create(
    model="openai/gpt-3.5-turbo", # id модели из списка моделей - можно использовать OpenAI, Anthropic и пр. меняя только этот параметр
    messages=messages,
    temperature=0.7,
    n=1,
    max_tokens=3000, # максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
    extra_headers={ "X-Title": "My App" }, )# опционально - передача информация об источнике API-вызова
    rezult = response.choices[0].message.content
    return(rezult)

df_prompt_rus = pd.read_csv('data/df_prompt_rus2.csv')
with st.sidebar:
    st.title('Бот - ВебКреатор')
    st.image('data/bot.png')
    role = st.selectbox(label = 'Выберите роль', options=df_prompt_rus.act_rus.to_list())
    base_prompt = df_prompt_rus[df_prompt_rus.act_rus == role]['prompt'].to_list()[0]
    st.text_area(label = 'Промпт ответа', value=base_prompt)

question = st.text_area(label = 'Введите запрос', height = 300)
if st.button(label = 'Сгенерировать код'):
    rezult = generate_answer(question, base_prompt)
    if rezult:
        st.write(rezult)
        if role == 'Младший веб-разработчик':
            components.html(rezult, width = 600, height = 600, scrolling=True)
