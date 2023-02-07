from estate import IdealistaScraper
from tg import TgBot
import psycopg2
from time import sleep
from asyncio import run
import json
import os


def main():
    token = os.environ['TELEGRAM_TOKEN']
    whitelist = list(map(int, json.loads(os.environ['TELEGRAM_WHITELIST'])))
    print(whitelist)
    bot = TgBot(token=token, id_whitelist=whitelist)
    run(listen(bot))
    print('Скрейпер запущен')
    bot.run()
    print('Бот запущен')


async def listen(bot: TgBot):
    while True:
        url = 'https://www.idealista.com/ru/venta-viviendas/valencia-valencia/con-precio-hasta_100000,pisos,apartamentos,lofts,buhardilla,publicado_ultimas-48-horas/?ordenado-por=fecha-publicacion-desc'
        scraper = IdealistaScraper()
        articles = scraper.get_articles(url)
        connection = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host=os.environ['POSTGRES_HOST'])
        cursor = connection.cursor()

        for article in articles:
            cursor.execute(
                'INSERT INTO articles (id, title, specs, description) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING',
                (article['id'], article['title'], article['specs'], article['desc']))
            if cursor.rowcount > 0:
                print('Добавлено ' + str(article['id']))
                try:
                    await bot.send_article(article)
                except:
                    print("Ошибка при отправлении")
                finally:
                    sleep(0.1)

        connection.commit()
        cursor.close()
        sleep(300)


if __name__ == '__main__':
    main()
