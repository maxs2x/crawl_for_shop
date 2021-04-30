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
        SECTION_ID = ['23483', '23484', '23485', '23486', '23487', '23488', '23489', '23490', '23491', '23492',
                      '23496', '23497', '23498', '23512', '23513', '23522', '23523', '23524', '23525', '23526', '23527', '23528', '23529']
        for param in SECTION_ID:
            yield scrapy.FormRequest(f'https://www.magistral-nn.ru/automag/?SECTION_ID={param}&getdata=true&nd=1616783290021&_search=true&nd=1616786082075&rows=50&page=1&sidx=id&sord=asc&name=%D0%92%D0%90%D0%97',
                                     callback=self.parse, method='GET')

    def build_images_url(self, text):
        full_url = 'https://www.magistral-nn.ru' + text
        return full_url

    def parse(self, response):
        page = json.loads(response.text)['page']
        total = json.loads(response.text)['total']
        navigation_categories = json.loads(response.text)['cat']
        for row in json.loads(response.text)['rows']:
            loader = ItemLoader(item=Product(), selector=row)
            cols = row['cell'][6]
            soupe = BeautifulSoup(cols, 'lxml')
            if row['cell'][0]:
                part_url_big_img = BeautifulSoup(row['cell'][0], 'lxml').select('span')[0]['data-dp']
                full_url_big_img = self.build_images_url(part_url_big_img)
                name_image = part_url_big_img.strip('/upload/prod_images/catalog/')[:-2]
            else:
                full_url_big_img = 'NONE'
                name_image = 'NONE'
            reformat_description = soupe.get_text()
            categories = str(navigation_categories) + str(reformat_description)
            print('input ITEM')
            print(categories)
            loader.add_value('title', reformat_description[-4:])
            loader.add_value('price', row['cell'][9])
            loader.add_value('balance', row['cell'][8])
            loader.add_value('description', reformat_description)
            loader.add_value('producer', row['cell'][13])
            loader.add_value('model_auto', reformat_description[-7:-3])
            loader.add_value('navigation_categories', categories)
            #loader.add_value('images', row['cell'][0])
            loader.add_value('image_alt', 'img_hex')
            loader.add_value('image_urls', full_url_big_img)
            loader.add_value('product_url', name_image)
            yield loader.load_item()
        page += 1
        if int(page) < 2:
            yield scrapy.FormRequest(
                f'https://www.magistral-nn.ru/automag/?SECTION_ID=23483&getdata=true&nd=1616783290021&_search=true&nd=1616786082075&rows=50&page={page}&sidx=id&sord=asc&name=%D0%92%D0%90%D0%97',
                callback=self.parse, method='GET')
        print('=========  KONEC  ================')