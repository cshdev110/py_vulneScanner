#!/usr/bin/env python


import requests
from urllib import parse
from bs4 import BeautifulSoup
## BeautifulSoup is to extract any element from any html page.

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "http://192.168.56.102/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url) # Retrieve the page code.
# print(response.content.decode())

# With BeautifulSoup is easy to go over a page's elements just by looking up the elements names.
parsed_html = BeautifulSoup(response.content.decode(), features="html.parser")
forms_list = parsed_html.findAll("form") ## Get a set of all elements in form's element.

# Iterating the form's elements to seek for the require elements.
for form in forms_list:

    post_uri = parse.urljoin(target_url, form.get("action"))
    print(post_uri)
    print(form.get("method"))
    
    inputs_list = form.findAll('input')
    post_data = {}
    for input in inputs_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        if input_type == "text":
            input_value = "test"

        post_data[input_name] = input_value
    result = requests.post(post_uri, data = post_data)
    print(result.content.decode())
