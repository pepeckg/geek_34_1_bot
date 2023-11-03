from parsel import Selector
import httpx
import asyncio

class AllNewsScraper:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    BASE_URL = "https://itshaman.ru/news/"
    list_news = ["apple", "mobile", "software", "hardware", "gaming", "linux", "crypto", "windows"]
    LINK_XPATH = '//article[@role="article"]/a/@href'

    async def parse_group(self, group):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            url = f"{self.BASE_URL}{group}/"
            response = await client.get(url)
            print(response.url)
            await self.scrape_links(html=response.text)

    async def scrape_links(self, html):
        tree = Selector(text=html)
        links = tree.xpath(self.LINK_XPATH).extract()
        for link in links:
            print(link)

    async def get_latest_links(self, group, limit):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            url = f"{self.BASE_URL}{group}/"
            response = await client.get(url)
            html = response.text
            tree = Selector(text=html)
            links = tree.xpath(self.LINK_XPATH).extract()
            return links[:limit]

    async def scrape_all_groups(self):
        await asyncio.gather(*(self.parse_group(group) for group in self.list_news))


if __name__ == "__main__":
    scraper = AllNewsScraper()
    asyncio.run(scraper.scrape_all_groups())


