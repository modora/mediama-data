import sys

from scrapy.cmdline import execute


def main(spiders: list):
    try:
        (
            execute(
                ["scrapy", "crawl"]
                + spiders
                + ["-a", "deltafetch_reset=1"]  # args
                + ["-s", "DELTAFETCH_DIR=/tmp/deltafetch"]
            )  # settings
        )
    except SystemExit:
        pass


if __name__ == "__main__":
    spiders = sys.argv[1:]
    main(spiders)
