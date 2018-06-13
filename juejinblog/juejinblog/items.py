# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JuejinblogItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    uid = scrapy.Field()
    image = scrapy.Field()
    company = scrapy.Field()
    job = scrapy.Field()
    describle = scrapy.Field()
    follow = scrapy.Field()
    follower = scrapy.Field()
