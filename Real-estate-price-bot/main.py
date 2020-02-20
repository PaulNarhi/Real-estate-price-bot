from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen as ureq
from bs4 import Comment
from _collections import defaultdict
import re
from writer import read, write
from datetime import date

def main():
    page_url = "https://www.vuokraovi.com/vuokra-asunnot?page=1&pageType="

    page_count = get_pages(page_url)

    price_map = get_prices(page_count)

    file_name = "data/prices " + str(date.today()) + ".json"

    write(price_map, file_name)
    



def get_pages(page_url):
    # variables and dict
    page_url = page_url# "https://www.vuokraovi.com/vuokra-asunnot?page=1&pageType="

    # open and close connection and save html to variable
    uClient = ureq(page_url)
    page_html = uClient.read()
    uClient.close()

    # html parsing
    page_soup = Soup(page_html, "html.parser")

    # get number of pages
    number_of_pages = int(page_soup.find("ul", {"class", "pagination"}).li
                          .find_next_sibling()
                          .find_next_sibling()
                          .find_next_sibling()
                          .find_next_sibling()
                          .find_next_sibling()
                          .find_next_sibling()
                          .find_next_sibling().text)
    return number_of_pages


def get_prices(number_of_pages):

    prices_of_postal_codes = defaultdict(list)  # initialize dictionary of type "postal code -> [prices]"

    for i in range(number_of_pages):

        page_url = "https://www.vuokraovi.com/vuokra-asunnot?page=" + str(i+1) + "&pageType="

        # open and close connection and save html to variable
        uClient = ureq(page_url)
        page_html = uClient.read()
        uClient.close()

        # html parsing
        page_soup = Soup(page_html, "html.parser")

        # grab individual real estate from page
        containers = page_soup.findAll("div", {"class": "list-item-container"})

        for contain in containers:
            # get post code
            comment = (contain.div.a.div.find_next_sibling().ul.find("li", {"class": "visible-xs"})
                       .find(text=lambda text: isinstance(text, Comment)))
            postal_code = str([int(i) for i in comment.split() if i.isdigit()][0]).rjust(5, "0")

            # get price
            price_text = contain.div.a.div.find_next_sibling().ul.find("li", {"class": "rent"}).span.text.strip()
            price = re.findall(r"\d ?\d+,?\d?\d", price_text.replace("\xa0", " "))
            if not price:
                continue
            price = float(price[0].replace(",", ".").replace(" ", ""))
            if price == 0:
                continue

            # get size
            layout = contain.div.a.div.find_next_sibling().ul.find("li", {"class": "semi-bold"}).text.strip()
            size = re.findall(r"[-+]?\d*,\d+|\d+", layout)
            if not size:
                continue
            size = float(size[0].replace(",", "."))
            if size < 10:
                continue

            price_per_m2 = price / size
            if price_per_m2 < 10:
                continue

            prices_of_postal_codes[postal_code].append(price_per_m2)
            # print("Size: " + size[0] + " m²" + " Price: " + price[0] + " €/kk" + " Price per m²: "
            #     + str(float(price[0].replace(",", ".")) / float(size[0].replace(",", "."))))

        print(i+1)

    return prices_of_postal_codes

main()
