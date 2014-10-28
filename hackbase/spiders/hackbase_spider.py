import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from hackbase.items import HackbaseItem, DetailItem, AuthorItem


class HackbaseSpider(CrawlSpider):
    name = "hackbase"
    allowed_domains = ["bbs.hackbase.com"]
    start_urls = [
        "http://bbs.hackbase.com/forum.php?mod=forumdisplay&fid=1&page=1",
    ]

    rules = (
        
        Rule(SgmlLinkExtractor(allow=('forum\.php\?mod=viewthread.*', ), deny=('page=', )), callback='parse_hackbase',follow=True),
        Rule(SgmlLinkExtractor(allow=('forum\.php\?mod=forumdisplay&fid=\d+&page=\d+', )), follow=True),
        Rule(SgmlLinkExtractor(allow=('forum\.php\?mod=viewthread.*page=\d+', )), callback='parse_hackbase_detail', follow=True),

    )

    #Rule(SgmlLinkExtractor(allow=('home\.php\?mod=space&uid=\d+', )), callback='parse_hackbase_author', follow=False)

    def parse_hackbase(self, response):
        #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
        #    f.write(response.body)

        sel = response.selector
        url = response.url
        item = HackbaseItem()

        item['main_post_post_id'] = [re.match('\d+',url[53:]).group(0)]
        item['url'] = url
        item['main_post_post_title'] = sel.xpath('//span[@id="thread_subject"]/text()').extract()
        view_and_reply = sel.xpath('//span[@class="xi1"]/text()').re('\d+')
        item['main_post_post_view'] = [view_and_reply[0]]
        item['main_post_post_reply'] = [view_and_reply[1]]
        item['main_post_post_date'] = [sel.xpath('//em[re:test(@id, "authorposton.*")]/text()').extract()[0][4:]]
        item['main_post_post_content'] = [sel.xpath('//*[re:test(@id, "postmessage.*")]/div[1]/text()').extract()[0]]
        auth_id = sel.xpath('//a[@class="xw1"]').re('\d+')[0]
        item['main_post_auth_id'] = [auth_id]
        item['main_post_auth_name'] = [sel.xpath('//a[@class="xw1"]/text()').extract()[0]]
        auth_url = 'http://bbs.hackbase.com/home.php?mod=space&uid=' + auth_id + '&do=profile'

        yield item

        yield Request(url=auth_url, meta={'item':item}, callback=self.parse_hackbase_author)

        for f in sel.xpath('//div[re:test(@id, "post_\d+")]').extract()[1:] :
        	yield grabFloor(f)

        #main_post_post_title = sel.xpath('//span[@id="thread_subject"]').re('(?<=<span id=\"thread_subject\">).*(?=<\/span>)')
        #item['main_post_post_title'] = [ustr.encode('utf-8') for ustr in main_post_post_title]

    def parse_hackbase_detail(self, response):
        sel = response.selector
        for f in sel.xpath('//div[re:test(@id, "post_\d+")]').extract() :
           yield grabFloor(f)


    def parse_hackbase_author(self, response):
    	item = AuthorItem()
        meta_item = response.meta['item']
        if meta_item is HackbaseItem :
            item['auth_type'] = [1]
        elif meta_item is DetailItem :
            item['auth_type'] = [2]
        sel = response.selector
        auth_url = response.url
        item['auth_id'] = sel.xpath('//*[@id="ct"]/div[1]/div/div[2]/div/div[1]/h2/span').re('\d+')
        item['auth_join_date'] = sel.xpath('//*[@id="pbbs"]/li[2]/text()').extract()
        item['auth_post_num'] = sel.xpath('//*[@id="cl bbda pbm mbm"]/li/a[5]/text()').re('\d+')
        item['auth_topic_num'] = sel.xpath('//*[@id="cl bbda pbm mbm"]/li/a[6]/text()').re('\d+')
        item['auth_time'] = sel.xpath('//*[@id="pbbs"]/li[1]/text()').extract()
        item['auth_level'] = sel.xpath('//em[@class="xg1"]/following-sibling::span[1]/a/text()').extract()
        item['auth_value'] = sel.xpath('//*[@id="psts"]/ul/li[2]/text()').extract()
        item['auth_money'] = sel.xpath('//*[@id="psts"]/ul/li[4]/text()').extract()
        item['auth_reputation'] =sel.xpath('//*[@id="psts"]/ul/li[3]/text()').extract()
        yield item

    def grabFloor(self, f):
        item = DetailItem()
        sel = Selector(text=f)
        item['post_floor'] = sel.xpath('//*[re:test(@id, "postnum\d+")]/em/text()').extract()
        item['post_id'] = sel.xpath('//div[re:test(@id, "post_\d+")]').re('\d+')[0]
        item['post_date'] = sel.xpath('//*[re:test(@id, "authorposton\d+")]').re('\d{4}(-\d{1,2}){2} (\d{1,2}:){2}\d{1,2}')
        item['post_content'] = sel.xpath('//*[re:test(@id, "postmessage_\d+")]/div[1]/text()').extract()
        auth_id = sel.xpath('//a[@class="xw1"]').re('\d+')[0]
        item['auth_id'] = [auth_id]
        item['auth_name'] = [sel.xpath('//a[@class="xw1"]/text()').extract()[0]]
        auth_url = 'http://bbs.hackbase.com/home.php?mod=space&uid=' + auth_id + '&do=profile'
        yield item
        yield Request(url=auth_url, meta={'item':item}, callback=self.parse_hackbase_author)

    #def add_coolie(self, request):
    #, process_request='add_cookie' 
    
    #.re('(?<=<span id=\"thread_subject\">).*(?=<\/span>)')