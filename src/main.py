import asyncio
import logging

from estate import IdealistaScraper, ScraperService
from repository import Repository
from tg import TgBot
from config import load_config


async def main():
    logging.basicConfig(level=logging.INFO)
    config = load_config()

    repo = Repository(config)
    bot = TgBot(config, repo)
    scraper = IdealistaScraper()
    service = ScraperService(scraper, repo, bot)

    await repo.connect()
    await bot.start()
    await service.start(config)
    await bot.stop()

if __name__ == '__main__':
    asyncio.run(main())
