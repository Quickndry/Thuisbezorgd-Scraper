import multiprocessing
import sqlite3
import threading
import concurrent.futures
import time

import scrapydo as scrapydo
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ..Thuizbezongd.spiders.ThuizSpider import ThuizSpider
from ..utils import get_links


class TaskQueue:

    def __init__(self):
        self.tasks = []
        self.num_workers = multiprocessing.cpu_count()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers)
        self.futures = []

        self.lock = threading.Lock()

    def add_task(self, task):
        self.tasks.append(task)

    def run(self):
        [self.futures.append(self.executor.submit(self.consume, task)) for task in self.tasks]

    def consume(self, link):

        #Start spider using concurrent spiders using scrapydo

        spider_to_run = ThuizSpider(link)

        scrapydo.run_spider(spider_to_run,
                            capture_items=True,)

    def stop(self):
        self.executor.shutdown()

    def generate_spider(self, link):
        process = CrawlerProcess(get_project_settings())

        process.crawl(ThuizSpider, {'link': link})
        process.start()


if __name__ == "__main__":
    # Create a queue
    task_queue = TaskQueue()

    region = "Noord-Holland"
    links = get_links(region)

    # Add tasks to the queue in this case, links
    [task_queue.add_task(link) for link in links]

    task_queue.run()
    # Wait for all tasks to be completed
    concurrent.futures.wait(task_queue.futures)
    # task_queue.stop()
