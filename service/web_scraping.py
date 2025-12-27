import requests
import json
from bs4 import BeautifulSoup
import logging

def get_data(ticker):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; DataBot/1.0)"
        }

        url = f"https://fiis.com.br/{ticker}/"
        html = requests.get(url, headers=headers).text

        soup = BeautifulSoup(html, "html.parser")

        div = soup.find("div", class_="yieldChart__dados").text.replace('\n', ' ').replace('\t', '').strip()
        items = div.split()
        if div:
            header_tokens = items[:10]
            data_tokens = items[10:]

            keys = [
                header_tokens[0],
                f"{header_tokens[1]} {header_tokens[2]}",
                f"{header_tokens[3]} {header_tokens[4]}",
                f"{header_tokens[5]} {header_tokens[6]}",
                f"{header_tokens[7]} {header_tokens[8]}",
                header_tokens[9],
            ]

            chunk_size = 8
            payload = []

            for idx in range(0, len(data_tokens), chunk_size):
                chunk = data_tokens[idx:idx + chunk_size]

                if len(chunk) < chunk_size:
                    logging.warning("Bloco incompleto ignorado: %s", chunk)
                    continue

                payload.append(
                    {
                        keys[0]: chunk[0],
                        keys[1]: chunk[1],
                        keys[2]: chunk[2],
                        keys[3]: f"{chunk[3]} {chunk[4]}",
                        keys[4]: chunk[5],
                        keys[5]: f"{chunk[6]} {chunk[7]}",
                    }
                )

            logging.info(payload)
            return payload
        else:
            logging.error("Div não encontrada")
            return []
    except Exception as e:
        logging.error(f"Erro ao buscar dados: {e}")
        return None