import urllib3
from bs4 import BeautifulSoup

url = 'http://www.53cal.jp/area/?a_code=1220131'

http = urllib3.PoolManager()
r = http.request('GET', url)

soup = BeautifulSoup(r.data, 'html.parser')
title_tag = soup.title
title = title_tag.string
print(title_tag)
print(title)