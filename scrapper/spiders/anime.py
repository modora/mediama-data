import scrapy
from urllib.parse import urljoin


class NyaaSpider(scrapy.Spider):
    name = "nyaa"
    allowed_domains = ["nyaa.si", "myanimelist.net"]

    MAL_LIMIT = 1000

    @staticmethod
    def generate_start_url():
        pass

    @staticmethod
    def format_url(
        query="",
        search_filter="no filter",
        category="all",
        sort_column="id",
        ascending=True,
        page=1,
    ):
        # Formats nyaa search urls

        # nyaa search urls are formatted as
        # /?q={query}&f={filter}&c={category}&s={sort_column}&o={order}&p={page}

        search_filter = {"no filter": 0, "no remakes": 1, "trusted only": 2}[
            search_filter
        ]
        category = {
            "all": "0_0",
            "anime": "1_0",
            "anime music video": "1_1",
            "anime english-translated": "1_2",
            "anime non-english-translated": "1_3",
            "anime raw": "1_4",
            "audio": "2_0",
            "lossless": "2_1",
            "lossy": "2_2",
            "literature": "3_0",
            "literature english-translated": "3_1",
            "literature non-english-translated": "3_2",
            "literature raw": "3_3",
            "live action": "4_0",
            "live action english-translated": "4_1",
            "idol/promotional video": "4_2",
            "live action non-english-translated": "4_3",
            "live action raw": "4_4",
            "pictures": "5_0",
            "graphics": "5_1",
            "photos": "5_2",
            "software": "6_0",
            "apps": "6_1",
            "games": "6_2",
        }[category]

        # The date column on nyaa actually maps to the id column
        sort_column = "id" if sort_column == "date" else sort_column

        order = "asc" if ascending else "desc"

        url = f"/?q={query}&f={search_filter}&c={category}&s={sort_column}&o={order}&p={page}"

        return urljoin("https://nyaa.si/", url)

    def start_requests(self):
        # Define starting url and parsing methods here

        # Nyaa has a search result limit of 100 pages Thus we cannot scrape the
        # entire database We can instead consider the most popular files. Simply
        # sorting the nyaa database for most completed downloads results in
        # mostly recent shows with many single episode releases. For a more
        # diverse dataset, we will instead get the top 1000 shows on MAL pass
        # those series as queries in nyaa, then scrape and parse each torrent
        self.mal_results = 0
        yield scrapy.Request(
            f"https://myanimelist.net/topanime.php?type=bypopularity&limit={self.mal_results}",
            self.parse_mal_popular,
        )

    def parse_mal_popular(self, response):
        # Parse the MAL most popular page

        # Parse page for series titles and use as the search query on nyaa
        for series in response.xpath(
            '//div[@class="detail"]/div[2]/a[1]/text()'
        ).getall():
            yield scrapy.Request(
                self.format_url(query=series, category="anime english-translated"),
                self.parse_search,
                cb_kwargs={"series": series}
            )

        self.mal_results += 50

        # Go to next page on MAL if limit not yet reached
        # MAL shows 50 results per page so offset accordingly
        if self.mal_results < self.MAL_LIMIT:
            next_page_url = response.xpath(
                '//div[contains(@class,"pagination")]/a[1]/@href'
            ).get()
            yield scrapy.Request(
                response.urljoin(next_page_url), self.parse_mal_popular
            )

    def parse_search(self, response, series=None):
        # This function parses the search results

        # Go the the torrent page for some title
        for href in response.xpath(
            "//tr/td[2]/a[1]/@href"
        ).getall():
            yield scrapy.Request(response.urljoin(href), self.parse_torrent, cb_kwargs={'series': series})

        next_page_url = response.xpath(
            '//li[@class="next"]/a/@href'
        ).get()
        yield scrapy.Request(response.urljoin(next_page_url), self.parse_search, cb_kwargs={'series': series})

    def parse_torrent(self, response, series=None):
        # This function parses torrent pages

        # nyaa shows the filelist so no need to download and parse torrent, we
        # can simply parse page for all filenames in the torrent

        filenames = [
            filename
            for filename in response.xpath(
                '//div[contains(@class,"torrent-file-list")]//li/text()'
            ).getall()
        ]

        yield {"filenames": filenames, "series": series}
