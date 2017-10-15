from bs4 import BeautifulSoup
import requests

url = 'https://news.bitcoin.com/'

r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)
for link in soup.findAll("div", {"class": "td-big-grid-meta"}):
    print(link.find_all('a')[0].text)
