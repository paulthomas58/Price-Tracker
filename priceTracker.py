import requests
from datetime import datetime
import csv
import numpy as np
from bs4 import BeautifulSoup

# change link to desired search item from ebay
LINK = "https://www.ebay.ca/sch/9355/i.html?_from=R40&_nkw=iphone+14+pro+max&LH_TitleDesc=0"

def get_prices_by_link(link):
    # get source
    r = requests.get(link)
    # parse source
    page_parse = BeautifulSoup(r.text, 'html.parser')
    # find all list items from search results
    search_results = page_parse.find(
        "ul", {"class": "srp-results"}).find_all("li", {"class": "s-item"})

    item_prices = []

    for result in search_results:
        price_as_text = result.find("span", {"class": "s-item__price"}).text
        if "to" in price_as_text:
            continue
        price = float(price_as_text[3:].replace(",", ""))
        item_prices.append(price)
    return item_prices


def remove_outliers(prices, m=2):
    data = np.array(prices)
    return data[abs(data - np.mean(data)) < m * np.std(data)]


def get_average(prices):
    return np.mean(prices)


def save_to_file(prices):
    fields = [datetime.today().strftime("%B-%D-%Y"),
              np.around(get_average(prices), 2)]
    with open('prices.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)


if __name__ == "__main__":
    prices = get_prices_by_link(LINK)
    print (get_average(prices))
    save_to_file(prices)
