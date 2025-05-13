#!/usr/bin/env python

import requests
import re
from urllib import parse
from bs4 import BeautifulSoup


class Scanner:
    def __init__(self, uri, links_to_ignore):
        self.session = requests.Session()
        self.target_uri = uri
        self.target_links = []
        self.links_to_ignore = links_to_ignore

    def extract_links_from(self, uri):
        response = self.session.get(uri)
        return re.findall('(?:href=")(.*?)"', response.content.decode('utf-8', 'ignore'))
    
    def crawl(self, uri=None):
        if uri == None:
            uri = self.target_uri
            
        href_links = self.extract_links_from(uri)

        for link in href_links:
            link = parse.urljoin(uri, link)

            if "#" in link:
                link = link.split("#")[0]

            if self.target_uri in link and link not in self.target_links and link not in self.links_to_ignore:
                self.target_links.append(link)
                print(link)
                self.crawl(link)


    def extract_forms(self, uri):
        response = self.session.get(uri)
        parsed_html = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")
        return parsed_html.findAll("form")
    

    def submit_form(self, form, value, uri):
        action = form.get("action")
        post_uri = parse.urljoin(uri, action)
        method = form.get("method")

        inputs_list = form.findAll("input")
        post_data = {}
        for input in inputs_list:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value

            post_data[input_name] = input_value
        
        if method == "post":
            return self.session.post(post_uri, data=post_data)
        
        return self.session.get(post_uri, params=post_data)
    

    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                print(">} Testing form in " + link)

            if "=" in link:
                print(">} Testing " + link)

    
    def test_xss_in_form(self, form, url):
        xss_test_script = "<Script>alert('test')</Script>"
        response = self.submit_form(form, xss_test_script, url)
        if xss_test_script in response.content.decode("utf-8", "ignore"):
            return True
                