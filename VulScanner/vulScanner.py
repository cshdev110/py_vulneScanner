#!/usr/bin/env python


import requests
from urllib import parse
from bs4 import BeautifulSoup

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "http://192.168.56.102/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)
# print(response.content.decode())

parsed_html = BeautifulSoup(response.content.decode())
forms_list = parsed_html.findAll("form")
# print(forms_list)

for form in forms_list:

    print(parse.urljoin(target_url, form.get("action")))
    print(form.get("method"))
    
    inputs_list = form.findAll('input')
    for input in inputs_list:
        print(input.get("name"))