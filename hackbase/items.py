# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HackbaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#    itemlist = [
#        'url',
#        'post_id',
#        'post_floor',
#        'post_title',
#        'post_view',
#        'post_reply',
#        'post_date',
#        'post_content',
#        'auth_id',
#        'auth_name',
#        'auth_type',
#        'auth_id',
#        'auth_url',
#        'auth_join_date',
#        'auth_post_num',
#        'auth_topic_num',
#        'auth_time',
#        'auth_level',
#        'auth_value',
#        'auth_money',
#        'auth_reputation'
#    ]
#    for i in itemlist:
#    	i = scrapy.Field()
    url = scrapy.Field()
    post_id = scrapy.Field()
    post_floor = scrapy.Field()
    post_title = scrapy.Field()
    post_view = scrapy.Field()
    post_reply = scrapy.Field()
    post_date = scrapy.Field()
    post_content = scrapy.Field()
    auth_id = scrapy.Field()
    auth_name = scrapy.Field()
    auth_url = scrapy.Field()
    auth_join_date = scrapy.Field()
    auth_post_num = scrapy.Field()
    auth_topic_num = scrapy.Field()
    auth_time = scrapy.Field()
    auth_level = scrapy.Field()
    auth_value = scrapy.Field()
    auth_money = scrapy.Field()
    auth_reputation = scrapy.Field()

