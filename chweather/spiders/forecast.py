# coding=utf8
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from chweather.items import ForecastItem
from datetime import date, timedelta
import json
import re
import time

class NextsevenSpider(Spider):
    name = "nextseven"
    allowed_domains = ["www.weather.com.cn"]
    start_urls = ['file:////Users//summer//code//python//scrapy//chweather//test.json']

    url_template = r'http://www.weather.com.cn/weather/%s.shtml'

    def parse(self, response):
        datas = json.loads(response.body)
        for data in datas:
            yield Request(self.url_template % data['id'], callback=self.parse_item, 
                    meta = {'cityId': data['id']}
                  )

    def parse_item(self, response):
        sel = Selector(response)
        if len(sel.xpath('//*[@id="weather6h"]/h1/text()')):
            #has six hour forecast
            title = sel.xpath('//*[@id="weather6h"]/h1/text()').extract()[0].strip()
        else:
            title = sel.xpath('//*[@id="7d"]/h1/text()').extract()[0].strip()

        updateTime = re.search('(\d{4}-\d{2}-\d{2})(\s|&nbsp)(\d{2}:\d{2})', title, re.UNICODE)
        updateTime = updateTime.group(1)+' '+updateTime.group(3)
        tms = time.strptime(updateTime, '%Y-%m-%d %H:%M')

        #next six forecast
        if len(sel.xpath('//*[@id="weather6h"]/h1/text()')):
            for table in sel.xpath('//*[@id="weather6h"]/div/table'):
                sixitem = ForecastItem()
                sixitem['type'] = 1
                sixitem['cityId'] = response.meta['cityId']
                sixitem['updateTime'] = updateTime
                sixitem['duration'] = table.xpath('tr[1]/th/text()').extract()[0]
                sixitem['stat'] = table.xpath('tr[3]/td/a/text()').extract()[0]
                temphigh = table.xpath('tr[4]/td/a/text()').extract()[0].strip().splitlines()
                templow = table.xpath('tr[4]/td/span/a/text()').extract()[0].strip().splitlines()
                sixitem['temp'] = '%d~%d' % (templow[0], temphigh[0])
                wind = table.xpath('tr[5]/td/b/a/text()').extract()[0].strip().splitlines()
                sixitem['wd'] = wind[0].strip()
                sixitem['ws'] = wind[1].strip()
                yield sixitem


        #next seven forecast
        #get tables and iterate through them
        for table in sel.xpath('//*[@id="7d"]/div/table[position()>1]'):
            newitem = ForecastItem()
            day = table.xpath('tr[1]/td[1]/a/text()')[0].extract()
            day = int(re.match('\d{1,2}', day).group(0))
            #get date
            if day < tms.tm_mday:
                month = tms.tm_mon+1
                if month > 12:
                    month = 1
                    year = tms.tm_year+1
                else:
                    year = tms.tm_year
            else:
                month = tms.tm_mon
                year = tms.tm_year
            nd = '%d-%02d-%02d' % (year, month, day)
            nextday = date(year, month, day)+timedelta(1)
            nextday = nextday.strftime('%Y-%m-%d')

            newitem['type'] = 2
            newitem['cityId'] = response.meta['cityId']
            newitem['stat'] = table.xpath('tr[1]/td[4]/a/text()').extract()[0].strip()
            newitem['temp'] = table.xpath('tr[1]/td[5]/a/b/strong/text()').extract()[0].strip()
            newitem['wd'] = table.xpath('tr[1]/td[6]/a/text()').extract()[0].strip()
            newitem['ws'] = table.xpath('tr[1]/td[7]/a/text()').extract()[0].strip()
            newitem['updateTime'] = updateTime
            ti = table.xpath('tr[1]/td[2]/text()')[0].extract()
            if ti == u'白天':
                newitem['duration'] = nd + ' 08:00-' + nd + ' 20:00' 
            else:
                newitem['duration'] = nd + ' 20:00-' + nextday + ' 20:00' 

            yield newitem

            if len(table.xpath('tr[2]')):
                #set night forecast
                nitem = ForecastItem()
                nitem['type'] = 2
                nitem['cityId'] = response.meta['cityId']
                nitem['stat'] = table.xpath('tr[2]/td[3]/a/text()').extract()[0].strip()
                nitem['temp'] = table.xpath('tr[2]/td[4]/a/span/strong/text()').extract()[0].strip()
                nitem['wd'] = table.xpath('tr[2]/td[5]/a/text()').extract()[0].strip()
                nitem['ws'] = table.xpath('tr[2]/td[6]/a/text()').extract()[0].strip()
                nitem['updateTime'] = updateTime
                nitem['duration'] = nd + ' 20:00-' + nextday + ' 08:00'  
                yield nitem

