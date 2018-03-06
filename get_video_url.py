# -*- coding: utf-8 -*-
from urllib import parse
import requests
import re
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/66.0.3350.0 Safari/537.36'
           }


def get_cookies_from_txt():
    with open('cookies.txt', 'r') as cookies_file:
        cookies_resource = cookies_file.read()
    return cookies_resource


def gen_cookies():
    cookies = {}
    cookies_resource = get_cookies_from_txt()
    for line in cookies_resource.split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    return cookies


def gethtml(url):
    session = requests.session()
    session.headers = headers
    requests.utils.add_dict_to_cookiejar(session.cookies, gen_cookies())
    response = session.get(url)
    web_html = response.text
    return web_html


def geturl_list(html_text):
    regex = r"(?<=a\shref=\"/watch).+?(?=\")"
    compile_regex = re.compile(regex)
    url_list = re.findall(compile_regex, html_text)
    prefix = "https://www.youtube.com/watch%s\n"

    with open('url_list.txt', 'a') as f:
        count = 0
        for url in url_list:
            result = (prefix % url)
            f.write(result)
            count = count+1
    return count


key_word = input('Pls input the keyword you want to research:').encode('utf-8')
key_word_url = parse.quote(key_word)
page = int(input('Pls input the counts of pages:'))

total = 0
for i in range(1, page):
    html = gethtml('https://www.youtube.com/results?search_query={0}&filters=short&page={1}'
                   .format(key_word_url, i)
                   )
    count1 = geturl_list(html)
    total = total+count1
print('Get {0} video url(s) in {1}!'.format(total, (os.path.join(os.getcwd(), 'url_list.txt'))))

'''
# for new web of Youtube https://www.youtube.com/new
total = 0
html = gethtml('https://www.youtube.com/results?search_query={0}&filters=short'.format(key_word_url)                  )
count1 = geturl_list(html)
total = total+count1
print('Get {0} video url(s) in {1}!'.format(total, (os.path.join(os.getcwd(), 'url_list.txt'))))
'''

exit(0)
