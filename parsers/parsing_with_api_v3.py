import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
import time
import datetime
import random
import csv

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument(f'user-agent={UserAgent().random}')
chrome_options.add_experimental_option('prefs', {'javascript_enabled': False})

base_url = "https://www.reuters.com/pf/api/v3/content/fetch/articles-by-search-v2"
params = {
    "query": '{"keyword":"crypto","offset":0,"orderby":"display_date:desc","size":100,"website":"reuters"}',
    "d": 137,
    "_website": "reuters"
}

def login():
    # открытие страницы в браузере
    driver.get('https://www.reuters.com/account/sign-in/')
    # поиск элементов формы
    email_input = driver.find_element(By.NAME, 'email')
    password_input = driver.find_element(By.NAME, 'password')
    submit_button = driver.find_element(By.CSS_SELECTOR, '.sign-in-form__sign-in-btn__2jvFh')

    # заполнение формы
    email_input.send_keys('********')
    password_input.send_keys('******')
    time.sleep(random.uniform(5, 8))
    # отправка формы
    submit_button.click()
    time.sleep(random.uniform(5, 8))

def parsing_paragraph(article, title):
    url = "https://www.reuters.com{}".format(article)
    print(url)
    driver.get(url)
    try:
        paragraphs = driver.find_elements(By.XPATH, '//p[contains(@data-testid,"paragraph-")]')
    except NoSuchElementException:
        print(f"Error: paragraphs not found on page {title}")
        paragraphs = []

    text = "\n".join([el.text.replace(",", "").replace('"', '') for el in paragraphs])
    time.sleep(random.uniform(5, 14))
    return(text)

def process_articles(articles):
    with open('test_new.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Headline', 'Date', 'Timestamp', 'Text'])
        for article in articles:
            article_id = article['id']
            canonical_url = article['canonical_url']
            title = article['title']
            published_time = article['published_time']

            # Преобразование 
            dt = datetime.datetime.fromisoformat(published_time.replace("Z", "+00:00"))
            date = dt.strftime('%Y-%m-%d %H:%M:%S')

            text = parsing_paragraph(canonical_url, title)
            print(f"ID: {article_id}\nURL: {canonical_url}\nTitle: {title}\nPublished time: {published_time}\nTimestamp: {date}\nText: {text}")
            writer.writerow([title, published_time, date, text])

# Инициализация драйвера
# driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
driver = webdriver.Chrome()
login()
for offset in range(0, 2500, 100):
    params["query"] = json.dumps({"keyword": "crypto", "offset": offset, "orderby": "display_date:desc", "size": 100, "website": "reuters"})
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        articles = data['result']['articles']
        process_articles(articles)
    else:
        print(f"Error {response.status_code}: {response.text}")
driver.quit()