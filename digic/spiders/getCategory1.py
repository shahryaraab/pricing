import scrapy
import csv
import itertools
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pprint
import urllib.request

# run spider with ==> scrapy crawl geturl
class categoryscraper(scrapy.Spider):
    name = 'get_path'
    start_urls = ['https://www.digikala.com/']

    def parse(self, response):
        SET_SELECTOR = '.c-navi-new__medium-display-title'
        name_list = []
        address_list = []
        for brickset in response.css(SET_SELECTOR):
            NAME_SELECTOR = 'span::text,::text'
            address_selector = '::attr(href)'
            namep = brickset.css(NAME_SELECTOR).extract()
            address = brickset.css(address_selector).extract()
            pprint.pprint(namep)
            name_list.append(namep[0].strip())

            address_list.append(address[0].strip())
            print('name ===== > ' , len(name_list))
            print('address ===> ' , len(address_list))
        pprint.pprint(name_list)
        pprint.pprint(address_list)

        with open('E:/categories.csv', 'a', newline='', encoding="utf-16") as csvoutput:
            writer = csv.writer(csvoutput, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for val in address_list:
                if (val is not None):
                    writer.writerow([val])
