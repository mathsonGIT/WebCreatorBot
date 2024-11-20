from selenium import webdriver
import time
from selenium.webdriver.common.by import By

def elibrary_search(query: str, max_results: int):
    results = list()
    driver = webdriver.Chrome()
    url = 'https://www.elibrary.ru/querybox.asp?scope=newquery'
    driver.get(url)
    ftext = driver.find_element(by=By.NAME, value="ftext")
    elems = driver.find_elements(by=By.CSS_SELECTOR, value="td.menus>a")
    ftext.send_keys(query)
    elems[1].click()
    time.sleep(2)
    articles = driver.find_elements(by=By.CSS_SELECTOR, value='td>span')
    for article in articles:
        ahref = article.find_elements(by=By.TAG_NAME, value='a')
        href = ahref[0].get_attribute('href')
        a = article.text.split('\n')
        title = f'{a[1]} {a[0]} {a[2]}'
        results.append({'title': title, 'href': href})
    driver.quit()
    return(results[:max_results])