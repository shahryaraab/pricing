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

# run spider with ==> scrapy crawl geturl
class getUrlscraper(scrapy.Spider):
    name = 'geturl'

    start_urls = []
    num_page = []
    wb = open_workbook('E:/digikala_digital_product/link_page.xlsx')
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
        # iterator = int (input('number of page ==> '))
        # iterator = int (input('number of page ==> '))
        # urls = [u'https://www.digikala.com/brand/moulinex/']
        urls = []
        for crawl_url in range (0,len(self.start_urls)):
            urls.append(self.start_urls[crawl_url])
            for page in range(2 ,int(self.num_page[crawl_url]+1)):
                url = self.start_urls[crawl_url]+str('?pageno=')+str(page)
                urls.append(url)
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # self.driver = webdriver.Chrome("E:/scrapy/chromedriver.exe")
        SET_SELECTOR = '.products__item-fatitle'
        # self.driver.get(response.url)

        product_selector = '.c-listing'
        product_data = []
        itemlink = []
        product_price_list = []
        product_name_list = []
        # product_en_name_list =[]
        # product_image_list = []
        # product_image_list_print = []
        product_data_list = []

        try:
            for brickset in response.css(product_selector):
                NAME_SELECTOR = 'div ul li div div div a::text'
                LINK_SELECTOR = 'div ul li div div div a::attr(href)'
                namep = brickset.css(NAME_SELECTOR).extract()
                link = brickset.css(LINK_SELECTOR).extract()
                print('====================')
                print(namep);
                print('********************')
                print(link);
                print('====================')
                product_data_list.append(namep)
                product_data_list.append(link)


            print('namep == > ', len(product_data_list[0]))
            pprint.pprint(product_data_list[0])
            print('pro 1 == > ', len(product_data_list[1]))
            pprint.pprint(product_data_list[1])


            # if(EC.presence_of_element_located((By.XPATH , '/html/body/main/div[2]/div/div[1]/div/div[2]/div/article/div[2]/div[3]/ul/li[6]/a')) != None):
            #     element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH , '/html/body/main/div[2]/div/div[1]/div/div[2]/div/article/div[2]/div[3]/ul/li[6]/a')))
        #     links = self.driver.find_elements_by_class_name('c-product-box__img')
        #     product_name = self.driver.find_elements_by_class_name('c-product-box__title')
        #
        #     for name in product_name:
        #         product_name_list.append(name.text)
        #         print( '======' ,name.text)
        #     pprint.pprint(product_name_list)
        #
        #     for link in links:
        #         itemlink.append(link.get_attribute("href"))
        #
        #
            product_data = ['']
            for product in range( 0 , len(product_data_list[0])):

                print ('iterator ===========>', product )
                print ('iterator ===========>', product_data_list[0][product] )
                product_data[0] += product_data_list[0][product]
                product_data[0] += '\t'
                product_data[0] += 'https://www.digikala.com'
                print ('iterator ===========>', product_data_list[1][product] )
                product_data[0] += product_data_list[1][product]
                product_data[0] += '\n'

            print('=================================================')
            pprint.pprint(product_data)

        #
        #
        # # write name , price and image path to csv file
            with open('E:/digikala_digital_product/links.csv', 'a', newline='', encoding="utf-16") as csvoutput:
                writer = csv.writer(csvoutput, quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for val in product_data:
                    if (val is not None):
                        writer.writerow([val])

        finally:
        # quit chrome driver after fetch data
            # self.driver.quit()\
            print('finished')
