import requests
import json
import re
from openai import OpenAI
import streamlit as st 
from pdfminer.high_level import extract_text
import urllib.request
import io
import asyncio
from duckduckgo_search import DDGS
from duckduckgo_search import AsyncDDGS

def cyberleninka_search(keywords: str, max_results: int): 
    results = []
    url = 'https://cyberleninka.ru/api/search'
    url_for_link = 'https://cyberleninka.ru'
    headers = {'Content-Type': 'application/json'}
    data = {
        "mode": "articles",
        "size": max_results, 
        "q": keywords
    }
    body = json.dumps(data)
    r = requests.post(url, headers = headers, data = body)
    
    for article in r.json()['articles']:
        authors = ','.join(article['authors']) if article['authors'] else 'Без автора'
        art = re.sub(r'</b>', '', article['name'])
        art = re.sub(r'<b>', '', art)
        res = f"{authors}. {art}. {article['journal']}, {article['year']}"
        href = f"{url_for_link}{article['link']}/pdf"
        
        results.append({'title': res, 'href': href})
    return(results)

def search_text_DDGS(keywords, max_results = 5): 
    results = DDGS().text(keywords = f"{keywords} filetype:pdf", region = 'ru-ru', max_results=max_results)
    res = [{'title': result['title'], 'href': result['href']}  for result in results] 
    return res



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
