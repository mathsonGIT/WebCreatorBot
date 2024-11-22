import streamlit as st 
import streamlit.components.v1 as components
from openai import OpenAI
import pandas as pd
from duckduckgo_search import DDGS

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

#generate answer with duck-duckgo search
def generate_answer_DDGS(question, prompt):
    results = DDGS().chat(f"Ты - {prompt} . Выполни запрос {question}", model='gpt-4o-mini')
    return(results)

st.set_page_config(
    page_title="WebCreatorBot",
    page_icon="👋",
)
#df_prompt_rus = pd.read_csv('data/df_prompt_rus2.csv')
with st.sidebar:
    st.title('Бот - ВебКреатор')
    st.image('data/bot.png')
    st.divider()
    st.subheader('Описание')
    st.markdown("Бот предназначен для генерации html, css, javascript кода на существующую веб-страницу")
    #role = st.selectbox(label = 'Выберите роль', options=df_prompt_rus.act_rus.to_list())
    base_prompt = 'I want you to act as a junior developer of individual interface blocks. I will describe the details of the block that you will code using the following programming languages: html, css, javascript. Do not separate html, css, js, combine all elements into one <div> block in order to insert the resulting code into an existing HTML document. Do not write explanations.'
    
    
    #df_prompt_rus[df_prompt_rus.act_rus == role]['prompt'].to_list()[0]
    #st.text_area(label = 'Промпт ответа', value=base_prompt)

question = st.text_area(label = 'Максимально опишите блок для вставки на веб страницу', height = 300)
if st.button(label = 'Сгенерировать код'):
    try:
        st.write('Duck Duck GO Rezults')
        rezult = generate_answer_DDGS(question, base_prompt)
    except:
        st.write('OPEN AI Rezults')
        rezult = generate_answer(question, base_prompt)
    if rezult:
        st.write(rezult)
        components.html(rezult, width = 600, height = 600, scrolling=True)
