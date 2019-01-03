# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from bole_splider.items import BoleSpliderItem
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import datetime
import re

class ExampleSpider(scrapy.Spider):
    name = 'bole'  #爬虫名字
    allowed_domains = ['blog.jobbole.com']  #错误原因:  http://blog.jobbole.com
    #allowed_domains中域名设置问题, Request需要的是一组域名而不是一组url
    start_urls = ['http://blog.jobbole.com/all-posts/']
    page_num=0

    #收集伯乐在线所有404的url以及404页面
    handle_httpstatus_list=[404]

    def __init__(self,**kwargs):
        self.fail_urls=[]
        dispatcher.connect(self.handle_splider_closed,signals.spider_closed)

    def handle_splider_closed(self,splider,reason):
        self.crawler.status.set_value("failed_urls",",".join(self.fail_urls))
    #开始的URL
    def parse(self, response):
        filename = "E://Python//爬虫//分布式爬虫-scrapy//bole_splider//输出.txt"
        with open(filename, 'wb') as f:
            f.write(response.body)
            f.close()
        post_nodes = response.xpath('//*[@id="archive"]/div/div[1]/a')
        for post_node in post_nodes:
            img_url = post_node.xpath('img/@src').extract_first('')   #获取文章的封面图片
            article_url = post_node.xpath('@href').extract_first('')  # 获取文章链接
            print("1")
            yield Request(
                url=parse.urljoin(response.url, article_url),
                # urljoin   是补全缺失的url
                meta={'front_img_url': img_url},
                # meta 是文章封面url
                callback=self.parse_detail
                # 回调函数，对回调函数调用：调用程序发出对回调函数的调用后，
                # 不等函数执行完毕，立即返回并继续执行。
                # 这样，调用程序执和被调用函数同时在执行。
                # 当被调函数执行完毕后，被调函数会反过来调用某个事先指定函数，
                # 以通知调用程序：函数调用结束。
            )
            """
            img_url2 = post_node.xpath('img/@src').extract()
            img_url2 === ['http://jbcdn2.b0.upaiyun.com/2018/12/93677bc0c5d849ca25cf8f39eeca8085.png']
            
            img_url3 = post_node.xpath('img/@src').extract_first()
            img_url4 = post_node.xpath('img/@src').extract_first('')
            img_url5 = post_node.xpath('img/@src').extract()[0]
            img_url3,4,5 === http://jbcdn2.b0.upaiyun.com/2018/12/93677bc0c5d849ca25cf8f39eeca8085.png
    
            print(img_url1,img_url2,img_url3,img_url4,img_url5)
            """
        next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first('')
        if self.page_num<5:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
            self.page_num +=1
        """if next_url:
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)"""
    def parse_detail(self,response):#response，是article_url，该函数是对article_url进行解析
        print("2")
        article_item = BoleSpliderItem()
        front_img_url = response.meta.get("front_img_url",'')   #文章封面图
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('')
        create_time = response.xpath('//div[@class="entry-meta"]/p/text()').extract_first('').strip().replace("·","").strip()
        prise_num = response.xpath('//div[@class="post-adds"]/span/h10/text()').extract_first('')
        comment_num=response.xpath('//div[@class="post-adds"]/a/span/text()').extract_first('')
        content = response.xpath('//div[@class="entry"]/p/text()').extract_first('')

        #将这些数据稍加处理，加入item中
        article_item['title'] = title
        article_item['front_img_url']=front_img_url

        """try:
            create_times = datetime.datetime.strptime(create_time,"%Y%m%d").date()
        except:
            create_times = datetime.datetime.now().date()
        #将时间转换为date格式"""
        article_item['create_date'] = create_time

        match_re = re.match(r'.*?(\d+).*',comment_num)
        #对comment_num进行判断，若为空，则评论数量为0
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums=0

        article_item['comment_num'] = comment_nums
        article_item['content']="content"

        yield article_item



