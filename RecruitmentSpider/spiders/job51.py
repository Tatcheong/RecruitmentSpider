import json
import re
from datetime import datetime, timedelta

from scrapy import Spider, Request

from RecruitmentSpider.items import Job51Item


class Job51Spider(Spider):
    name = 'job51'
    allowed_domains = ['search.51job.com', 'jobs.51job.com']
    start_urls = 'https://search.51job.com/list/000000,000000,0000,00,9,99,大数据,2,{}.html?'

    @staticmethod
    def crawl_time(format_str='%Y-%m-%d %H:%M:%S'):
        return datetime.now().strftime(format_str)

    def start_requests(self):
        yield Request(url=self.start_urls.format(1))

    def parse(self, response, **kwargs):
        item = Job51Item()
        page = response.meta.get('page', 1)
        job_json = re.search('window.__SEARCH_RESULT__ = (.*?)</script>', response.text).group(1)
        job_list = json.loads(job_json).get('engine_search_result', [])
        # 判断是否为最后一页
        if len(job_list) == 0:
            return

        for job in job_list:
            # 工作名
            job_name = job.get('job_name')
            if '数据' not in job_name:
                break
            item['job_name'] = job_name
            # 公司链接
            item['company_href'] = job.get('company_href')
            # 公司名
            item['company_name'] = job.get('company_name')
            # 公司规模
            item['companysize_text'] = job.get('companysize_text')
            # 公司业务
            item['industryField'] = job.get('companyind_text')
            # 公司业务
            item['companytype_text'] = job.get('companytype_text')
            # 工作经验
            item['experience'] = job.get('attribute_text')[1]
            # 更新时间
            issuedate = job.get('issuedate')
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            # 仅爬取昨天更新的内容
            if not yesterday in issuedate:
                break
            item['issuedate'] = issuedate
            # 工作链接
            job_href = job.get('job_href')
            item['job_href'] = job_href
            # 公司待遇
            item['jobwelf'] = job.get('jobwelf')
            # 工资
            item['providesalary_text'] = job.get('providesalary_text')
            # 工作地点
            item['workarea_text'] = job.get('workarea_text')

            yield Request(url=job_href, callback=self.parse_job, meta={'item': item.copy()})

        yield Request(url=self.start_urls.format(page + 1), callback=self.parse, meta={'page': page + 1})

    def parse_job(self, response):
        item = response.meta['item']
        job_info_list = response.xpath('//div[@class="bmsg job_msg inbox"]/p')
        # 详细职位信息写入文件
        job_info = ''
        for info in job_info_list:
            job_info += info.xpath('text()').extract_first('')
        item['job_info'] = job_info
        # with open('job_info.txt', 'a', encoding='utf-8') as file:
        #     file.write(job_info + '\n')
        # 关键字
        job_keyword = re.findall(r'welfare=">(.*?)</a>', response.text, re.S)
        item['job_keyword'] = '/'.join(job_keyword)
        # 爬取时间
        item['crawl_time'] = self.crawl_time()

        yield item
