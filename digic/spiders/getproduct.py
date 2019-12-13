import scrapy
import itertools
import codecs
import pprint
import scrapy
import csv
import itertools
import urllib.request
from hashids import Hashids
from xlrd import open_workbook
import json
from datetime import datetime
from unidecode import unidecode

class BrickSetSpider(scrapy.Spider):
    name = 'get_pro'
    start_urls = []
    mainpro = []
    wb = open_workbook('E:/digikala_digital_product/links.xlsx')
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols

    for row in range(0, number_of_rows):
        value  = (sheet.cell(row,1).value);
        if (str(value).strip()  != ''):
            start_urls.append(value)

    started_index = 9700
    end_index = 15000
    num_product = end_index - started_index
    start_urls = start_urls[started_index:end_index]
    iterator = 0
    start_SKU = int(input("please enter the start number : "))
    data_attr_value = []
    data_attr = []
    attr_accu = ['']
    product_data = []
    product_data_en = []
    product_image = []
    product_sku_list = []
    product_brand = []
    product_category = []
    product_url = []
    attribute_list = []
    product_description =[]
    product_price =[]
    product_category = []
    product_brand = []

    def parse(self, response):
        hashids = Hashids(salt='yp',min_length=7,alphabet='ABCDEFGHJKLMNPQRSTUVWXYZ1234567890')
        #selector set for get main product data
        Product_Detail_Selector = '.c-product__info'
        Image_Selector ='.c-gallery '
        Category_Selector = '.c-params'
        attr_key_Selector = '.c-params__list-key'
        attr_value_selector = ".c-params__list-value"
        Product_Price_Selector =".c-product__seller-price-real"
        desc_selector =".c-content-expert__summary"

        att_list= []
        value_list =[]
        product_data_list = []
        attribute_list = []
        product_image_list = []
        save_list = []
        attribute_type_list = []
        attr_sign_list = []
        pro_description = []
        pro_price =[]
        product_image_list_print = []
        product_sku = []
        pro_img_list_split = []
        product_en_name_list =[]
        split_name =[]
        pre_attr_list_accu_change = False
        brand_list = []
        category_list = []
        stock_title_list= ['']

# ********************************************************************
        #get main product data
        for brickset in response.css(Product_Detail_Selector):
            nameSelector = 'div h1::text'
            latinNameSelector = 'div h1 span::text'
            brandANDcategorySelector = 'div div div div ul li a::text '
            brandSelector = 'div div div div ul li a::text '
            namep = brickset.css(nameSelector).extract_first()
            namep_EN = brickset.css(latinNameSelector).extract_first()
            brandANDcategory = brickset.css(brandSelector).extract()
            product_data_list.append([namep])
            if (namep_EN is not None):
                product_data_list.append([namep_EN])
            else:
                product_data_list.append([''])
            if(len(brandANDcategory)==1):
                category_list.append(brandANDcategory[0])
                brand_list.append([''])
            elif(len(brandANDcategory)>1):
                category_list.append(brandANDcategory[1])
                brand_list.append(brandANDcategory[0])

        #get product price
        for brickset in response.css(Product_Price_Selector):
            priceSelector = 'div::text '
            price = brickset.css(priceSelector).extract_first()
            if(price is not None):
                if(len(price)>0):
                    pro_price.append([unidecode(price)])
                else:
                    pro_price.append([''])
            else:
                pro_price.append([''])
            # pprint.pprint(price)

        #get product brand
        for brickset in response.css(Product_Detail_Selector):
            brandSelector = 'div div div div ul li a::text  '
            brand = brickset.css(brandSelector).extract()
            product_data_list.append([brand])
            # pprint.pprint(brand)

        stock_title_selector = ".c-product-stock__title"
        for brickset in response.css(stock_title_selector):
            stock_selector = '::text'
            stock_title = brickset.css(stock_selector).extract()
            if (stock_title is not None):
                stock_title_list[0]=stock_title[0].strip()
            else:
                stock_title_list.append('')

        #get product description
        for pro_desc in response.css(desc_selector):
            NAME_SELECTOR = 'div div p::text'
            desc = pro_desc.css(NAME_SELECTOR).extract_first()
            if(desc is not None):
                if(len(desc)>0):
                    pro_description.append(desc)
                else :
                    pro_description.append([''])
            # pprint.pprint(desc);

        #get product image
        for brickset in response.css(Image_Selector):
            NAME_SELECTOR = 'div div img::attr(data-zoom-image) ,ul li div img::attr(data-src)'
            imgp = brickset.css(NAME_SELECTOR).extract()
            product_image_list.append(imgp)
            # pprint.pprint(imgp);

        # print(product_image_list)
        sku = hashids.encode(self.start_SKU + self.iterator)
        product_sku.append (sku)
        self.iterator +=1
        iter = 0
