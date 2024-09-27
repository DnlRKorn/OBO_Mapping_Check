import requests
from bs4 import BeautifulSoup

kg_obo_url = "https://kghub.org/kg_obo/"
kg_obo_page = requests.get(kg_obo_url)
soup = BeautifulSoup(kg_obo_page.text, 'html.parser')

for tr in soup.findAll("tr")[1::]:
    link = tr.findAll('td')[3].findAll('a')[1].get('href')
    print(link)

