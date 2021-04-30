# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os
from urllib.parse import urlparse
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker
from scrapy.pipelines.images import ImagesPipeline
from magistral.models import db_connect, create_table, Suspension


class SaveProductPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        session = self.Session()
        suspension = Suspension()
        suspension.title = item["title"][0]
        suspension.price = item["price"][0]
        suspension.balance = item["balance"][0]
        suspension.description = item["description"][0]
        suspension.producer = item["producer"][0]
        suspension.model_auto = item["model_auto"][0]
        suspension.images = item["images"][0]
        suspension.image_alt = item["image_alt"][0]
        suspension.product_url = item["product_url"][0]
        suspension.navigation_categories = item["navigation_categories"][0]

        try:
            session.add(suspension)
            session.commit()
            print('===============++++++++++++++++++==========================================================')
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item


class DuplicatesPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        exist_product = session.query(Suspension).filter_by(description=str(item["description"][0])).first()
        if exist_product is not None:  # the current quote exists
            raise DropItem("Duplicate item found: %s" % item["description"])
            session.close()
        else:
            return item
            session.close()


class SaveImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def file_path(self, request, response=None, info=None, *, item=None):
        return 'files/' + os.path.basename(urlparse(request.url).path)

