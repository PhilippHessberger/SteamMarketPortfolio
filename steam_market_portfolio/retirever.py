from datetime import datetime
from decimal import Decimal
import json
import re


class Retriever:
    def __init__(self):
        self.balance = 0
        self.item_ids = []
        self.gain_or_loss = []
        self.item_names = []
        self.listed_on = []
        self.acted_on = []
        self.prices = []


    def retrieve(self, response_text):
        pattern = r'"descriptions"\s*:\s*\[(?:[^\[\]]+|\[(?:[^\[\]]+|\[[^\[\]]*\])*\])*\]\s*,?'
        pruned_response_text = re.sub(pattern, '', response_text, flags=re.DOTALL)

        response_json = json.loads(pruned_response_text)["assets"]["730"]["2"]

        self.extract_ids(response_json)
        self.extract_gain_or_loss(pruned_response_text)
        self.extract_item_names(response_json)
        self.extract_listed_and_acted_on(pruned_response_text)
        self.extract_prices(pruned_response_text)
    

    def calculate_balance(self):
        for i in range(len(self.item_ids)):
            if self.gain_or_loss[i] == 'bought':
                self.balance -= self.prices[i]
            elif self.gain_or_loss[i] == 'sold':
                self.balance += self.prices[i]
    

    def print_balance(self):
        print(f"Balance: {self.balance:.2f}€")


    def extract_ids(self, response_json):
        response_json_keys = list(response_json.keys())
        for i in range(len(response_json_keys)):
            self.item_ids.append(response_json[response_json_keys[i]]["id"])
    

    def extract_gain_or_loss(self, pruned_response_text):
        # gain_or_loss_pattern = r'<div class=\\"market_listing_left_cell market_listing_gainorloss\\">\\n\\t\\t(.)\\t<\\/div>'
        gain_or_loss_pattern = r'<div class=\\"market_listing_left_cell market_listing_gainorloss\\">\\n\\t\\t(.)\\t<\\/div>.{,2000}Counter-Strike 2<'
        gain_or_loss = re.findall(gain_or_loss_pattern, pruned_response_text, flags=re.DOTALL)

        for i, sign in enumerate(gain_or_loss):
            if sign == '+':
                gain_or_loss[i] = 'bought'
            elif sign == '-':
                gain_or_loss[i] = 'sold'
        
        self.gain_or_loss.extend(gain_or_loss)


    def extract_item_names(self, response_json):
        response_json_keys = list(response_json.keys())
        for i in range(len(response_json_keys)):
            self.item_names.append(str({response_json[response_json_keys[i]]["name"]}).replace(',', ''))


    def extract_listed_and_acted_on(self, pruned_response_text):
        listed_or_acted_on_pattern = r'<div class=\\"market_listing_right_cell market_listing_listed_date can_combine\\">\\n\\t\\t(.{,100}?)\\t.{,100}?market_listing_listed_date can_combine\\">\\n\\t\\t(.{,10}?)\\t.{,700}Counter-Strike 2<'
        listed_or_acted_on = re.findall(listed_or_acted_on_pattern, pruned_response_text)

        current_year = datetime.now().year
        last_month = None

        for i, date_tuple in enumerate(listed_or_acted_on):
            acted_on_str = date_tuple[0]
            listed_on_str = date_tuple[1]

            acted_on_month = datetime.strptime(acted_on_str, "%d %b").month
            if last_month is not None and acted_on_month > last_month:
                current_year -= 1
            last_month = acted_on_month

            acted_on_full_date_str = f"{acted_on_str} {current_year}"
            acted_on_date = datetime.strptime(acted_on_full_date_str, "%d %b %Y")
            self.acted_on.append(acted_on_date)

            listed_on_full_date_str = f"{listed_on_str} {current_year}"
            listed_on_date = datetime.strptime(listed_on_full_date_str, "%d %b %Y")
            self.listed_on.append(listed_on_date)


    def extract_prices(self, pruned_response_text):
        prices_pattern = r'<span class=\\"market_listing_price\\">\\n\\t\\t\\t\\t\\t\\t\\t\\t([\d,.\-]+)€\\t.{,1000}Counter-Strike 2<'
        prices = re.findall(prices_pattern, pruned_response_text, flags=re.DOTALL)

        for i, price in enumerate(prices):
            if price.endswith('--'):
                price = (price[:-2] + '00')
            prices[i] = Decimal(price.replace(',', '.'))
        
        self.prices.extend(prices)


    def to_csv(self, filename):
        with open(filename, "w") as file:
            file.write("item_id,gain_or_loss,item_name,listed_on,acted_on,price\n")
            
            for i in range(len(self.item_ids)):
                file.write(f"{self.item_ids[i]},"
                           f"{self.gain_or_loss[i]},"
                           f"{self.item_names[i]},"
                           f"{self.listed_on[i].strftime('%Y-%m-%d')},"
                           f"{self.acted_on[i].strftime('%Y-%m-%d')},"
                           f"{self.prices[i]:.2f}\n")
        print(f"Data written to {filename}")
