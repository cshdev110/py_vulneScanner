#!/usr/bin/env python

import scanner
#import requests

##Testing
# target_uri = "http://192.168.56.102/mutillidae/"

target_uri = "http://192.168.56.102/dvwa/"
links_to_ignore = ["http://192.168.56.102/dvwa/logout.php"]
data_dict = {"username": "admin", "password": "password", "Login": "submit"}
# Every usege of requests, it logins and closes the session immediately logging out removing all cookies. 
# That is an issue as the session is required to stay open.
#response = requests.post(target_uri, data=data_dict)


vuln_scanner = scanner.Scanner(target_uri, links_to_ignore)
vuln_scanner.session.post(target_uri + "login.php", data=data_dict)
# vuln_scanner.crawl()
forms = vuln_scanner.extract_forms("http://192.168.56.102/dvwa/vulnerabilities/xss_r/")
print(forms)

response = vuln_scanner.submit_form(forms[0], "test", "http://192.168.56.102/dvwa/vulnerabilities/xss_r/")
print(response.content.decode("utf-8", "ignore"))