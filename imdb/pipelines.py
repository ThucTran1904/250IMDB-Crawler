# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import sqlite3




class MongodbPipeline(object):
    collection_name = "best_movies"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://thuctran1:0905193063@cluster0.k7181.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["IMDB"]


    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item


class SQLlitePipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect("imdb.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE best_movies(
                    title TEXT,
                    year TEXT,
                    duration TEXT,
                    genre TEXT,
                    rating TEXT,
                    rating_count TEXT,
                    release_date TEXT,
                    movie_url TEXT
                )
            
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()


    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO best_movies (title,year,duration,genre,rating,rating_count,release_date,movie_url) VALUES(?,?,?,?,?,?,?,?)

        ''', (
            item.get('title'),
            item.get('year'),
            item.get('duration'),
            item.get('genre'),
            item.get('rating'),
            item.get('rating_count'),
            item.get('release_date'),
            item.get('movie_url')
        ))
        self.connection.commit()
        return item