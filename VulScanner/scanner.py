#!/usr/bin/env python

import requests
import re
from urllib import parse


class Scanner:
    def __init__(self, uri):
        self.target_uri = uri
        self.target_links = []

    def extract_links_from(self, uri):
        response = requests.get(uri)
        return re.findall('(?:href=")(.*?)"', response.content.decode('utf-8', 'ignore'))
    
    def crawl(self, uri=None):
        if uri == None:
            uri = self.target_uri
            
        href_links = self.extract_links_from(uri)

        for link in href_links:
            link = parse.urljoin(uri, link)

            if "#" in link:
                link = link.split("#")[0]

            if self.target_uri in link and link not in self.target_links:
                self.target_links.append(link)
                print(link)
                self.crawl(link)