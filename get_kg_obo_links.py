import requests
from bs4 import BeautifulSoup

def obo_link_gen():
    kg_obo_url = "https://kghub.org/kg_obo/"
    kg_obo_page = requests.get(kg_obo_url)
    soup = BeautifulSoup(kg_obo_page.text, 'html.parser')

    table = soup.find("table")
    trs = table.findAll("tr")
    for tr in trs[1::]:
        link_pt1 = tr.findAll("td")[2].find("a").text
        link_pt2 = tr.findAll("td")[3].text
        link = link_pt1 + link_pt2
        yield link

if(__name__=="__main__"):
    for obo_link in obo_link_gen():
        print(obo_link)
