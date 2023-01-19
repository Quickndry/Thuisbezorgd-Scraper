import logging
from select import select

from Thuizbezongd.gen_spider import GenSpider

from typing import Optional

PROVINCES = ['Groningen', 'Friesland', 'Drenthe', 'Overijssel', 'Gelderland',
             'Utrecht', 'Noord-Holland', 'Zuid-Holland', 'Zeeland', 'Noord-Brabant', 'Limburg']


def province_selector(default: Optional[str] = 'Noord-Holland') -> str:
    while True:
        print(f"Select a province in the Netherlands (default is {default}): ")
        for index, province in enumerate(PROVINCES):
            print(f"{index + 1}. {province}")
        user_input = input()

        if not user_input:
            return default

        try:
            index = int(user_input) - 1
            if 0 <= index < len(PROVINCES):
                return PROVINCES[index]
        except ValueError:
            pass
        print("Invalid input. Please select a number from the list.")


if __name__ == '__main__':
    province = province_selector()
    logging.info(f"{province} has been selected!")

    spider_kwargs = {}
    ##Spider configuration
    # spider_kwargs = {'min_sleep_duration': 15,
    #                  'use_proxy': True,
    #                  'proxy': "http://matrixian:TYYQeMZ7uI76YQ0p@proxy.packetstream.io:31112",
    #                  'number_of_attempts': 5}

    # Default is Noord-Holland
    GenSpider(province, spider_kwargs)
