# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RestaurantItem(scrapy.Item):
    ID = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    logo_link = scrapy.Field()
    website = scrapy.Field()
    rating_value = scrapy.Field()
    rating_count = scrapy.Field()
    delivery_time = scrapy.Field()
    item_categories = scrapy.Field()
    min_order_amount = scrapy.Field()
    delivery_area = scrapy.Field()
    postal_codes = scrapy.Field()


class MenuItem(scrapy.Item):
    restaurant_ID = scrapy.Field()
    item_ID = scrapy.Field()
    item_name = scrapy.Field()
    item_category = scrapy.Field()
    item_price = scrapy.Field()

