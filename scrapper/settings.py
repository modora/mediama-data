BOT_NAME = "mediama"

SPIDER_MODULES = ['scrapper.spiders']

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    'scrapper.pipelines.FilePipeline': 100
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 500
}
