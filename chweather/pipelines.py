# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import memcache
from chweather import settings
import json

class ChweatherPipeline(object):

    def process_item(self, item, spider):
        print item
        return item

class MemCachedPipeline(object):

    def __init__(self):
        addr = settings.MEMCACHED_ADDRESS
        if addr is None:
            self.mc = None
        else:
            self.mc = memcache.Client([addr], debug=0)

    def process_item(self, item, spider):
        if not self.mc:
            return item

        cachedItem = self.mc.get(item['cityId'].encode('ascii'))
        if cachedItem:
            cachedItem = json.loads(cachedItem)
            cachedItem['temp'] = item['temp']
            cachedItem['wd'] = item['wd']
            cachedItem['ws'] = item['ws']
            cachedItem['updateTime'] = item['updateTime']
            self.mc.set(item['cityId'].encode('ascii'), json.dumps(cachedItem))
        else:
            newitem = {}
            newitem['city'] = item['city']
            newitem['cityId'] = item['cityId']
            newitem['temp'] = item['temp']
            newitem['wd'] = item['wd']
            newitem['ws'] = item['ws']
            newitem['updateTime'] = item['updateTime']
            newitem['next6'] = []
            newitem['next7'] = []
            self.mc.set(item['cityId'].encode('ascii'), json.dumps(newitem))

        return item
