from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen as ureq
from bs4 import Comment
from _collections import defaultdict
import re
from writer import read_csv, write_csv
from scrapers import s_price, s_size, s_postal_code, s_id, s_rooms
from datetime import date

def main():
    page_url = "https://www.vuokraovi.com/vuokra-asunnot?page=1&pageType="

    page_count = get_pages(page_url)

    data = get_data(page_count)

    file_name = "../data/data " + str(date.today()) + ".csv"

    write_csv(data[1:], file_name)

    print("\nFound " + str(len(data)-1) + " apartments with sufficient data")
    print("Save data to " + file_name + " at ../data folder\n")
    



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


def get_data(number_of_pages):

    data_matrix = [[]]  # Initialize dataframe of type [Id, price, size, price/size, postcode, rooms]

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

        for container in containers:
            # get post code
            postal_code = s_postal_code(container)

            # get price
            price = s_price(container)
            if not price:
                continue
            price = float(price[0].replace(",", ".").replace(" ", ""))
            if price == 0:
                continue

            # get size
            size = s_size(container)
            if not size:
                continue
            size = float(size[0].replace(",", "."))
            if size < 10:
                continue

            price_per_m2 = round(price / size, 2)
            if price_per_m2 < 10:
                continue


            data_matrix.append([s_id(container), price, size, price_per_m2, postal_code, s_rooms(container)])

        print("Scanning page: " + str(i+1))

    return data_matrix

main()
