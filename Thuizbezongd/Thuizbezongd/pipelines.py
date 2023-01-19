import logging
import sqlite3

from Thuizbezongd.Thuizbezongd.items import RestaurantItem, MenuItem


class RestaurantPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        import os.path

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "../thuisbezongd.db")

        with sqlite3.connect(db_path) as self.conn:
            self.curr = self.conn.cursor()

    def create_table(self):
        # self.curr.execute("""DROP TABLE IF EXISTS restaurants""")
        # self.curr.execute("""DROP TABLE IF EXISTS menus""")

        self.curr.execute("""CREATE TABLE IF NOT EXISTS restaurants(ID TEXT PRIMARY KEY, name TEXT, address TEXT,
                             logo_link TEXT, website TEXT, rating_value REAL,
                             rating_count INTEGER, delivery_time INTEGER, item_categories TEXT,
                             min_order_amount REAL, delivery_area TEXT, postal_codes TEXT)""")

        self.curr.execute("""CREATE TABLE IF NOT EXISTS menus(item_ID TEXT PRIMARY KEY, restaurant_ID TEXT, 
                              item_name TEXT, item_category TEXT, item_price REAL,
                              FOREIGN KEY (restaurant_ID) REFERENCES restaurants (ID))""")

    def process_item(self, item, spider):
        if isinstance(item, RestaurantItem):
            self.store_restaurant(item)

        elif isinstance(item, MenuItem):
            self.store_menu(item)

        return item


    def store_restaurant(self, item):

        logging.info("Restourant inserting... ", item)
        cursor =self.curr.execute \
            ("""INSERT INTO restaurants (ID, name, address, logo_link, website, rating_value, rating_count, delivery_time, item_categories, min_order_amount, delivery_area, postal_codes) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(ID) DO NOTHING""", (
            item['ID'],
            item['name'],
            item['address'],
            item['logo_link'],
            item['website'],
            item['rating_value'],
            item['rating_count'],
            item['delivery_time'],
            item['item_categories'],
            item['min_order_amount'],
            item['delivery_area'],
            item['postal_codes'],))

        if cursor:
            logging.info("Restourant inserted successfully")
        else:
            logging.error("Error: Failed to insert restourant")

        self.conn.commit()

    def store_menu(self, item):
        logging.info("Menu inserting... ", item)
        cursor = self.curr.execute \
            ("""INSERT INTO menus (item_ID, restaurant_ID, item_name, item_category, item_price) VALUES(?,?,?,?,?)
                         ON CONFLICT(item_ID) DO NOTHING""",
                          (
                              item['item_ID'],
                              item['restaurant_ID'],
                              item['item_name'],
                              item['item_category'],
                              item['item_price'],
                          ))

        if cursor:
            logging.info("Menu inserted successfully")
        else:
            logging.error("Error: Failed to insert menu")

        self.conn.commit()

