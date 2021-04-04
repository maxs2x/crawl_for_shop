# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose


class MagistralItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Product(Item):
    title = Field()
    price = Field()
    balance = Field()
    description = Field()
    producer = Field()
    model_auto = Field()
    navigation_categories = Field()
    image = Field()
    image_alt = Field()
    product_url = Field()