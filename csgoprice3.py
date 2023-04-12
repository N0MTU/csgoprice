import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time

# Set the list of item names to include
include_names = ["Chroma Case", "Glove Case", "Operation Breakout Weapon Case", "Gamma 2 Case", "Spectrum Case", "Chroma 3 Case", "Chroma 2 Case", "Gamma Case", "Operation Wildfire Case", "Revolver Case", "Clutch Case", "Falchion Case", "Shadow Case"]

# Initialize empty lists for prices and names
prices = []
names = []

# Loop over all pages of search results
for page_num in range(1, 5):
    # Construct the URL for the current page
    url = f"https://steamcommunity.com/market/search?q=case&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&category_730_Type%5B%5D=tag_Type_Hands&appid=730#p{page_num}_default_desc"

    # Set the headers to indicate desired language and currency
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Currency": "GBP"
    }
    time.sleep(2)
    # Send a GET request to the URL with the headers
    response = requests.get(url, headers=headers)

    # Parse the response HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all items on the page
    items = soup.find_all("div", {"class": "market_listing_row market_recent_listing_row market_listing_searchresult"})

    # Loop over all items on the page
    for item in items:
        # Find the name and price elements for the current item
        name_element = item.find("span", {"class": "market_listing_item_name"})
        price_element = item.find("span", {"class": "market_table_value normal_price"})

        # If both name and price elements were found
        if name_element is not None and price_element is not None:
            # Extract the name and price values
            name = name_element.text.strip()
            price = price_element.find("span", {"class": "normal_price"}).get("data-price")

            # If the item name is in the list of included names and has not been added yet, add the name and price to the respective lists
            if name in include_names and price is not None and name not in names:
                prices.append(float(price)/100)
                names.append(name)

# Create a bar chart of the prices for the included items
plt.bar(names, prices)
print(prices)
plt.xticks(rotation=90)
for i, price in enumerate(prices):
    plt.text(i, price + 0.05, f"${price:.2f}", ha="center")

# Set the title and axis labels
plt.title("CS:GO Item Prices")
plt.xlabel("Item Name")
plt.ylabel("Price (USD)")

# Show the plot
plt.show()