# **************************************save image*********************************
        for image in range(0,len(product_image_list[0])) :
                product_image_350_save ,temp = product_image_list[0][image].split('?')
                if (namep_EN is not None):
                    namep_EN  = [w.replace(' ', '-') for w in namep_EN]
                    namep_EN = [w.replace('.', '-') for w in namep_EN]
                    namep_EN = [w.replace('(', '-') for w in namep_EN]
                    namep_EN = [w.replace(')', '-') for w in namep_EN]
                    namep_EN = [w.replace('&', '-') for w in namep_EN]
                    namep_EN = [w.replace('+', '-') for w in namep_EN]
                    split_name = [w.replace('/', '-') for w in namep_EN]
                    name=''
                    name = ''.join(split_name)
                    pro_img_title ="E:/digikala_digital_product/product-9700/product_photo/"+name
                else :
                    pro_img_title ="E:/digikala_digital_product/product-9700/product_photo/"
                pro_img_title +='-YP-'
                pro_img_title += str(sku).strip()
                pro_img_title += '-'
                pro_img_title += str(iter)
                pro_img_title += '.jpg'
                iter +=1
            # create path to save image
                product_image_list_print.append(pro_img_title)
            # download first image to the Photo directory
                if (iter == 1):
                    urllib.request.urlretrieve(product_image_350_save , pro_img_title)

        #get attribute value
        for brickset1 in response.css(attr_key_Selector):
            Attribute_Type_Selector = 'article section ul li div::attr(class)'
            Attribute_Selector = 'span::text ,  span a::text'
            att_value = brickset1.css(Attribute_Selector).extract()
            value_list.append(att_value)
            # pprint.pprint(att_value)

        #get attribute key
        for brickset3 in response.css(attr_value_selector):
            Attribute_value_Selector = 'span::text ,  span a::text'
            att_key = brickset3.css(Attribute_value_Selector).extract()
            for value in att_key:
                index = att_key.index(value)
                blank_array = str(att_key[index]).splitlines()
                blank_str = ''
                for i in blank_array:
                    if(len(i.strip())>=1):
                        blank_str += i.strip()

                att_key[index] = blank_str
            att_list.append(att_key)
            # pprint.pprint(att_key)

        attt = ''
        attribute = {}
        index = 0
        last = 0
        for item in range(0 , len(att_list)-1):
            if(len(value_list[index])!=0):
                if(index is not 0):
                    attt += ','
                attribute[str(value_list[index][0]).strip()] = []
                attribute[str(value_list[index][0]).strip()].append(str(att_list[index][0]).strip())
                attt += str(value_list[index][0]).strip()
                attt += '='
                attt += str(att_list[index][0]).strip()
                last = index
                index +=1

            else :
                if(len(att_list[index])>0):
                    attt += '</br>'
                    attt += str(att_list[index][0]).strip()
                    attribute[str(value_list[last][0]).strip()].append(str(att_list[index][0]).strip())
                    index +=1

        if (len(pro_price)==0):
            pro_price.append([''])

        time = datetime.now()
        timesave  =time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        pro = {}
        pro = {
            'product_name' : product_data_list[0][0].strip(),
            'product_en_name' : product_data_list[1][0].strip(),
            'sku' : product_sku[0],
            'stock_title' : stock_title_list[0],
            'product_pic' : product_image_list_print ,
            'price' : [ { 'price' : pro_price[0][0].strip().replace(",",''),'date' :timesave, 'source' :response.url}],
            'brand' : brand_list[0],
            'category' : category_list[0],
            'url' : [response.url],
            'product_desc' : pro_description,
            'imported' :'',
            'HS-code' : '' ,
            'barcode': '',
            'GS1' : '',
            'add_date' : timesave
        }

        pro['attribute_list'] = attribute
        self.mainpro.append(pro)

        with open('E:/digikala_digital_product/product-9700/data.json', 'w', encoding='utf-8') as f:
            json.dump(self.mainpro, f, ensure_ascii=False, indent=4, default=str)

        print_data = ['']
        print_data[0] += product_sku[0]
        print_data[0] += '\t'
        print_data[0] += str(pro_price[0][0]).replace(',','').strip()
        print_data[0] += '\t'
        if (len(pro_description)>0):
            print_data[0] += str(pro_description[0]).replace('\n','').strip()
        print_data[0] += '\t'
        print_data[0] += str(stock_title_list[0])
        print_data[0] += '\t'
        print_data[0] += str(product_data_list[0][0]).replace('\r\n','').strip()
        print_data[0] += '\t'
        print_data[0] += str(product_data_list[1][0]).replace('\r\n','').strip()
        print_data[0] += '\t'
        print_data[0] += str(attt).replace('\r\n','').strip()
        print_data[0] += '\t'
        print_data[0] += str(product_image_list_print[0])
        if(len(product_image_list_print )>1):
            print_data[0] += '\t'
            print_data[0] += str(product_image_list_print[1:])
        else:
            print_data[0] += '\t'

        with open('E:/digikala_digital_product/product-9700/product_data.csv', 'a', newline='', encoding="utf-16") as csvoutput:
            writer = csv.writer(csvoutput, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for val in print_data :
                writer.writerow([val])
        print('===========================================================')
        print('product == > ', self.iterator , ' of ' , self.num_product )
        print((self.iterator / self.num_product)*100 ,' % complete')
