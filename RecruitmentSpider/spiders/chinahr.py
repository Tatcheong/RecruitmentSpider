import re

from scrapy import Spider, Request


class ChinahrSpider(Spider):
    name = 'chinahr'
    allowed_domains = ['www.chinahr.com']
    start_urls = [
        'http://j1.58cdn.com.cn/git/hrg-fe-zhaopin-chinahr/chinahr-job-category-pc/static/js/job_category_v20201123150542.js']
    base_url = 'https://www.chinahr.com/channel'

    def parse(self, response, **kwargs):
        city_dict = re.search('city:{.*?}}}', response.text, re.S).group(0)
        city_list = re.findall(r':\"(.*?)\|\d+\"', city_dict)
        for city in city_list:
            yield Request(url=f'{self.base_url}/{city}/', callback=self.parse_city)

    @staticmethod
    def parse_city(response):
        job_url_list = response.xpath('//div[@class="assortment_left_wrap"]/ul/li/div/a')
        for job_url in job_url_list:
            print(job_url.xpath('@href').extract_first(''))
