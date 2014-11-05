# -*- coding: utf-8 -*-

# Scrapy settings for hackbase project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'hackbase'

SPIDER_MODULES = ['hackbase.spiders']
NEWSPIDER_MODULE = 'hackbase.spiders'

DOWNLOAD_DELAY = 0.05
RANDOMIZE_DOWNLOAD_DELAY = True

#COOKIES_ENABLED = True
DEPTH_LIMIT = 0
#CONCURRENT_ITEMS = 1000


ITEM_PIPELINES = ['hackbase.pipelines.HackbasePipeline']

DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hackbase (+http://www.yourdomain.com)'
