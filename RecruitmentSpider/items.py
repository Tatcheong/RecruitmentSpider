from scrapy import Item, Field


class BaseItem(Item):
    company_href = Field()  # 公司链接
    company_name = Field()  # 公司名
    companysize_text = Field()  # 公司规模
    industryField = Field()  # 公司业务
    experience = Field()  # 工作经验
    issuedate = Field()  # 更新时间
    job_href = Field()  # 工作链接
    job_name = Field()  # 工作名
    job_info = Field() # 职位要求
    job_keyword = Field()  # 关键字
    providesalary_text = Field()  # 工资
    workarea_text = Field()  # 工作地点
    crawl_time = Field()  # 爬取时间


class ChinahrItem(BaseItem):
    pass


class Job51Item(BaseItem):
    companytype_text = Field()  # 公司类型
    jobwelf = Field()  # 公司待遇


class lagouItem(BaseItem):
    pass
