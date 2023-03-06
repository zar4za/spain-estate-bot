import asyncio
from asyncio import sleep

from tg import TgBot
from config import load_config


async def main():
    config = load_config('../appsettings.json')
    bot = TgBot(config)
    await bot.start()
    await sleep(60)
    # sleep method is used while nothing is here to prevent app from closing
    await bot.stop()

if __name__ == '__main__':
    asyncio.run(main())

