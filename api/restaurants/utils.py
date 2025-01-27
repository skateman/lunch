from datetime import datetime
import os
import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MENICKA_URL = "https://www.menicka.cz/api/iframe/?id=%s"


def fetch_html(url, encoding="utf-8"):
    for _ in range(3):
        try:
            response = requests.get(url)
            response.encoding = encoding
            if response.status_code == 200:
                return BeautifulSoup(response.text, features="lxml")
            logger.warning("Error during fetching url %s: HTTP %s, %s",
                           url, response.status_code, response.text)
        except requests.exceptions.RequestException:
            logger.warning("Error fetching url.")
    logger.error("URL not fetched.")
    return None


def fetch_menicka(restaurant_id):
    return fetch_html(MENICKA_URL % restaurant_id, encoding="windows-1250")


def parse_menicka(html):
    result = {}
    for content in html.find_all("div", {"class": "content"}):
        h2 = content.find("h2")
        if h2:
            current_date = datetime.strptime(h2.text.split()[1], "%d.%m.%Y").date()
            result[current_date] = []
            for tr in content.find_all("tr"):
                for alergen in tr.find_all("em"):
                    alergen.extract()
                result[current_date].append(tr.text)
    return result
