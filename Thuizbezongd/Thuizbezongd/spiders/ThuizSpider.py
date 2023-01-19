import json
import logging
import random
import time
import re

import requests
import scrapy
from requests.adapters import HTTPAdapter
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse
from urllib3 import Retry

from ..items import RestaurantItem, MenuItem
from ..refresh_vpn import refresh_vpn


class ThuizSpider(scrapy.Spider):
    name = 'ThuizSpider'
    allowed_domains = ['cw-api.takeaway.com']

    #  refresh_vpn()
    # 'path': f'/api/v33/restaurants?deliveryAreaId=936068&postalCode={postalCode}&limit=0&isAccurate=true',

    headers = {
        'authority': 'cw-api.takeaway.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'nl',
        'origin': 'https://www.thuisbezorgd.nl',
        'referer': 'https://www.thuisbezorgd.nl/',
        'sec-ch-ua-platform': "Linux",
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'x-country-code': 'nl',
        'x-language-code': 'nl',
        'x-requested-with': 'XMLHttpRequest', }

    def __init__(self, link='',
                 min_sleep_duration=20,
                 use_proxy=False,
                 proxy="",  #Removed for security
                 number_of_attempts=5):
        """
           This constructor takes five arguments and assigns them to the spider's attributes.
        """

        self.sleep_duration = random.randint(min_sleep_duration, min_sleep_duration + 30)

        self.use_proxy = use_proxy
        self.PROXY = proxy
        self.number_of_attempts = number_of_attempts

        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.info(f'Spider is initiated! \n Link: {link}')
        logging.info(f'Params: \n Link: {link}'
                     f'\n Min sleep duration: {min_sleep_duration} \n'
                     f' Proxy: {proxy}\n'
                     f' Use Proxy: {"yes" if use_proxy == True else "no"}')

        self.link = link

    def start_requests(self):
        """
          This method initiates the spider by making the GET request to the API endpoint and passing the headers, proxy, and the parse method as a callback.
        """

        logging.info(f'Started request for link: {self.link}')
        # logging.info(f'Worker: {self.worker}')

        # use dont_filter flag to be able to send same request again.(we send same request in errback in case of a failed request)
        requests_kwargs = {
            'url': self.link,
            'method': 'GET',
            'headers': self.headers,
            'callback': self.parse,
            'dont_filter': True,
            'errback': self.errback
        }

        if self.use_proxy:
            requests_kwargs['meta'] = {'proxy': self.PROXY}

        yield scrapy.http.Request(**requests_kwargs)

    def errback(self, failure):

        # Get the response object if it exists
        response = failure.value.response if hasattr(failure.value, 'response') else None
        # Log the failure details
        logging.error(f'Request failed with status code: {response.status}') if response else None
        logging.error(f'Request failed with url: {failure.request.url}')

        # Check if the number of attempts is greater than 0
        if self.number_of_attempts > 0:
            # refresh_vpn()
            # Too many requests error, so wait longer.
            if response.status == 429:
                logging.info(f"Waiting... 120 sec")
                time.sleep(120)
            else:
                time.sleep(10)

            self.number_of_attempts -= 1
            yield failure.request
        else:
            return

    def parse(self, response: HtmlResponse):
        """
           This method loads the JSON response and extracts the relevant information about each restaurant and stores it in the "restaurant_item" object.
        """

        logging.info(f"Inside the parse method! Request for link: {self.link}")
        restaurants = response.json().get("restaurants")

        if not restaurants:
            self.logger.warning(f"Restaurants not found for link: {response.url}")
            raise CloseSpider("Restaurants not found")

        restaurant_item = RestaurantItem()

        logging.info("Waiting...")
        time.sleep(self.sleep_duration)

        for restaurant_id, restaurant_info in restaurants.items():
            restaurant_item['ID'] = restaurant_info.get("id")
            restaurant_item['name'] = restaurant_info.get("brand", {}).get("name")

            location = restaurant_info.get("location", {})

            restaurant_item['address'] = location.get("streetAddress") + ", " + location.get("city")
            restaurant_item['logo_link'] = restaurant_info.get("brand", {}).get("logoUrl", "").replace("{parameters}/",
                                                                                                       "")
            restaurant_item['website'] = ""

            rating = restaurant_info.get("rating", {})
            restaurant_item['rating_value'] = rating.get("score")
            restaurant_item['rating_count'] = rating.get("votes")

            restaurant_item['item_categories'] = str(
                list(filter(lambda x: x.strip() and x != '',
                            [re.sub(r'\d+|_', '', string) for string in restaurant_info.get("cuisineTypes", [])])))

            shipping_info = restaurant_info.get("shippingInfo", {}).get("delivery", {})

            restaurant_item['delivery_time'] = shipping_info.get("duration", "")
            restaurant_item['min_order_amount'] = float(shipping_info.get("minOrderValue")) / 100. if shipping_info.get(
                "minOrderValue") else ""

            restaurant_item['delivery_area'] = ""
            restaurant_item['postal_codes'] = ""

            primary_slug = restaurant_info.get("primarySlug")
            url = f"https://cw-api.takeaway.com/api/v33/restaurant?slug={primary_slug}"

            logging.info(f"Gathering values is completed for restourant: {restaurant_item['name']}")

            logging.info(f"Yielding request for url: : {url}")

            logging.info("Waiting...")
            time.sleep(self.sleep_duration)

            requests_kwargs = {
                'url': url,
                'method': 'GET',
                'headers': self.headers,
                'callback': self.parse_menus,
                'dont_filter': True,
                'errback': self.errback
            }

            if self.use_proxy:
                requests_kwargs['meta'] = {'proxy': self.PROXY}

            yield scrapy.http.Request(**requests_kwargs)

            yield restaurant_item

    def parse_menus(self, response):

        logging.info("Inside the parse_menus")
        # time.sleep(self.sleep_duration)
        # logging.info("Waiting...")

        data = response.json()

        rest_name = data.get("brand").get("name")
        logging.info(f"Parsing menus for {rest_name}")
        menus = data.get("menu", {})
        products = menus.get("products", {})

        # iterate through products
        for product_id, product_info in products.items():

            final_category = ""
            # check if product is in categories
            for category in menus.get("categories", []):
                if product_id in category.get("productIds", []):
                    final_category = category.get("name")

            product_name = product_info.get("name")

            logging.info(f"Parsing products... Product name: {product_name}")

            menu_item = MenuItem()

            menu_item['restaurant_ID'] = data.get("restaurantId")
            menu_item['item_ID'] = product_id
            menu_item['item_name'] = product_info.get("name")
            menu_item['item_category'] = final_category
            menu_item['item_price'] = float(
                product_info.get("variants", [{}])[0].get("prices", {}).get("delivery")) / 100

            yield menu_item
