import json

import requests
from requests.packages import urllib3

urllib3.disable_warnings()
url = 'https://gate.lagou.com/v1/entry/positionsearch/searchPosition'
job_api = 'https://gate.lagou.com/v1/entry/position/jd?positionId=7963208&isCInspectB=1'
company_api = 'https://gate.lagou.com/v1/entry/bigCompany/query?companyId=33956'

headers = {
    'x-l-req-header': '{"userToken":"475a50abbbbed97ec3d6dd7b62205e8081397a751cdce7cf5946b2ebe5c265e2","reqVersion":71000,"lgId":"990000000057390_1610420455506","appVersion":"7.10.1","userType":0,"deviceType":200}',
    'x-l-janus-strategy': '{"strategies":[{"key":"position_card","value":"A"},{"key":"APP_RESUME_FLOW_21","value":"B"}]',
    'content-type': 'application/json;charset=utf-8',
    'accept-encoding': 'gzip',
    'user-agent': 'okhttp/3.11.0'
}

data = {"aggregateLevel": 0, "businessZone": "", "city": "全国", "district": "", "hiTag": "", "isAd": "0",
        "isSchoolJob": 'false', "keyword": "大数据", "keywordSource": 0, "lastShowCompanyId": 0, "latitude": "",
        "latitudeHigh": "", "latitudeLow": "", "longitude": "", "longitudeAndLatitude": "", "longitudeHigh": "",
        "longitudeLow": "", "mapLeveL": 0, "nearByKilometers": "", "pageNo": 1, "pageSize": 15,
        "refreshHiTagList": 'true', "salaryLower": 0, "salaryUpper": 0, "searchType": "",
        "shieldDeliveyCompany": 'false',
        "showId": "", "sort": 0, "subwayLineName": "", "subwayStation": "", "tagType": 0}

for page in range(1, 5):
    data['pageNo'] = page
    # response = requests.post(url=url, headers=headers, data=json.dumps(data), verify=False)
    response = requests.get(url=company_api, headers=headers, verify=False)
    print(response.status_code)
    print(response.text)
