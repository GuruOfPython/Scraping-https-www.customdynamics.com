# https://www.customdynamics.com/vehicle/harley-davidson-led-lighting
# https://www.customdynamics.com/vehicle/indian

import scrapy
from scrapy.http import FormRequest
import os, math, xlrd, openpyxl, csv, random, re, time, json, itertools
from lxml import html
import requests
from urllib.parse import urlparse, urljoin, unquote
from string import ascii_lowercase, digits, punctuation


class MainScraper(scrapy.Spider):
    name = 'two_websites_scraper'

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 20,
        # 'DOWNLOAD_DELAY': 1,
        'dont_filter': True,
        'RETRY_ENABLED': False,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5,
        'CONCURRENT_REQUESTS_PER_IP': 5,
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_IGNORE_HTTP_CODES': [301, 302, 403, 404, 429, 500, 503],
        'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage',
        'HTTPCACHE_POLICY': 'scrapy.extensions.httpcache.DummyPolicy',
    }

    def __init__(self):
        self.input_directory = os.getcwd() + '/Input/'
        self.save_directory = os.getcwd() + '/Result/'
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

        result_file_name = self.save_directory + "total_results.csv"
        self.create_result_file(result_file_name=result_file_name)

        self.domain_url = "https://www.customdynamics.com"
        self.start_urls = {
            "Harley": {
                "first post url": "https://www.customdynamics.com/amfinder/index/options/",
                "first post header": {
                    "dropdown_id": "4",
                    "parent_id": "9808",
                    "use_saved_values": "0",
                    "parent_dropdown_id": "3"
                },
                "prefix": "harley-davidson",
                "suffix": "cat=8"
            },
            "Indian": {
                "first post url": "https://www.customdynamics.com/amfinder/index/options/",
                "first post header": {
                    "dropdown_id": "4",
                    "parent_id": "10661",
                    "use_saved_values": "0",
                    "parent_dropdown_id": "3"
                },
                "prefix": "indian",
                "suffix": "cat=503"
            },
        }
        self.total_result = []
        self.total_urls = []
        self.total_cnt = 0

    def start_requests(self):
        for type, body in self.start_urls.items():
            pass

    def create_result_file(self, result_file_name):
        heading = [
            "Name", "Description", "Images", "Price"
        ]
        import codecs
        self.result_file = codecs.open(result_file_name, "w", "utf-8")
        self.result_file.write(u'\ufeff')
        self.insert_row(result_row=heading)

    def insert_row(self, result_row):
        result_row = [str(elm) if elm else "" for elm in result_row]
        result_row = [elm.replace('"', '""') for elm in result_row]
        self.result_file.write('"' + '","'.join(result_row) + '"' + "\n")
        self.result_file.flush()

if __name__ == '__main__':
    from scrapy.utils.project import get_project_settings
    from scrapy.crawler import CrawlerProcess, CrawlerRunner

    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(MainScraper)
    process.start()
