"https://itshaman.ru/news/"
from parsel import Selector
import requests


class NewsScraper:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    URL = 'https://itshaman.ru/news/'
    LINK_XPATH = '//article[@role="article"]/a/@href'
    # PLUS_URL = 'https://www.prnewswire.com'
    # DATE_XPATH = '//h3/small/text()'

    def parse_data(self):
        html = requests.get(url=self.URL).text
        tree = Selector(text=html)
        links = tree.xpath(self.LINK_XPATH).extract()

        for link in links:
            print(link)

        return links[:5]


if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.parse_data()






