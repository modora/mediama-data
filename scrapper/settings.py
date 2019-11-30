from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

BOT_NAME = "mediama"

SPIDER_MODULES = ['scrapper.spiders']

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    'scrapper.pipelines.FilePipeline': 100,
    'scrapper.pipelines.CSVPipeline': 1000
}

SPIDER_MIDDLEWARES = {
    'scrapy_deltafetch.DeltaFetch': 100,
}

DELTAFETCH_ENABLED = True
DELTAFETCH_DIR = ROOT_DIR / 'deltafetch'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 500
}
