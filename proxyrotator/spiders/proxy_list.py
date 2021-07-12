# -*- coding: utf-8 -*-
import scrapy
from random import choice
import logging


class ProxyListSpider(scrapy.Spider):
    name = 'proxy_list'
    allowed_domains = ['sslproxies.org','httpbin.org']
    start_urls = ['https://sslproxies.org']

    def parse(self, response):
        blocks = response.xpath("//table[@id='proxylisttable']/tbody/tr")
        complete_ips = []
        for x in blocks:
            ip_address = str(x.xpath(".//td[1]").get()).replace("<td>",'').replace("</td>",'')
            port = str(x.xpath(".//td[2]").get()).replace("<td>",'').replace("</td>",'')

            final_ip = ("%s:%s"%(ip_address,port))
            complete_ips.append(final_ip)

        for r in range(1,60):
            https = choice(complete_ips)
            yield scrapy.Request(url='https://httpbin.org/ip',callback=self.data_scraper,meta={"proxy":https},dont_filter=True)

    def data_scraper(self,response):
        logging.info(response.body)