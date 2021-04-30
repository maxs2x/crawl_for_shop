# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,currentdir)
from spiders.distribution_categories import DistributionCategories


def remove_quotes(text):
    # strip the unicode comma
    text = text.strip(u'\u002C')
    text = text.strip(u'\xa0')
    return text


def database_distribution(categories):
    """
    :param arr: массив в котором первое значение категория навигайии в спршеном ресурсе,
    а второе - описание товара
    :return: если спаршеная категория есть в словаре distribution_incoming_categories - возвращается соответствующий ключ из словаря
    иначе в класс DistributionCategories передаётся описание товара и класс возвращает категорию которая соответствует описанию товара
    """
    my_categories = ['damper', 'springs', 'levers', 'bearings', 'steering',
                     'silent_blocks', 'ball_joints', 'ignition', 'sensor', 'wiring',
                     'gena', 'light', 'vacuum', 'brace_cylinder', 'brake_discs', 'brake_pads'
                     'caliper', 'GBC', 'timing_belt', 'intake_system', 'exhaust_system', 'motor_support',
                     'piston', 'stuff', 'front_bumper', 'back_bumper', 'door', 'hood', 'wing', 'nut'
                     'glass', 'gearbox_parts', 'actuator', 'clutch', 'gear', ]
    #incoming_categories = []
    distribution_incoming_categories = {'clutch': '16 - Сцепление', 'gearbox_parts': '17 - Коробка перемены передач',
                    'gear': '24 - Задний мост', 'exhaust_system': '12 - Система выпуска газов',
                    'stuff': '13 - Система охлаждения'}
    for categories_out, incoming_categories in distribution_incoming_categories.items():
        if incoming_categories in categories:
            return categories_out
    categories_out = DistributionCategories().distribution(categories)
    if not categories_out:
        categories_out = 'other'
    return categories_out



def sort_from_model(text):
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


class Product(Item):
    title = Field()
    price = Field()
    balance = Field()
    description = Field(
        input_processor=MapCompose(remove_quotes)
        )
    producer = Field()
    model_auto = Field()
    navigation_categories = Field(
        input_processor=MapCompose(database_distribution)
        )
    images = Field()
    image_alt = Field()
    image_urls = Field()
    product_url = Field()