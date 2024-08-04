#!/usr/bin/env python

import scanner

target_uri = "http://192.168.56.102/mutillidae/"
vuln_scanner = scanner.Scanner(target_uri)
vuln_scanner.crawl()