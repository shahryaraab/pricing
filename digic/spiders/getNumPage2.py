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
from xlrd import open_workbook


# run spider with ==> scrapy crawl get_num_page
class numPageScraper(scrapy.Spider):
    name = 'get_num_page'

    start_urls = []
    wb = open_workbook('E:/categories.xlsx')
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols

    for row in range(0, number_of_rows):
        value  = (sheet.cell(row,0).value);
        if (str(value).strip()  != ''):
            start_urls.append(value)

    def parse(self, response):
        page_number_selector = '.c-pager__next'
        product_data = []
        product_data_list = []

        # add url to output list
        product_data_list.append(response.url)

        for brickset in response.css(page_number_selector):
            page_num_selector = '::attr(data-page)'
            number_of_page = brickset.css(page_num_selector).extract()
            print('num page == > ' , number_of_page)
            if(number_of_page is  not None):
                product_data_list.append(number_of_page)
            else:
                product_data_list.append('onepage')

        print('ppppppp',product_data_list)
        product_data = ['']
        product_data[0] += product_data_list[0]
        product_data[0] += '\t'
        product_data[0] += product_data_list[1][0]
        product_data[0] += '\n'

        print('=================================================')
        pprint.pprint(product_data)

    # # write name , price and image path to csv file
        with open('E:/digikala_digital_product/link_page.csv', 'a', newline='', encoding="utf-16") as csvoutput:
            writer = csv.writer(csvoutput, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for val in product_data:
                if (val is not None):
                    writer.writerow([val])
