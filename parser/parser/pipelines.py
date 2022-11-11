# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2

class SavingToPostgresPipeline(object):

    def __init__(self):
        self.create_connection()


    def create_connection(self):
        conn = psycopg2.connect(
            host="localhost",
            database="parsing_test",
            user="adinai_m",
            password="9817")


    def process_item(self, item, spider):
        self.store_db(item)
        #we need to return the item below as scrapy expects us to!
        return item

    def store_in_db(self, item):
        self.curr.execute(""" insert into chocolate_products values (%s,%s)""", (
            item[0],
            item[1],
        ))
        self.conn.commit()