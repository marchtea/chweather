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
#USER_AGENT = 'chweather (+http://www.yourdomain.com)'


#Settings For ChWeather
MEMCACHED_ADDRESS = '127.0.0.1:11211'
