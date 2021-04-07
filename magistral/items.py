# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose


def remove_quotes(text):
    # strip the unicode comma
    text = text.strip(u'\u002C')
    return text


class Product(Item):
    title = Field()
    price = Field()
    balance = Field()
    description = Field(
        input_processor=MapCompose(remove_quotes)
        )
    producer = Field()
    model_auto = Field()
    navigation_categories = Field()
    image = Field()
    image_alt = Field()
    product_url = Field()