#!/usr/bin/env python

import scanner
#import requests

##Testing
# target_uri = "http://192.168.56.102/mutillidae/"

target_uri = "http://192.168.56.102/dvwa/"
links_to_ignore = ["http://192.168.56.102/dvwa/logout.php"]
data_dict = {"username": "admin", "password": "password", "Login": "submit"}
# Every usege of requests, it logins and closes the session immediately logging out and removing all cookies. 
# That is an issue as the session is required to stay open.
#response = requests.post(target_uri, data=data_dict)


vuln_scanner = scanner.Scanner(target_uri, links_to_ignore)
vuln_scanner.session.post(target_uri + "login.php", data=data_dict)

# This will crawl the target URI and extract all links from it.
# It uses the target_uri supported when the Scanner class was initialized.
vuln_scanner.crawl()

# This will show whether the links contain forms or not.
print("Links to scan:")
vuln_scanner.run_scanner()

# This will extract all forms from the target URI.
forms = vuln_scanner.extract_forms("http://192.168.56.102/dvwa/vulnerabilities/xss_r/")
print(forms)

# # Just for testing purpose. This pice of code extract the text input from the form
# response = vuln_scanner.submit_form(forms[0], "test-01", "http://192.168.56.102/dvwa/vulnerabilities/xss_r/")

# print("\n")
# str_to_extract_start = "<pre>"
# str_to_extract_end = "</pre>"

# start_indx = response.content.decode("utf-8", "ignore").find(str_to_extract_start)
# end_indx = response.content.decode("utf-8", "ignore").find(str_to_extract_end)
# start_indx = start_indx + len(str_to_extract_start)

# print(response.content.decode("utf-8", "ignore")[start_indx:end_indx])
# print("\n")
# print(response.content.decode("utf-8", "ignore"))
# # end testing purpose

# Testing function test_xss_in_form
response = vuln_scanner.test_xss_in_form(forms[0], "http://192.168.56.102/dvwa/vulnerabilities/xss_r/")
print(response)
