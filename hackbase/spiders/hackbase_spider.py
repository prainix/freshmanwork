import scrapy
import re
import hashlib
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from hackbase.items import HackbaseItem


class HackbaseSpider(CrawlSpider):
    name = "hackbase"
    allowed_domains = ["bbs.hackbase.com"]
    start_urls = [
        "http://bbs.hackbase.com/forum.php?mod=forumdisplay&fid=1&page=1",
    ]

    rules = (
        
        Rule(SgmlLinkExtractor(allow=('forum\.php\?mod=viewthread.*', ), deny=('page=','action=','ordertype=' )), callback='parse_hackbase',follow=True),
        Rule(SgmlLinkExtractor(allow=('forum\.php\?mod=forumdisplay&fid=\d+&page=\d+', )), follow=True),
 

    )
    #Rule(SgmlLinkExtractor(allow=('forum\.php\?mod=viewthread.*page=\d+', )), callback='parse_hackbase_detail', follow=True),
    #Rule(SgmlLinkExtractor(allow=('home\.php\?mod=space&uid=\d+', )), callback='parse_hackbase_author', follow=False)

    def start_requests(self):
        return [Request(url="http://bbs.hackbase.com/member.php?mod=logging&action=login", callback=self.post_message)]
    
    def post_message(self, response):
        sel = response.selector
        formhash = sel.xpath('//input[@name="formhash"]/@value').extract()[0]
        seccodehash = sel.xpath('//span[re:test(@id, "seccode_.*")]/@id').extract()[0][8:]
    	return [scrapy.FormRequest.from_response(response, formdata={'formhash':formhash, 'referer':'http://bbs.hackbase.com/forum.php', 'username':'xeudyn', 'password':'69f250d147800a1cdec6da4bcc148aa3', 'questionid':'0','answer':'','seccodehash':seccodehash,'seccodemodid':'member::logging','seccodeverify':'','loginsubmit':'true'},callback=self.after_login)]

    def after_login(self, response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)




#    def parse_hackbase_author(self, response):
#    	item = AuthorItem()
#        meta_item = response.meta['item']
#        if meta_item is HackbaseItem :
#            item['auth_type'] = [1]
#        elif meta_item is DetailItem :
#            item['auth_type'] = [2]
#        sel = response.selector
#        auth_url = response.url
#        item['auth_id'] = [sel.xpath('//*[@id="ct"]/div[1]/div/div[2]/div/div[1]/h2/span').re('\d+')[1]]
#        item['auth_join_date'] = sel.xpath('//*[@id="pbbs"]/li[2]/text()').extract()
#        item['auth_post_num'] = sel.xpath('//*[@id="cl bbda pbm mbm"]/li/a[5]/text()').re('\d+')
#        item['auth_topic_num'] = sel.xpath('//*[@id="cl bbda pbm mbm"]/li/a[6]/text()').re('\d+')
#        item['auth_time'] = sel.xpath('//*[@id="pbbs"]/li[1]/text()').extract()
#        item['auth_level'] = sel.xpath('//em[@class="xg1"]/following-sibling::span[1]/a/text()').extract()
#        item['auth_value'] = sel.xpath('//*[@id="psts"]/ul/li[2]/text()').extract()
#        item['auth_money'] = sel.xpath('//*[@id="psts"]/ul/li[4]/text()').extract()
#        item['auth_reputation'] =sel.xpath('//*[@id="psts"]/ul/li[3]/text()').extract()
#        yield item

    def grabFloor(self, f, url):
        item = HackbaseItem()
        sel = Selector(text=f)
        item['url'] = url
        
