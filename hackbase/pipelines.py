# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

connection = sqlite3.connect('main_post.db')
cu = connection.cursor()
connection.execute('''CREATE TABLE IF NOT EXISTS main_post
       (post_id INT PRIMARY KEY   NOT NULL,
       post_title TEXT,
       post_view TEXT,
       post_reply TEXT,
       post_date TEXT,
       post_content TEXT,
       auth_id TEXT,
       auth_name TEXT,
       auth_join_date TEXT,
       auth_post_num TEXT,
       auth_topic_num TEXT,
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
       auth_id TEXT,
       auth_name TEXT,
       auth_join_date TEXT,
       auth_post_num TEXT,
       auth_topic_num TEXT,
       auth_time TEXT,
       auth_level TEXT,
       auth_value TEXT,
       auth_money TEXT,
       auth_reputation TEXT, 
       PRIMARY KEY (post_floor, post_id));''')

connection.execute('''CREATE TABLE IF NOT EXISTS what_the_post_detail
       (post_id INT PRIMARY KEY   NOT NULL,
       post_date TEXT,
       post_content TEXT,
       auth_id TEXT,
       auth_name TEXT,
       auth_join_date TEXT,
       auth_post_num TEXT,
       auth_topic_num TEXT,
       auth_time TEXT,
       auth_level TEXT,
       auth_value TEXT,
       auth_money TEXT,
       auth_reputation TEXT);''')

class HackbasePipeline(object):

#	def __init__(self):

    def process_item(self, item, spider):
        global connection
        global cu
        if item['post_floor'][0] == u'1':
        	#main post
            sqlex0 = "SELECT * FROM main_post WHERE post_id=%d" % int(item['post_id'][0])
            cu.execute(sqlex0)
            cuf = cu.fetchall()
            if len(cuf) == 0:
                sqlex = "INSERT INTO main_post (post_id, post_title, post_view, post_reply, post_date, post_content, auth_id, auth_name,auth_join_date,auth_post_num,auth_topic_num,auth_time,auth_level,auth_value,auth_money,auth_reputation) VALUES (%d, \'%s\', \'%s\', \'%s\',\'%s\', \'%s\', \'%s\', \'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\') " % (int(item['post_id'][0]),item['post_title'][0].replace('\'','\'\''),item['post_view'][0],item['post_reply'][0],item['post_date'][0],''.join(item['post_content']).replace('\'','\'\''),item['auth_id'][0],item['auth_name'][0].replace('\'','\'\''),item['auth_join_date'][0],item['auth_post_num'][0],item['auth_topic_num'][0],item['auth_time'][0],item['auth_level'][0],item['auth_value'][0],item['auth_money'][0],item['auth_reputation'][0])
                connection.execute(sqlex)
                connection.commit()
            else:
                pass

        elif item['post_floor'][0] == u'0':
            #recommand floor
            sqlex0 = "SELECT * FROM what_the_post_detail WHERE post_id=%d" % int(item['post_id'][0])
            cu.execute(sqlex0)
            cuf = cu.fetchall()
            if len(cuf) == 0:
                sqlex = "INSERT INTO what_the_post_detail (post_id, post_date, post_content, auth_id, auth_name,auth_join_date,auth_post_num,auth_topic_num,auth_time,auth_level,auth_value,auth_money,auth_reputation) VALUES (%d, \'%s\', \'%s\', \'%s\', \'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (int(item['post_id'][0]),item['post_date'][0],''.join(item['post_content']).replace('\'','\'\''),item['auth_id'][0],item['auth_name'][0].replace('\'','\'\''),item['auth_join_date'][0],item['auth_post_num'][0],item['auth_topic_num'][0],item['auth_time'][0],item['auth_level'][0],item['auth_value'][0],item['auth_money'][0],item['auth_reputation'][0])
                connection.execute(sqlex)
                connection.commit()
            else:
                pass
        else:
            sqlex0 = "SELECT * FROM post_detail WHERE post_id=%d and post_floor=%d" % (int(item['post_id'][0]),int(item['post_floor'][0]))
            cu.execute(sqlex0)
            cuf = cu.fetchall()
            if len(cuf) == 0:
                sqlex = "INSERT INTO post_detail (post_floor, post_id, post_date, post_content, auth_id, auth_name,auth_join_date,auth_post_num,auth_topic_num,auth_time,auth_level,auth_value,auth_money,auth_reputation) VALUES (%d, %d, \'%s\', \'%s\', \'%s\', \'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (int(item['post_floor'][0]),int(item['post_id'][0]),item['post_date'][0],''.join(item['post_content']).replace('\'','\'\''),item['auth_id'][0],item['auth_name'][0].replace('\'','\'\''),item['auth_join_date'][0],item['auth_post_num'][0],item['auth_topic_num'][0],item['auth_time'][0],item['auth_level'][0],item['auth_value'][0],item['auth_money'][0],item['auth_reputation'][0])
                connection.execute(sqlex)
                connection.commit()
            else:
            	pass

        return item

    def close_spider(self, spider):
    	global connection
    	connection.close()

