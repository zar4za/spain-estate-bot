import requests
from bs4 import BeautifulSoup


def aggregate(item):
    link = item.find('a', class_='item-link')
    specs = map(lambda x: x.text, item.findAll('span', class_='item-detail'))
    desc = item.find('div', class_='item-description')

    return {
        'id': int(link.attrs['href'].split('/')[3]),
        'title': link.text[:64],
        'url': link.attrs['href'],
        'specs': ', '.join(specs)[:256],
        'desc': desc.text[:512]
    }


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

    def get_articles(self, url):
        page = self.session.get(url)
        print(page.status_code)

        soup = BeautifulSoup(page.text, 'html.parser')
        articles = soup.findAll('article', class_='item')
        articles = list(map(aggregate, articles))
        return articles

