# -*- coding: utf-8 -*-
import scrapy
from items import NewspItem


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for item in movie_list:
            douban_item = NewspItem()
            douban_item['number'] = item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['name'] = item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            introduce_info = item.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
            for introduce_item in introduce_info:
                douban_item['introduce'] = "".join(introduce_item.split())
            douban_item['star'] = item.xpath(
                ".//div[@class='info']/div[@class='bd']//div[@class='star']/span[2]/text()").extract_first()
            douban_item['evaluate'] = item.xpath(
                ".//div[@class='info']/div[@class='bd']//div[@class='star']/span[4]/text()").extract_first()
            douban_item['describe'] = item.xpath(
                ".//div[@class='info']/div[@class='bd']/p[@class='quote']/span/text()").extract_first()
            yield douban_item
        next_link = response.xpath(".//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse)
