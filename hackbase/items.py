# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HackbaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    main_post_post_id = scrapy.Field()
    main_post_post_title = scrapy.Field()
    main_post_post_view = scrapy.Field()
    main_post_post_reply = scrapy.Field()
    main_post_post_date = scrapy.Field()
    main_post_post_content = scrapy.Field()
    main_post_auth_id = scrapy.Field()
    main_post_auth_name = scrapy.Field()
    #或优化

class AuthorItem(scrapy.Item):
	# define the fields for your item here like:
    # name = scrapy.Field()
    auth_type = scrapy.Field()
    auth_id = scrapy.Field()
    auth_url = scrapy.Field()
    auth_join_date = scrapy.Field()
    auth_post_num = scrapy.Field()
    auth_topic_num = scrapy.Field()
    auth_time = scrapy.Field()
    auth_level = scrapy.Field()
    auth_value = scrapy.Field()
    auth_money = scrapy.Field()
    auth_reputation = scrapy.Field()


class DetailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    post_floor = scrapy.Field()
    post_id = scrapy.Field()
    post_date = scrapy.Field()
    post_content = scrapy.Field()
    auth_id = scrapy.Field()
    auth_name = scrapy.Field()