#        'auth_join_date',
#        'auth_post_num',
#        'auth_topic_num',
#        'auth_time',
#        'auth_level',
#        'auth_value',
#        'auth_money',
#        'auth_reputation'
        
        item['post_id'] = [sel.xpath('//*[@id="pt"]/div/a[last()]').re('\d+')[0]]
        post_floor = sel.xpath('//*[re:test(@id, "postnum\d+")]/em/text()').extract()
        item['post_floor'] = post_floor

        if post_floor[0] == '1' :
            item['post_title'] = sel.xpath('//span[@id="thread_subject"]/text()').extract()
            view_and_reply = sel.xpath('//span[@class="xi1"]/text()').re('\d+')
            item['main_post_post_view'] = [view_and_reply[0]]
            item['main_post_post_reply'] = [view_and_reply[1]]
        else :
            pass
        item['post_date'] = sel.xpath('//*[re:test(@id, "authorposton\d+")]').re('\d{4}(-\d{1,2}){2} (\d{1,2}:){2}\d{1,2}')
        item['post_content'] = sel.xpath('//*[re:test(@id, "postmessage_\d+")]/div[1]/text()').extract()
        auth_id = sel.xpath('//a[@class="xw1"]').re('\d+')[0]
        item['auth_id'] = [auth_id]
        item['auth_name'] = [sel.xpath('//a[@class="xw1"]/text()').extract()[0]]
        auth_url = 'http://bbs.hackbase.com/home.php?mod=space&uid=' + auth_id + '&do=profile'
        yield item
        #yield Request(url=auth_url, meta={'item':item}, callback=self.parse_hackbase_author)

    #def add_coolie(self, request):
    #, process_request='add_cookie' 


    def parse_hackbase(self, response):
        #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
        #    f.write(response.body)

        print '-------------------------------------------------'
        print response.body
        print '-------------------------------------------------'
        sel1 = response.selector
        url = response.url

        #sel.xpath('//div[@class="tns xg2"]').extract()
        #hashlib.new("md5", "ks960613").hexdigest()
        for f in sel1.xpath('//div[re:test(@id, "post_\d+")]').extract() :
            item = HackbaseItem()
            sel = Selector(text=f)
            item['url'] = url
        
#        'auth_join_date',
#        'auth_post_num',
#        'auth_topic_num',
#        'auth_time',
#        'auth_level',
#        'auth_value',
#        'auth_money',
#        'auth_reputation'
        
            item['post_id'] = [sel1.xpath('//*[@id="pt"]/div/a[last()]').re('\d+')[0]]
            post_floor = sel.xpath('//*[re:test(@id, "postnum\d+")]/em/text()').extract()
            item['post_floor'] = post_floor
            if post_floor == False :
            	post_floor.append('0')
            elif post_floor[0] == '1' :
                item['post_title'] = sel1.xpath('//span[@id="thread_subject"]/text()').extract()
                view_and_reply = sel1.xpath('//span[@class="xi1"]/text()').re('\d+')
                item['post_view'] = [view_and_reply[0]]
                item['post_reply'] = [view_and_reply[1]]
            else :
                pass
            item['post_date'] = [sel.xpath('//*[re:test(@id, "authorposton\d+")]/text()').extract()[0][4:]]
            post_content = sel.xpath('//*[re:test(@id, "postmessage_\d+")]/div[1]/text()').extract()
            if post_content :
            	item['post_content'] = post_content
            else :
            	post_content = ['']
            auth_id_list = sel.xpath('//a[@class="xw1"]').re('\d+')
            if auth_id_list :
                auth_id = auth_id_list[0]
                item['auth_id'] = [auth_id]
                item['auth_name'] = [sel.xpath('//a[@class="xw1"]/text()').extract()[0]]
                auth_url = 'http://bbs.hackbase.com/home.php?mod=space&uid=' + auth_id + '&do=profile'
#                auth_join_date = 
#                auth_post_num = 
#                auth_topic_num = 
#                auth_time = 
#                auth_level = 
#                auth_value = 
#                auth_money = 
            else :
            	item['auth_id'] = ['']
            	item['auth_name'] = ['']
            	auth_join_date  = ['']
                auth_post_num = ['']
                auth_topic_num = ['']
                auth_time = ['']
                auth_level = ['']
                auth_value = ['']
                auth_money = ['']
            yield item
#re('\d{4}(-\d{1,2}){2} (\d{1,2}:){2}\d{1,2}')
#        	item = self.grabFloor(f,url)

        #yield Request(url=auth_url, meta={'item':item}, callback=self.parse_hackbase_author)

        #for f in sel.xpath('//div[re:test(@id, "post_\d+")]').extract()[1:] :
#        	yield grabFloor(f)

        #main_post_post_title = sel.xpath('//span[@id="thread_subject"]').re('(?<=<span id=\"thread_subject\">).*(?=<\/span>)')
        #item['main_post_post_title'] = [ustr.encode('utf-8') for ustr in main_post_post_title]

#    def parse_hackbase_detail(self, response):
#        sel = response.selector
#        for f in sel.xpath('//div[re:test(@id, "post_\d+")]').extract() :
#           yield grabFloor(f)
    
    #.re('(?<=<span id=\"thread_subject\">).*(?=<\/span>)')