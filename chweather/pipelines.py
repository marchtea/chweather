# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import memcache
from chweather import settings
import json
from scrapy.exceptions import DropItem

class ChweatherPipeline(object):

    def process_item(self, item, spider):
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

        try:
            if not len(self.mc.get_stats()):
                return item
        except Exception as e:
            print e
            return item

        cachedItem = self.mc.get(item['cityId'].encode('ascii'))
        if spider.name == 'realtime':
            self.__save_realtime(item, cachedItem)
        elif spider.name == 'nextseven':
            self.__save_forecast(item, cachedItem)
        else:
            raise DropItem("Unknown spider's item %s" % item)

        return item

    def __save_forecast(self, item, cachedItem):
        if cachedItem:
            cachedItem = json.loads(cachedItem)

            if item['type'] == 1:
                nextsix = cachedItem['next6']
                nitem = dict(item)
                if len(nextsix) == 0:
                    nextsix.append(nitem['updateTime'])
                    nextsix.append(nitem)
                else:
                    if nextsix[0] == item['updateTime']:
                        if (len([i for i in nextsix[1:] if i['duration'] == item['duration']])):
                            return
                        else:
                            nextsix.append(nitem)
                    else:
                        nextsix = [item['updateTime'], nitem]
                cachedItem['next6'] = nextsix
            elif item['type'] == 2:
                nextseven = cachedItem['next7']
                item = dict(item)
                if len(nextseven) == 0:
                    nextseven.append(item['updateTime'])
                    nextseven.append(item)
                else:
                    if nextseven[0] == item['updateTime']:
                        if (len([i for i in nextseven[1:] if i['duration'] == item['duration']])):
                            return
                        else:
                            nextseven.append(item)
                    else:
                        nextseven = [item['updateTime'], item]
                cachedItem['next7'] = nextseven
            self.mc.set(cachedItem['cityId'].encode('ascii'), json.dumps(cachedItem))
        else:
            newitem = {}
            newitem['cityId'] = item['cityId']
            if item['type'] == 1:
                newitem['next6'] = [item['udpateTime'], dict(item)]
            else:
                newitem['next7'] = [item['udpateTime'], dict(item)]
            self.mc.set(item['cityId'].encode('ascii'), json.dumps(newitem))

    def __save_realtime(self, item, cachedItem):
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

