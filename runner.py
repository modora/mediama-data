import sys

from scrapy.cmdline import execute

def main(spiders: list):
	try:
		execute(['scrapy', 'crawl'] + spiders)
	except SystemExit:
		pass

if __name__ == "__main__":
	spiders = sys.argv[1:]
	main(spiders)
