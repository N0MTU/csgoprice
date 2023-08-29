#Libraries used for price tracker.
import requests
from bs4 import BeautifulSoup #web crawler
import matplotlib.pyplot as plt #graph plotter
import time
import datetime
from collections import defaultdict
from scipy.interpolate import interp1d #value interpolator

#Specify names of items to find
include_names = ["Chroma Case", "Glove Case", "Operation Breakout Weapon Case", "Gamma 2 Case", "Spectrum Case", "Chroma 3 Case", "Chroma 2 Case", "Gamma Case", "Operation Wildfire Case", "Revolver Case", "Clutch Case", "Falchion Case", "Shadow Case"]

prices = defaultdict(list)

#for loop to scan web page (url) for items (include_names)
for page_num in range(1, 5):
    url = f"https://steamcommunity.com/market/search?q=case&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&category_730_Type%5B%5D=tag_Type_Hands&appid=730#p{page_num}_default_desc"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Currency": "GBP"
        }
    time.sleep(2)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all("div", {"class": "market_listing_row market_recent_listing_row market_listing_searchresult"})
    #finding all items listed in the HTML class containing them
    for item in items:
        name_element = item.find("span", {"class": "market_listing_item_name"})
        price_element = item.find("span", {"class": "market_table_value normal_price"})
        if name_element is not None and price_element is not None:
            name = name_element.text.strip()
            price = price_element.find("span", {"class": "normal_price"}).get("data-price")
            if name in include_names and price is not None:
                prices[name].append(float(price)/100)
                # Update price-date file
                with open("item_prices.txt", "a") as f:
                    f.write(f"{name},{datetime.date.today().strftime('%Y-%m-%d')},{prices[name][-1]:.2f}\n")

# Line graph of price changes over time
with open("item_prices.txt", "r") as f:
    lines = f.readlines()

#standardise item lists for display
price_lists = defaultdict(list)
for line in lines:
    name, date, price = line.strip().split(",")
    price_lists[name].append((date, float(price)))

#interpolate values between known prices
plt.figure()
for name, prices in price_lists.items():
    dates, values = zip(*prices)
    f = interp1d(range(len(dates)), values, kind='linear', fill_value='extrapolate')
    plt.plot(dates, f(range(len(dates))), label=name)

#plot graph
plt.title("Price Changes Over Time")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
