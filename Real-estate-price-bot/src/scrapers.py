from bs4 import Comment
import re


def s_id(container):
	comment = container.div.find(text=lambda text: isinstance(text, Comment))
	id = re.findall(r"\d\d\d\d\d\d", comment)
	return id[0]



def s_postal_code(container):
    comment = (container.div.a.div.find_next_sibling().ul.find("li", {"class": "visible-xs"})
               .find(text=lambda text: isinstance(text, Comment)))
    postal_code = str([int(i) for i in comment.split() if i.isdigit()][0]).rjust(5, "0")

    return postal_code

def s_price(container):
    price_text = container.div.a.div.find_next_sibling().ul.find("li", {"class": "rent"}).span.text.strip()
    price = re.findall(r"\d ?\d+,?\d?\d", price_text.replace("\xa0", " "))
    
    return price

def s_size(container):
    layout = container.div.a.div.find_next_sibling().ul.find("li", {"class": "semi-bold"}).text.strip()
    size = re.findall(r"[-+]?\d*,\d+|\d+", layout)

    return size


# TODO: get regex working so that only room numbers get added
def s_rooms(container):
    rooms = container.div.a.div.find_next_sibling().ul.find("li", {"class": "semi-bold"}).find_next_sibling().text
    if not rooms:
        return -1
    return rooms[0]
