# -*- coding: utf-8 -*-
import scrapy
import json
from bs4 import BeautifulSoup
from magistral.items import Product
from scrapy.loader import ItemLoader

product_item = Product()

class MagistralSpider(scrapy.Spider):
    name = 'mst'
    allowed_domains = ['magistral-nn.ru']


    def start_requests(self):
        yield scrapy.FormRequest('https://www.magistral-nn.ru/automag/?SECTION_ID=23483&getdata=true&nd=1616783290021&_search=true&nd=1616786082075&rows=50&page=1&sidx=id&sord=asc&name=%D0%92%D0%90%D0%97',
                                     callback=self.parse, method='GET')


    def sort_in_model(self, text):
        model = ['ВАЗ-2107', 'ВАЗ-2109', 'ВАЗ-2112', 'Калина', 'Приора', 'Нива', 'ВАЗ-2101', 'ВАЗ-2114']
        all_model = ['ВАЗ-2101', 'ВАЗ-2105', 'ВАЗ-2121', 'ВАЗ-2106', 'ВАЗ-2107', 'ВАЗ-2108', 'ВАЗ-2109', 'ВАЗ-2112', 'ВАЗ-2113', 'Калина', 'Приора', 'Нива', 'ВАЗ-2114']
        text_out_model = ''
        for elem in all_model:

            if elem in text:
                text_out_model = text.replace(elem, '')
                find_model = elem
                return [find_model, text_out_model]
            else:
                find_model = None
                text_out_model = text
        return [find_model, text_out_model]


    def parse(self, response):
        page = json.loads(response.text)['page']
        total = json.loads(response.text)['total']
        text = '!!!****_______________________=================   PAGES: '
        end_text = '    =================_______________________****!!!'
        print(text, total, page, end_text)
        item = Product()
        for row in json.loads(response.text)['rows']:
            loader = ItemLoader(item=Product(), selector=row)
            cols = row['cell'][6]
            soupe = BeautifulSoup(cols, 'lxml')
            reformat_description = soupe.get_text()
            loader.add_value('title', reformat_description[-4:])
            loader.add_value('price', row['cell'][9])
            loader.add_value("balance", row['cell'][8])
            loader.add_value('description', reformat_description)
            loader.add_value('producer', row['cell'][13])
            loader.add_value('model_auto', reformat_description[-7:-3])
            loader.add_value('image', row['cell'][0])
            loader.add_value('image_alt', 'img_hex')
            loader.add_value('product_url', row['cell'][4])
            yield loader.load_item()
        page += 1
        if int(page) < int(total):
            yield scrapy.FormRequest(
                f'https://www.magistral-nn.ru/automag/?SECTION_ID=23483&getdata=true&nd=1616783290021&_search=true&nd=1616786082075&rows=50&page={page}&sidx=id&sord=asc&name=%D0%92%D0%90%D0%97',
                callback=self.parse, method='GET')
        print('=========  KONEC  ================')