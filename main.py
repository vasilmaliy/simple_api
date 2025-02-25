from flask import Flask, request, jsonify
import os
import random
import time  # Додано імпорт модуля time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import Optional, Tuple

app = Flask(__name__)

BASE_DIR = os.path.realpath(os.path.dirname(__file__))


def get_header() -> dict:
    """Генерує випадкові HTTP-заголовки"""
    headers = [
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Referer": "https://www.google.com/"
        },
        # ... інші заголовки
    ]
    return random.choice(headers)


def get_x_page_with_selenium(url: str) -> Tuple[Optional[str], int]:
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
        return driver.page_source, 200
    except Exception as e:
        print(f"Selenium помилка: {e}")
        return f"Помилка: {str(e)}", 500
    finally:
        if driver:
            driver.quit()


@app.route('/scrape', methods=['POST'])
def scrape_page():
    """Обробник POST-запитів для скрапінгу сторінок"""
    url = request.args.get('url')

    if not url:
        return jsonify({"error": "Відсутній параметр URL"}), 400

    if not url.startswith(('http://', 'https://')):
        return jsonify({"error": "Невірний формат URL"}), 400

    html, status_code = get_x_page_with_selenium(url)
    return html, status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)