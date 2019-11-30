from pathlib import Path

import scrapy
from scrapy.exporters import CsvItemExporter
from functional import seq

from .helpers import *

class CSVPipeline:
    fields = ["series", "source", "filename"]  # item fields to export

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, scrapy.signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, scrapy.signals.spider_closed)
        return pipeline
    
    def spider_opened(self, spider):
        filepath = spider.settings.get('DATA_DIR').joinpath(f'{spider.name}.csv')
        self.file = open(filepath, 'a+b')
        self.exporter = CsvItemExporter(self.file, fields_to_export=self.fields)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        filenames = item.get('filenames', [])
        data = item.copy()
        if 'filenames' in data:
            del data['filenames']
        for filename in filenames:
            data['filename'] = filename
            self.exporter.export_item(data)
        return item


class FilePipeline:
    @staticmethod
    def clean_filelist(filelist):
        VALID_VIDEO_EXT = ('.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv')

        return (
            seq(filelist)
            .map(strip_string)
            .filter_not(is_empty_string)
            .filter(is_video_file_from_ext)
            .filter(lambda filename: filename.endswith(VALID_VIDEO_EXT))
        )

    def process_item(self, item, spider):
        if item.get("filenames"):
            # Clean the filenames and remove any results with no name
            filenames = self.clean_filelist(item.get("filenames"))

            # export only if there are valid filenames after cleaning
            if filenames:
                item['filenames'] = filenames
            else:
                raise scrapy.exceptions.DropItem("No valid files found")
        else:
            raise scrapy.exceptions.DropItem(
                f"{spider.name}: Missing filenames in {item}"
            )
        return item
