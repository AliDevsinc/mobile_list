import requests
from bs4 import BeautifulSoup
import csv


class Scraper:

    def __init__(self):
        self.url = "https://www.whatmobile.com.pk/Samsung_Mobiles_Prices"

    def store_in_csv(self, mobiles):
        filename = 'mobile_data.csv'
        with open(filename, 'w', newline='') as f:
            w = csv.DictWriter(f, ['name', 'price'])
            w.writeheader()
            for mobile in mobiles:
                w.writerow(mobile)

    def store_in_txt(self, high, low, avg):
        f = open("mobile_price.txt", "w")
        f.write(
            f"Maximum price is {high}, Minimum price is {low} and Average price is {avg}")
        f.close()

    def calculation(self, data):
        high_price = max(data)
        low_price = min(data)
        average_price = round(sum(data) / len(data), 2)
        self.store_in_txt(high_price, low_price, average_price)

    def clean_data(self, prices):
        data = []
        for price in prices:
            p = price.strip().split(" ")
            if p[-1] != 'N/A':
                data.append(int(p[-1].replace(",", "")))
        self.calculation(data)

    def fetch_data(self):
        mobiles = []
        prices = []
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html.parser')
        for mobile in soup.find_all('div', attrs={'class': 'item'}):
            name = mobile.find('a', attrs={'class': 'BiggerText'})
            price = mobile.find('span')
            prices.append(price.text)
            mob = {"name": name.text, "price": price.text}
            mobiles.append(mob)
        self.clean_data(prices)
        self.store_in_csv(mobiles)


obj = Scraper()
obj.fetch_data()
