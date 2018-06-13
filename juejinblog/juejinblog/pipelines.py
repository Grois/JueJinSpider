# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.connections
from datetime import datetime as dt


class JuejinblogPipeline(object):

    def __init__(self):
        self.db = pymysql.connect(host="localhost", user="root",
                                  password="root", db="juejin")
        self.cur = self.db.cursor()
        self.db.set_charset('utf8mb4')
        self.cur.execute('SET NAMES utf8mb4')
        self.cur.execute('SET CHARACTER SET utf8mb4')
        self.cur.execute('SET character_set_connection=utf8mb4')

    def process_item(self, item, spider):
        self.save_user(item)
        return item

    def save_user(self, user):
        # print(word)
        now_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = 'INSERT INTO `juejin`.`users`(`name`,`uid`,`image`,`company`,`job`,`describle`,`follow`,`follower`,`add_time`)VALUES("' + \
              user['name'] + '","' + user['uid'] + '","' + user['image'] + '","' + self.db.escape_string(user['company']) + '","' + user[
                  'job'] + '","' + user['describle'] + '","' + user['follow'] + '","' + user[
                  'follower'] + '","' + now_date + '")'
        # print(sql)
        self.cur.execute(sql)
        self.db.commit()
