from pathlib import Path

import scrapy
from functional import seq

from .helpers import *

DATA_DIR = Path(__file__).parent.joinpath("../data").resolve()


class FilePipeline:
    @staticmethod
    def clean_filelist(filelist):
        VALID_VIDEO_EXT = ('.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv')

        return list(
            seq(filelist)
            .map(strip_string)
            .filter_not(is_empty_string)
            .filter(is_video_file_from_ext)
            .filter(lambda filename: filename.endswith(VALID_VIDEO_EXT))
        )

    def open_spider(self, spider):
        self.export_file = DATA_DIR.joinpath(f"{spider.name}.csv")

        with open(self.export_file, "w") as f:
            f.write("series,filename\n")

    def close_spider(self, spider):
        with open(self.export_file, 'r') as f:
            sorted_names = sorted(f.readlines()[1:])
        with open(self.export_file, 'w') as f:
            f.write("series,filename\n")
            f.write(sorted_names)

    def process_item(self, item, spider):
        # Write all results to the data/{spider_name}.csv

        if item.get("filenames"):
            # Clean the filenames and remove any results with no name
            filenames = self.clean_filelist(item.get("filenames"))

            # only write to export_file if there are valid filenames after 
            # cleaning
            if len(filenames) > 0:
                with open(self.export_file, "a") as f:
                    for filename in filenames:
                        series = item.get('series', '')
                        if series is None:
                            series = ''
                        line = f'{series},{filename}\n'
                        f.write(line)
        else:
            raise scrapy.exceptions.DropItem(
                f"{spider.name}: Missing filenames in {item}"
            )
