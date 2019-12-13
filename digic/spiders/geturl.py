import scrapy
import csv
import itertools
import pprint
import urllib.request
from xlrd import open_workbook

# run spider with ==> scrapy crawl geturl
class getUrlscraper(scrapy.Spider):
    name = 'geturl'
    start_urls = []
    num_page = []

    wb = open_workbook('E:/products/flormar/link_page.xlsx')
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols

    for row in range(0, number_of_rows):
        value  = (sheet.cell(row,0).value);
        num = (sheet.cell(row,1).value);
        if (str(value).strip()  != ''):
            start_urls.append(value)
            num_page.append(num)

    def start_requests(self):
        urls = []
        for crawl_url in range (0,len(self.start_urls)):
            urls.append(self.start_urls[crawl_url])
            for page in range(2 ,int(self.num_page[crawl_url]+1)):
                url = self.start_urls[crawl_url]+str('?pageno=')+str(page)
                urls.append(url)
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        SET_SELECTOR = '.products__item-fatitle'
        product_selector = '.c-listing'
        product_data = []
        itemlink = []
        product_price_list = []
        product_name_list = []
        product_data_list = []

        try:
            for brickset in response.css(product_selector):
                NAME_SELECTOR = 'div ul li div div div a::text'
                LINK_SELECTOR = 'div ul li div div div a::attr(href)'
                namep = brickset.css(NAME_SELECTOR).extract()
                link = brickset.css(LINK_SELECTOR).extract()
                product_data_list.append(namep)
                product_data_list.append(link)

            product_data = ['']
            for product in range( 0 , len(product_data_list[0])):
                product_data[0] += product_data_list[0][product]
                product_data[0] += '\t'
                product_data[0] += 'https://www.digikala.com'
                product_data[0] += product_data_list[1][product]
                product_data[0] += '\n'

        # # write name , price and image path to csv file
            with open('E:/products/flormar/links.csv', 'a', newline='', encoding="utf-16") as csvoutput:
                writer = csv.writer(csvoutput, quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for val in product_data:
                    if (val is not None):
                        writer.writerow([val])

        finally:
            print('finished')
