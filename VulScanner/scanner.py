#!/usr/bin/env python

import requests
import re
from urllib import parse
from bs4 import BeautifulSoup

# The class Scanner is used to crawl a web application, extract links, forms, 
# and test for vulnerabilities such as XSS.
class Scanner:
    def __init__(self, uri, links_to_ignore):
        self.session = requests.Session()
        self.target_uri = uri
        self.target_links = []
        self.links_to_ignore = links_to_ignore

    # This method extracts all links from a given URI.
    def extract_links_from(self, uri):
        response = self.session.get(uri)
        # Using regex to find all href links in the response content
        # For instance, it will return links similar to href="setup.php"
        # Note: This regex is basic and may not cover all edge cases in HTML parsing.
        # It is recommended to use BeautifulSoup for more robust HTML parsing.
        return re.findall('(?:href=")(.*?)"', response.content.decode('utf-8', 'ignore'))
    
    # This method starts the crawling process from the target URI.
    def crawl(self, uri=None):
        if uri == None:
            uri = self.target_uri
            
        href_links = self.extract_links_from(uri)

        # Filter out links that are not valid or should be ignored
        for link in href_links:
            # after parse.urljoin, link will be absolute link
            # For example, if link is "setup.php" and uri is "http://example.com/",
            # link will become "http://example.com/setup.php" 
            link = parse.urljoin(uri, link)

            if "#" in link:
                link = link.split("#")[0]

            if self.target_uri in link and link not in self.target_links and link not in self.links_to_ignore:
                # Add the link to the target links list which will be used for scanning
                self.target_links.append(link)
                print(link)
                # Recursively crawl the new link
                self.crawl(link)


    # This method extracts all forms from a given URI. 
    def extract_forms(self, uri):
        response = self.session.get(uri)
        parsed_html = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")
        return parsed_html.findAll("form")
    

    # This method submits a form with a given value and URI.
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
    

    # This method runs the scanner on the target links, extracting forms and testing for vulnerabilities.
    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                print(">} Testing form in " + link)

            if "=" in link:
                print(">} Testing " + link)

    # This method tests for XSS vulnerabilities in a form by submitting a script tag.
    # It returns True if the script is found in the response, indicating a vulnerability.
    def test_xss_in_form(self, form, url):
        xss_test_script = "<Script>alert('test')</Script>"
        response = self.submit_form(form, xss_test_script, url)
        if xss_test_script in response.content.decode("utf-8", "ignore"):
            return True
                