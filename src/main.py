import asyncio
from asyncio import sleep

from src.repository import Repository
from tg import TgBot
from config import load_config


async def main():
    config = load_config()
    repo = Repository(config)
    bot = TgBot(config, repo)
    await repo.connect()
    await bot.start()
    await sleep(60)
    # sleep method is used while nothing is here to prevent app from closing
    await bot.stop()

if __name__ == '__main__':
    asyncio.run(main())
