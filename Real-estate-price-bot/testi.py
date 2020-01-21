from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

page_url = "https://www.vuokraovi.com/vuokra-asunnot/Turku"

# open and close connection and save html to variable
uClient = uReq(page_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# grab individual real estate
containers = page_soup.findAll("div", {"class": "list-item-container"})

# get price of real estate
print(containers[0].div.a.div.find_next_sibling().ul.find("li", {"class": "rent"}).span.text.strip())

