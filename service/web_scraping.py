import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; DataBot/1.0)"
}

url = "https://fiis.com.br/vgia11/"
html = requests.get(url, headers=headers).text

soup = BeautifulSoup(html, "html.parser")

div = soup.find("div", class_="yieldChart__dados")

if div:
    print(div.text)
else:
    print("Div não encontrada")