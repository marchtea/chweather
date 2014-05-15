# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChweatherItem(Item):
    # define the fields for your item here like:
    # name = Field()
    city = Field()
    cityId = Field()
    temp = Field()
    wd = Field()
    ws = Field()
    updateTime = Field()
