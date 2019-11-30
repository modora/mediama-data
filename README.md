# Overview
This repository contains scripts to gather sample data used for mediama. For
development purposes, the data found in `data/` should be sufficient. If you
want the most up-to-date information, run `scrapy crawl <list of spiders>` where
the list is separated by spaces. By default, scrapes are incremented from the
previous crawl. For a full crawl, pass in the argument `-a deltafetch_reset=1`

# Data
All data files are formatted as csv files with the format show below. The source
column represents the name of the torrent file.

```
series,source,filename
Steins;Gate,[WhyNot] Steins;Gate [BD 720p AAC],[WhyNot] Steins;Gate - 01 [BD 720p AAC][5CFFC1C7].mkv
Steins;Gate,[WhyNot] Steins;Gate [BD 720p AAC],[WhyNot] Steins;Gate - 02 [BD 720p AAC][C32D5ABE].mkv
Steins;Gate,[WhyNot] Steins;Gate [BD 720p AAC],[WhyNot] Steins;Gate - 03 [BD 720p AAC][6F55BDF5].mkv
...
Steins;Gate,[WhyNot] Steins;Gate [BD 720p AAC],[WhyNot] Steins;Gate - 25 [BD 720p AAC][5AAF0DA8].mkv
```

# Sources
Currently, all data is collected by scrapping torrent trackers and parsing
torrent files. Torrents are encoded using bencode. Here are some examples of
decoded torrent files with the SHA-1 hashes for pieces truncated:

```json
{
   "announce": "http://torrent.ubuntu.com:6969/announce",
   "comment": "Kubuntu CD cdimage.ubuntu.com",
   "creation date": 1555522851,
   "info": {
      "length": 1916190720,
      "name": "kubuntu-19.04-desktop-amd64.iso",
      "piece length": 524288,
      "pieces": "<hex>B4 08 CF 8C AC 9A ...</hex>"
   }
}
```

```json
{
   "announce": "http://nyaa.tracker.wf:7777/announce",
   "announce-list": [
      [
         "http://nyaa.tracker.wf:7777/announce"
      ],
      [
         "http://anidex.moe:6969/announce"
      ],
      [
         "http://tracker.minglong.org:8080/announce"
      ],
      [
         "udp://open.stealth.si:80/announce"
      ],
      [
         "udp://tracker.opentrackr.org:1337/announce"
      ],
      [
         "udp://tracker.coppersurfer.tk:6969/announce"
      ],
      [
         "udp://exodus.desync.com:6969/announce"
      ]
   ],
   "comment": "https://nyaa.si/view/968031",
   "created by": "NyaaV2",
   "creation date": 1507732463,
   "encoding": "UTF-8",
   "info": {
      "files": [
         {
            "length": 881416933,
            "path": [
               "[Doki] Pokemon The Origin - 01 (1920x1080 Hi10P BD FLAC) [6D4B7E82].mkv"
            ]
         },
         {
            "length": 506118666,
            "path": [
               "[Doki] Pokemon The Origin - 02 (1920x1080 Hi10P BD FLAC) [0E24B465].mkv"
            ]
         },
         {
            "length": 670495165,
            "path": [
               "[Doki] Pokemon The Origin - 03 (1920x1080 Hi10P BD FLAC) [0C538A1F].mkv"
            ]
         },
         {
            "length": 753866630,
            "path": [
               "[Doki] Pokemon The Origin - 04 (1920x1080 Hi10P BD FLAC) [981AF68C].mkv"
            ]
         }
      ],
      "name": "Pokemon The Origin (2013) [Doki](1920x1080 Hi10P BD FLAC)",
      "piece length": 2097152,
      "pieces": "<hex>B8 5C 1E 00 69 C7 ...</hex>"
   }
}

```

This table lists all the sources for the following media

| Media | Source |
| --- | --- |
| Anime | <ul><li>nyaa.si</li></ul> |

## Nyaa
Nyaa does not have an official API so data is scraped from the web API. The
query passed into the search API are the top 1000 series listed on MAL and all
search results are parsed for their filelists.
