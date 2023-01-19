import concurrent.futures
import time

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ..Thuizbezongd.spiders.ThuizSpider import ThuizSpider
from ..utils import get_links


class MySpider:
    def generate_spider(self, link):

        print(link)
        time.sleep(4)
        process = CrawlerProcess(get_project_settings())
        process.crawl(ThuizSpider, {'link': link})
        process.start()

    def run_spiders(self, links):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            [executor.submit(self.generate_spider, task) for task in links]


if __name__ == "__main__":

    region = "Noord-Holland"

    # Task is api_links for addresses
    links = get_links(region)

    a = MySpider()
    a.run_spiders(links)