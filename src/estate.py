import logging
import re
from asyncio import sleep

import requests
from bs4 import BeautifulSoup

from repository import Repository
from tg import TgBot

logger = logging.getLogger(__name__)


def aggregate(item):
    link = item.find('a', class_='item-link')
    specs = list(map(lambda x: x.text, item.findAll('span', class_='item-detail')))
    price = item.find('span', class_='item-price')

    return Article(
        article_id=int(link.attrs['href'].split('/')[3]),
        title=link.text[:64],
        url=link.attrs['href'],
        specs=specs,
        price=price.text
    )


class IdealistaScraper:
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/87.0.4280.141 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                      'image/avif,image/webp,image/apng,*/*;q=0.8,application/'
                      'signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru,fil;q=0.9,pt;q=0.8,pt-BR;q=0.7,pt-PT;q=0.6,es;q=0.5,en;q=0.4',
            'cache-control': 'no-cache',
            'cookie': 'afUserId=6daf1859-1f83-43c5-b67c-1dbcae427392-p',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'upgrade-insecure-requests': '1'
        }
        self.session.headers.update(self.headers)
        logger.info("Initialized scraper.")

    def get_articles(self, url):
        page = self.session.get(url)
        if page.status_code == 200:
            logger.info("Loaded page.")
        else:
            logger.warning(f"Failed to load page. Status code: {page.status_code}")

        soup = BeautifulSoup(page.text, 'html.parser')
        articles = soup.findAll('article', class_='item')
        articles = list(map(aggregate, articles))
        return articles


class Article:
    def __init__(self, article_id, title: str, url: str, price: str, specs: list):
        self.article_id = article_id
        self.title = title
        self.url = 'https://idealista.com' + url
        self.price = price
        self.room_count = str(specs[0])
        self.area = str(specs[1])
        self.floor = specs[2]
        self.elevator = str(specs[2]).find('лифтом') != -1


class ScraperService:
    def __init__(self, scraper: IdealistaScraper, repo: Repository, bot: TgBot):
        self.scraper = scraper
        self.repo = repo
        self.bot = bot

    async def start(self, config):
        url = (f"https://www.idealista.com/ru/venta-viviendas/{config['filter']['region']}/"
               f"{config['filter']['filters']}publicado_ultimas-48-horas/?ordenado-por=fecha-publicacion-desc")
        logger.info("Started polling service.")

        while True:
            articles = self.scraper.get_articles(url)
            new_articles = self.repo.insert_many_articles(articles)
            users = self.repo.get_userids_to_notify()

            for article in new_articles:
                for userid in users:
                    await self.bot.send_article(userid[0], article)
                    await sleep(0.2)

            logger.info("Idling for next 5 minutes.")
            await sleep(300)

