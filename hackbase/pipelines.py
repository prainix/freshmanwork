# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

connection = sqlite3.connect('main_post.db')
connection.execute('''CREATE TABLE IF NOT EXISTS main_post
       (post_id INT PRIMARY KEY   NOT NULL,
       post_title TEXT,
       post_view INT,
       post_reply INT,
       post_date TEXT,
       post_content TEXT,
       auth_id INT,
       auth_name TEXT,
       auth_join_date TEXT,
       auth_post_num INT,
       auth_topic_num INT,
       auth_time TEXT,
       auth_level TEXT,
       auth_value TEXT,
       auth_money TEXT,
       auth_reputation TEXT);''')

connection.execute('''CREATE TABLE IF NOT EXISTS post_detail
       (post_floor INT NOT NULL,
       post_id INT NOT NULL,
       post_date TEXT,
       post_content TEXT,
       auth_id INT,
       auth_name TEXT,
       auth_join_date TEXT,
       auth_post_num INT,
       auth_topic_num INT,
       auth_time TEXT,
       auth_level TEXT,
       auth_value TEXT,
       auth_money TEXT,
       auth_reputation TEXT, 
       PRIMARY KEY (post_floor, post_id));''')

class HackbasePipeline(object):

#	def __init__(self):

    def process_item(self, item, spider):
        global connection
        if item is HackbaseItem :
            connection.execute("INSERT INTO main_post (post_id, post_title, post_view, post_reply, post_date, post_content, auth_id, auth_name) VALUES (%d, %s, %d, %d, %s, %s, %d, %s)" % (int(item['main_post_post_id'][0]),item['main_post_post_title'][0],int(item['main_post_post_view'][0]),int(item['main_post_post_reply'][0]),item['main_post_post_date'][0],item['main_post_post_content'][0],int(item['main_post_auth_id'][0]),item['main_post_auth_name'][0]))
            connection.commit()

        if item is DetailItem :
            connection.execute("INSERT INTO post_detail (post_floor, post_id, post_date, post_content, auth_id, auth_name) VALUES (%d, %d, %s, %s, %d, %s,)" % (int(item['post_floor'][0]),int(item['post_id'][0]),item['post_date'][0],item['post_content'][0],int(item['auth_id'][0]),item['auth_name'][0]))
            connection.commit()

        if item is AuthorItem :
            if item['auth_type'][0] == 1:
                connection.execute("UPDATE main_post SET auth_join_date=%s, auth_post_num=%d, auth_topic_num=%d, auth_time=%s, auth_value=%d, auth_level=%s, auth_money=%d, auth_reputation=%d WHERE auth_id=%d" % (item['auth_join_date'][0],int(item['auth_post_num'][0]),int(item['auth_topic_num'][0]),item['auth_time'][0],int(item['auth_value'][0]),item['auth_level'][0],int(item['auth_money'][0]),inti(tem['auth_reputation'][0]),int(item['auth_id'][0])))
                connection.commit()
            elif item['auth_type'][0] == 2:
            	connection.execute("UPDATE post_detail SET auth_join_date=%s, auth_post_num=%d, auth_topic_num=%d, auth_time=%s, auth_value=%d, auth_level=%s, auth_money=%d, auth_reputation=%d WHERE auth_id=%d" % (item['auth_join_date'][0],int(item['auth_post_num'][0]),int(item['auth_topic_num'][0]),item['auth_time'][0],int(item['auth_value'][0]),item['auth_level'][0],int(item['auth_money'][0]),inti(tem['auth_reputation'][0]),int(item['auth_id'][0])))
                connection.commit()
                connection.commit()
        return item

#UPDATE COMPANY set SALARY = 25000.00 where ID=1

    def close_spider(spider):
    	global connection
    	connection.close()