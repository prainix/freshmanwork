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
	#main_post_auth_id = scrapy.Field()
	#main_post_auth_name = scrapy.Field()
	#main_post_auth_join_date = scrapy.Field()
	#main_post_auth_post_num = scrapy.Field()
	#main_post_auth_topic_num = scrapy.Field()
	#main_post_auth_time = scrapy.Field()
	#main_post_auth_level = scrapy.Field()
	#main_post_auth_value = scrapy.Field()
	#main_post_auth_money = scrapy.Field()
	#main_post_auth_reputation = scrapy.Field()
	#或优化












