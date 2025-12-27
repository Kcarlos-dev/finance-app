import requests
import json
from bs4 import BeautifulSoup
import logging

def get_paper(ticker):
    try:
        if not ticker:
            logging.error("Ticker não informado")
            return None
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; DataBot/1.0)"
        }
        url = f"https://www.fundamentus.com.br/detalhes.php?papel={ticker}"
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", class_="conteudo clearfix")
        tb = div.find("table")
        dados = []
        for row in tb.find_all("tr"):
            cols = [td.get_text(strip=True).replace('?',"") for td in row.find_all(["td", "th"])]
            if cols:
                dados.append(cols)
        payload = {
            f"{dados[0][0]}": dados[0][1],
            f"{dados[0][2]}": dados[0][3],
            f"{dados[1][2]}": dados[1][3],
            f"{dados[2][2]}": dados[2][3],
            f"{dados[3][2]}": dados[3][3],
            f"{dados[4][2]}": dados[4][3],
        }
        return payload
    except Exception as e:
        logging.error(f"Erro ao buscar dados: {e}")
        return None