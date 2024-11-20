
from pdfminer.high_level import extract_text
import urllib.request
import io
import asyncio
from duckduckgo_search import AsyncDDGS, DDGS
import numpy as np

#request = 'Antitrust Compliance – Assessing Antitrust Risks and Creating an Effective Antitrust Compliance Program'


async def download_read_pdf(article: dict) -> dict:
    #if user_agent == None:
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    headers = {'User-Agent': user_agent}
    #request = urllib.request.Request(url = article['href'], data=None, headers=headers)
    try:
        request = urllib.request.Request(article['href'], data=None, headers=headers)
        open = urllib.request.urlopen(request).read()
        file = io.BytesIO(open)
        text = extract_text(file)
        len_text = len(text)
        indexes = np.round(len_text * np.array([0.15, 0.85]), 0)
        new_text = text[int(indexes[0]): int(indexes[1])]
        try:
            results = await AsyncDDGS().achat(keywords = f'russian summarize {new_text}', model='claude-3-haiku', timeout = 40)
            return({'title': article['title'], 'href': article['href'], 'text': text, 'annotation': results})
        except:
            return({'title': article['title'], 'href': article['href'], 'text': text, 'annotation': 'объемный документ'})
    except:
        return({'title': article['title'], 'href': article['href']})


async def read_all_document(articles: list) -> list:
    tasks = [download_read_pdf(article) for article in articles]
    results = await asyncio.gather(*tasks)
    return results