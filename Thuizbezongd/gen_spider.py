import logging
import time

from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings

from Thuizbezongd.Thuizbezongd import settings as my_settings
from Thuizbezongd.Thuizbezongd.spiders.ThuizSpider import ThuizSpider
from Thuizbezongd.utils import get_links


class GenSpider:

    def __init__(self, region="Noord-Holland", spider_kwargs=None):

        if spider_kwargs is None:
            spider_kwargs = {}

        links = get_links(region)

        if not links:
            print("Region not found!")
            return

        for link in links:
            logging.info(f"Spider is generating with link: {link}")

            spider_kwargs['link'] = link

            self.generate_spider(spider_kwargs)
            logging.info(f"Spider is generating completed with link: {link}")
            logging.info(f"Waiting")
            time.sleep(60)

    def generate_spider(self, spider_kwargs):

        crawler_settings = Settings()
        # Get settings, https://github.com/scrapy/scrapy/issues/1904
        crawler_settings.setmodule(my_settings)
        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(ThuizSpider, **spider_kwargs)
        process.start()
