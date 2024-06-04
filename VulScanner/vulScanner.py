#!/usr/bin/env python


import requests
from bs4 import BeautifulSoup

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


#at two minutes from the tutorial