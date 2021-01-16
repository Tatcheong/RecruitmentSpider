from datetime import datetime, timedelta

from scrapy import Spider
from scrapy.http import JsonRequest, Request

from RecruitmentSpider.items import lagouItem


class LagouSpider(Spider):
    name = 'lagou'
    allowed_domains = ['gate.lagou.com']

    api_url = 'https://gate.lagou.com/v1/entry/positionsearch/searchPosition'

    company_href = 'https://m.lagou.com/gongsi/{}.html'

    company_api = 'https://gate.lagou.com/v1/entry/bigCompany/query?companyId='

    job_href = 'https://app.lagou.com/share/position.html?userId={}&positionId={}'

    job_api = 'https://gate.lagou.com/v1/entry/position/jd?positionId={}&isCInspectB=1'

    headers = {
        'x-l-req-header': '{"userToken":"475a50abbbbed97ec3d6dd7b62205e8081397a751cdce7cf5946b2ebe5c265e2","reqVersion":71000,"lgId":"990000000057390_1610420455506","appVersion":"7.10.1","userType":0,"deviceType":200}',
        'x-l-janus-strategy': '{"strategies":[{"key":"position_card","value":"A"},{"key":"APP_RESUME_FLOW_21","value":"B"}]',
        'content-type': 'application/json;charset=utf-8',
        'accept-encoding': 'gzip',
        'user-agent': 'okhttp/3.11.0'
    }

    data = {
        "aggregateLevel": 0, "businessZone": "", "city": "全国", "district": "", "hiTag": "", "isAd": "0",
        "isSchoolJob": 'false', "keyword": "大数据", "keywordSource": 0, "lastShowCompanyId": 0, "latitude": "",
        "latitudeHigh": "", "latitudeLow": "", "longitude": "", "longitudeAndLatitude": "", "longitudeHigh": "",
        "longitudeLow": "", "mapLeveL": 0, "nearByKilometers": "", "pageNo": 0, "pageSize": 15,
        "refreshHiTagList": 'true', "salaryLower": 0, "salaryUpper": 0, "searchType": "",
        "shieldDeliveyCompany": 'false',
        "showId": "", "sort": 0, "subwayLineName": "", "subwayStation": "", "tagType": 0
    }

    @staticmethod
    def format_date(timestamp: int):
        date = datetime.fromtimestamp(timestamp)
        return date.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def crawl_time(format_str='%Y-%m-%d %H:%M:%S'):
        return datetime.now().strftime(format_str)

    def start_requests(self):
        for page in range(1000):
            self.data['pageNo'] = page
            temp = JsonRequest(url=self.api_url, headers=self.headers, data=self.data, callback=self.parse,
                               dont_filter=True)
            yield temp

    def parse(self, response, **kwargs):
        """
        提取工作的主要信息
        """
        item = lagouItem()
        result_dict = response.json()
        job_list = result_dict.get('content', '').get('positionCardVos', '')
        # 判断是否为最后一页
        if not isinstance(job_list, list):
            return
        for job in job_list:
            # 工作名
            item['job_name'] = job.get('positionName')
            # 公司链接
            company_id = str(job.get('companyId'))
            item['company_href'] = self.company_href.format(company_id)
            # 公司名
            item['company_name'] = job.get('companyName')
            # 公司规模
            item['companysize_text'] = job.get('companySize')
            # 公司类型
            item['industryField'] = job.get('industryField').replace(',', '/')
            # 工作经验
            item['experience'] = job.get('workYear')
            # 更新时间
            timestamp = job.get('createTime') / 1000
            issuedate = self.format_date(timestamp)
            # 仅爬取昨天更新的内容
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            if not yesterday in issuedate:
                break
            item['issuedate'] = issuedate
            # 工作链接
            user_id = job.get('hrId')
            position_id = job.get('positionId')
            item['job_href'] = self.job_href.format(user_id, position_id)
            # 工资
            item['providesalary_text'] = job.get('salary')
            # 关键字
            job_keyword = job.get('positionLabels')
            item['job_keyword'] = '/'.join(job_keyword)
            # 工作地点
            item['workarea_text'] = job.get('city')

            job_api = self.job_api.format(position_id)
            yield Request(url=job_api, headers=self.headers, callback=self.parse_job,
                          meta={'item': item.copy(), 'company_id': company_id})

    def parse_job(self, response):
        """
        提取职位需求，写入txt文件
        """
        item = response.meta['item']
        content = response.json().get('content', '')
        if content == '':
            return
        # 详细职位信息写入文件
        job_info = content.get('positionDetail', ' ')
        # with open('job_info.txt', 'a', encoding='utf-8') as file:
        #     file.write(job_info + '\n')
        item['job_info'] = job_info
        company_api = self.company_api + response.meta['company_id']
        # 爬取时间
        item['crawl_time'] = self.crawl_time()
        return item

        # yield Request(url=company_api, headers=self.headers, callback=self.parse_company, meta={'item': item.copy()})

    def parse_company(self, response):
        """
        提取公司待遇，返回最终item
        """
        item = response.meta['item']
        content = response.json().get('content', [])
        if len(content) == 0:
            return
        benefitVos = content.get('benefitVos', '')
        label_list = []
        if benefitVos == '':
            label_list = []
        for benefitVo in benefitVos:
            label_list.append(benefitVo.get('label'))
        # 公司待遇
        item['jobwelf'] = ' '.join(label_list)

        return item
