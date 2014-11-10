import scrapy
import requests
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from hackbase.items import HackbaseItem



authors = {}

class HackbaseSpider(CrawlSpider):
    name = "hackbase"
    allowed_domains = ["bbs.hackbase.com"]
    start_urls = [
        "http://bbs.hackbase.com/forum.php?mod=forumdisplay&fid=1",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('forum\.php\?mod=viewthread&tid=.*', ), deny=('authorid=','action=','ordertype=','from=album' )), callback='parse_hackbase',follow=True),
        Rule(SgmlLinkExtractor(allow=('forum\.php\?mod=forumdisplay&fid=\d+&page=\d+', )), follow=True),
    )
    def start_requests(self):
    	scrapy.log.start(logfile='main.log', loglevel=scrapy.log.INFO, logstdout=None)
        return [Request(url="http://bbs.hackbase.com/member.php?mod=logging&action=login", callback=self.post_message)]
    
    def post_message(self, response):
        sel = response.selector
        formhash = sel.xpath('//input[@name="formhash"]/@value').extract()[0]
        seccodehash = sel.xpath('//span[re:test(@id, "seccode_.*")]/@id').extract()[0][8:]
        post_url = sel.xpath('//form[@name="login"]/@action').extract()[0]
        return [scrapy.FormRequest(url='http://bbs.hackbase.com/%s&inajax=1' % (post_url), formdata={'formhash':formhash, 'referer':'http://bbs.hackbase.com/forum.php', 'username':'xeudyn', 'password':'69f250d147800a1cdec6da4bcc148aa3', 'questionid':'0','answer':'','seccodehash':seccodehash,'seccodemodid':'member::logging','seccodeverify':'','loginsubmit':'true'},callback=self.after_login)]

    def after_login(self, response):
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print response.body.decode('gbk').encode('utf8')
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        for url in self.start_urls:
            yield self.make_requests_from_url(url)




    def parse_hackbase_author(self, response):
    	global authors
        item = response.meta['item']
        sel = response.selector

        auth_money = sel.xpath('//*[@id="psts"]/ul/li[4]/text()').re('\d*')
        if auth_money :
            item['auth_money'] = [auth_money[0]]

        else :
            item['auth_money'] = ['0']

        auth_reputation = sel.xpath('//*[@id="psts"]/ul/li[3]/text()').re('\d*')
        if auth_reputation :
            item['auth_reputation'] = [auth_reputation[0]]
        else :
            item['auth_reputation'] = ['0'] 

        auth_join_date = sel.xpath('//*[@id="pbbs"]/li[2]/text()').extract()

        if auth_join_date :
            pass
        else :
            auth_join_date = ['']
        item['auth_join_date'] = auth_join_date
        authors[item['auth_id'][0]] = (item['auth_money'], item['auth_reputation'], item['auth_join_date'])
        yield item

    def parse_hackbase(self, response):
        sel1 = response.selector
        url = response.url

        floor_list =sel1.xpath('//div[re:test(@id, "post_\d+")]').extract()
        for f in  floor_list:
            item = HackbaseItem()
            sel = Selector(text=f)
            item['url'] = url
        
            item['post_id'] = [sel1.xpath('//*[@id="pt"]/div/a[last()]').re('\d+')[0]]
            post_floor = sel.xpath('//*[re:test(@id, "postnum\d+")]/em/text()').extract()

            if post_floor :
                if post_floor[0] == '1' :
                    post_title = sel1.xpath('//span[@id="thread_subject"]/text()').extract()
                    if post_title:
                    	item['post_title'] = post_title
                    else:
                    	item['post_title'] = ['']
                    view_and_reply = sel1.xpath('//span[@class="xi1"]/text()').re('\d+')
                    item['post_view'] = [view_and_reply[0]]
                    item['post_reply'] = [view_and_reply[1]]
                else :
                    pass
            else :
                post_floor.append('0')
            item['post_floor'] = post_floor
            post_date = sel.xpath('//*[re:test(@id, "authorposton\d+")]/text()').extract()
            if post_date:
            	item['post_date'] = [post_date[0][4:]]
            else:
            	item['post_date'] = ['']
            post_content = sel.xpath('//*[re:test(@id, "postmessage_\d+")]/text()').extract()

            if post_content :
            	item['post_content'] = post_content
            else :
                item['post_content'] = ['']
            auth_id_list = sel.xpath('//a[@class="xw1"]').re('\d+')
            if auth_id_list :
                auth_id = auth_id_list[0]
                item['auth_id'] = [auth_id]
                item['auth_name'] = [sel.xpath('//a[@class="xw1"]/text()').extract()[0]]
                auth_url = 'http://bbs.hackbase.com/home.php?mod=space&uid=' + auth_id + '&do=profile'
                item['auth_post_num'] = sel.xpath('//a[re:test(@href, ".*uid=.*type=thread.*")]/text()').extract()
                auth_topic_num = sel.xpath('//a[re:test(@href, ".*uid=.*type=reply.*")]/text()').extract()

                if auth_topic_num:
                    item['auth_topic_num'] = auth_topic_num
                else:
                    item['auth_topic_num'] = sel.xpath('//a[re:test(@href, ".*uid=.*type=reply.*")]/span/@title').extract()
                item['auth_time'] = sel.xpath('//*[re:test(@id, "favatar\d+")]/dl[3]/dd/text()').extract()

                auth_level = sel.xpath('//a[re:test(@href, ".*usergroup.*")]/text()')
                if auth_level :
                    item['auth_level'] = sel.xpath('//a[re:test(@href, ".*usergroup.*")]/text()').extract()
                else :
                    item['auth_level'] = sel.xpath('//a[re:test(@href, ".*usergroup.*")]/font/text()').extract()

                auth_value = [sel.xpath('//a[re:test(@href, ".*mod=space.uid=\d+&do=profile")]/text()').extract()[0]]
                if auth_value:
                	item['auth_value'] = auth_value
                else:
                    item['auth_value'] = sel.xpath('//a[re:test(@href, ".*mod=space.uid=\d+&do=profile")]/span/@title').extract()

                if auth_id in authors:
                    (item['auth_money'], item['auth_reputation'], item['auth_join_date']) = authors[auth_id]
                    yield item
                else:
                    yield Request(url=auth_url, meta={'item':item}, callback=self.parse_hackbase_author)
            else :
            	#if post or author is baned
                item['auth_id'] = ['0']
                item['auth_name'] = ['']
                item['auth_join_date']  = ['']
                item['auth_post_num'] = ['0']
                item['auth_topic_num'] = ['0']
                item['auth_time'] = ['']
                item['auth_level']= ['']
                item['auth_value'] = ['0']
                item['auth_money'] = ['0']
                item['auth_reputation'] = ['0']
                yield item

            

