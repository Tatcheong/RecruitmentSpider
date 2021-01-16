import requests
import gzip
from requests.packages import urllib3

urllib3.disable_warnings()
headers = {
    'traceid': 'b82ea1f7-c1f2-43a6-8685-159f55a22d71',
    'zp-accept-encrypting': '1',
    'zp-accept-encoding': '1',
    'zp-accept-compressing': '3',
    'user-agent': 'NetType/wifi Screen/810X1440 BossZhipin/8.180 Android 23',
    't2': 'CDG8ENFZjA0AANAM1DDhQRQMyW2tTYAYfWjIKdgY0AgENaFZn',
    'accept-encoding': 'gzip'
}

url = 'https://api5.zhipin.com/api/zpgeek/app/geek/search/cardlist?filterParams=%7B%22districtCode%22%3A%22-1%22%2C%22cityCode%22%3A%22101190400%22%2C%22businessId%22%3A%22-1%22%7D&source=1&searchType=3&page=2&prefix=q&query=%E5%A4%A7%E6%95%B0%E6%8D%AE&expectId=165963308&curidentity=0&v=8.180&app_id=1003&req_time=1609987984784&uniqid=337D04381C7E02BB251D79D2CA66B01F&client_info=%7B%22version%22%3A%226.0.1%22%2C%22os%22%3A%22Android%22%2C%22start_time%22%3A%221609987915517%22%2C%22resume_time%22%3A%221609987915517%22%2C%22channel%22%3A%220%22%2C%22model%22%3A%22Android%7C%7CMuMu%22%2C%22ssid%22%3A%22%5C%22oS06W8Pu3%5C%22%22%2C%22bssid%22%3A%226f%3A53%3A30%3A36%3A57%3A38%22%2C%22imei%22%3A%22330000000147455%22%2C%22longitude%22%3A0%2C%22dzt%22%3A0%2C%22latitude%22%3A0%2C%22uniqid%22%3A%22337D04381C7E02BB251D79D2CA66B01F%22%2C%22oaid%22%3A%22NA%22%2C%22umid%22%3A%228550de1a7a44c3699493eaabef359ca%22%2C%22network%22%3A%22wifi%22%2C%22operator%22%3A%22UNKNOWN%22%7D&sig=V2.0e09be6c45533a1e137117f56a99f54d6'

response = requests.get(url=url, headers=headers, verify=False)
html = response.content.decode(response.apparent_encoding)
print(html)
