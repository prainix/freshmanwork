import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from hackbase.items import HackbaseItem


class HackbaseSpider(CrawlSpider):
    name = "hackbase"
    allowed_domains = ["bbs.hackbase.com"]
    start_urls = [
        "http://bbs.hackbase.com/forum.php?mod=forumdisplay&fid=1&page=1",
    ]

    rules = (
        
        Rule(LinkExtractor(allow=('forum\.php\?mod=viewthread.*', ), deny=('page=', )), callback='parse_hackbase', process_request='add_cookie'),
        #Rule(SgmlLinkExtractor(allow=('forum\.php\?mod=forumdisplay&fid=\d+&page=\d+', )), follow=True),
    )

    def parse_hackbase(self, response):
        #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
        #    f.write(response.body)

        sel = response.selector
        #url = response.url
        item = HackbaseItem()

        #item['main_post_post_id'] = re.match('(?<=&tid)\d+',url).group(0)
        item['url'] = response.url
        item['main_post_post_title'] = sel.xpath('//span[@id="thread_subject"]/text()').extract()
        view_and_reply = sel.xpath('//span[@class="xi1"]/text()').re('\d+')
        item['main_post_post_view'] = [view_and_reply[0]]
        item['main_post_post_reply'] = [view_and_reply[1]]
        item['main_post_post_date'] = [sel.xpath('//em[re:test(@id, "authorposton.*")]/text()').extract()[0][4:]]
        item['main_post_post_content'] = [sel.xpath('//td[re:test(@id, "postmessage.*")]/text()').extract()[0]]



        #main_post_post_title = sel.xpath('//span[@id="thread_subject"]').re('(?<=<span id=\"thread_subject\">).*(?=<\/span>)')
        #item['main_post_post_title'] = [ustr.encode('utf-8') for ustr in main_post_post_title]
        return item

    #def add_coolie(self, request):
    
    #.re('(?<=<span id=\"thread_subject\">).*(?=<\/span>)')

    