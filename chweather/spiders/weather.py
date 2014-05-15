from scrapy.spider import Spider
from chweather.items import ChweatherItem
from scrapy.http import Request
import json

class WeatherSpider(Spider):
    name = 'weather'
    allowed_domains = ['weather.com.cn']
    start_urls = ['file:////Users//summer//code//python//scrapy//chweather//test.json']

    url_template = r'http://www.weather.com.cn/data/ks/%s.html'
    referer_template = r'http://www.weather.com.cn/weather/%s.shtml'


    def parse(self, response):
        datas = json.loads(response.body)
        for data in datas:
            yield Request(self.url_template % data['id'], callback=self.parse_item, 
                    headers = {'user-agent': r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1964.4 Safari/537.36',
                               'referer': self.referer_template % data['id']
                        })

    def parse_item(self, response):
        data = json.loads(response.body)
        i = ChweatherItem()
        i['city'] = data['weatherinfo']['city']
        i['cityId'] = data['weatherinfo']['cityid']
        i['temp'] = data['weatherinfo']['temp']
        i['wd'] = data['weatherinfo']['WD']
        i['ws'] = data['weatherinfo']['WSE']
        i['updateTime'] = data['weatherinfo']['time']
        return i

