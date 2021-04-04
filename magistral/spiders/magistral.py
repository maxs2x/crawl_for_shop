# -*- coding: utf-8 -*-
import scrapy
import json
from bs4 import BeautifulSoup
from magistral.items import Product
from scrapy.loader import ItemLoader



product_item = Product()


class MagistralSpider(scrapy.Spider):
    name = 'magistral'
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
            cols = row['cell'][6]
            soupe = BeautifulSoup(cols, 'lxml')
            reformat_description = self.sort_in_model(soupe.get_text())
            item['description'] = reformat_description[1]
            item['model_auto'] = reformat_description[0]
            item['price'] = row['cell'][9]
            item['producer'] = row['cell'][13]
            yield item
        page += 1
        if int(page) < int(total):
            yield scrapy.FormRequest(f'https://www.magistral-nn.ru/automag/?SECTION_ID=23483&getdata=true&nd=1616783290021&_search=true&nd=1616786082075&rows=50&page={page}&sidx=id&sord=asc&name=%D0%92%D0%90%D0%97',
                                     callback=self.parse, method='GET')
        else:
            print('=========  KONEC  ================')