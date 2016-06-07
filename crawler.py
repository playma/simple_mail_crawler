import sys
import urllib.request
from urllib.error import URLError, HTTPError
from socket import timeout
import re
import json
import threading

count = 0

def crawl(url, n):
    ##print(n)
    if(int(n)<1):
        return;
    global count
   
    try:
        url_validation = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if re.match(url_validation, url):
            data = str(urllib.request.urlopen(url, timeout=1).read())
            n = int(n)
            if(n>1):
                url_pat = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
                urls = re.findall(url_pat, data)
            
                for i in range(0, len(urls)):
                    if not re.match('mailto', urls[i]):
                        new = n-1
                        threading.Thread(target = crawl, args = (urls[i], new)).start() 

            mail_pat = re.compile(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+")
            mails = re.findall(mail_pat, data)
            
            if(len(mails)>0):
                for i in range(0, len(mails)):
                    count += 1
                    print(count, '\t', mails[i])	            
    except HTTPError as e:
    	#print('Error code: ', e.code)
    	pass
    	#print('http Error')
    	#print(url)
    except URLError as e:
    	pass
    	#print('URL Error')
    	#print(url)
        #print('Reason: ', e.reason)
    except timeout:
        pass
    return;

if __name__ == '__main__':
    hostname = sys.argv[1]
    n = sys.argv[2]
    print("Start to crawl ", hostname)

    threading.Thread(target = crawl, args = (hostname, n)).start() 

    


