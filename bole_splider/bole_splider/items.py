# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoleSpliderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()      #文章标题
    create_date = scrapy.Field()    #创建时间
    front_img_url = scrapy.Field()      #w文章封面图片
    prise_num = scrapy.Field()          #获赞数量
    comment_num = scrapy.Field()        #评论数量
    content = scrapy.Field()           #评论
