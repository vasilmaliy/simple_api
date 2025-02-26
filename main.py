from flask import Flask, request, jsonify
import os
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from typing import Optional

app = Flask(__name__)

BASE_DIR = os.path.realpath(os.path.dirname(__file__))


def get_header() -> dict:
    """Генерує випадкові HTTP-заголовки"""
    headers = [
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Referer": "https://www.google.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "TE": "Trailers"
        },
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/90.0.818.62 Safari/537.36",
            "Referer": "https://www.google.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        },
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
            "Referer": "https://www.google.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "TE": "Trailers"
        },
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.google.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    ]
    return random.choice(headers)


def get_x_page_with_selenium(url: str) -> Optional[str]:
    """Отримує HTML через Selenium з випадковим User-Agent"""
    driver = None
    try:
        chrome_options = Options()
        user_agent = get_header().get("User-Agent")
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        driver.implicitly_wait(random.uniform(5, 11))
        return driver
    except Exception as e:
        print(f"Selenium помилка: {e}")
        driver.quit()
        return f"Помилка: {str(e)}", 500


@app.route('/')
def hello():
    return "Привіт, це твій API сервер!"

@app.route('/scrape', methods=['GET', 'POST'])
def scrape_page():
    """Обробник запитів для отримання вмісту сторінки"""
    url = request.args.get('url') if request.method == 'GET' else request.form.get('url')

    if not url:
        return jsonify({"error": "Відсутній параметр URL"}), 400

    if not url.startswith(('http://', 'https://')):
        return jsonify({"error": "Невірний формат URL"}), 400

    driver = get_x_page_with_selenium(url)
    element = driver.find_element(By.CLASS_NAME, 'css-9pa8cd')

    img = element.get_attribute("src")

    driver.quit()

    return img


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)