# Scrapy settings for chweather project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'chweather'

SPIDER_MODULES = ['chweather.spiders']
NEWSPIDER_MODULE = 'chweather.spiders'


ITEM_PIPELINES = {
    'chweather.pipelines.ChweatherPipeline': 400,
    'chweather.pipelines.MemCachedPipeline': 500,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1964.4 Safari/537.36'

#Settings For ChWeather
MEMCACHED_ADDRESS = '127.0.0.1:11211'

SPIDER_MIDDLEWARES = {
'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': None
}
