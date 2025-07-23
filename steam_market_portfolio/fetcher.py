import time
import steam_market_portfolio.session_utils as su


class Fetcher:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = su.get_session_with_cookies(username, password)
        self.items_left_to_fetch = None
        self.fetch_responses = []
        self.fetch_start = 0

    def fetch_items(self):
        while self.items_left_to_fetch is None or self.items_left_to_fetch > 0:
            fetch_amount = 500 if self.items_left_to_fetch is None else min(self.items_left_to_fetch, 500)
            resp = self.session.get(f"https://steamcommunity.com/market/myhistory/render/?query=&start={self.fetch_start}&count={fetch_amount}")
            
            if self.items_left_to_fetch is None:
                self.items_left_to_fetch = int(resp.json().get('total_count', 0))
            
            self.items_left_to_fetch -= fetch_amount if self.items_left_to_fetch is not None else None
            self.fetch_start += fetch_amount
            time.sleep(3)
            self.fetch_responses.append(resp.text)
            print(f"Fetched {fetch_amount} items, {len(self.fetch_responses)} responses collected.")
            print(f"Items left to fetch: {self.items_left_to_fetch if self.items_left_to_fetch is not None else 'unknown'}")
        
        return self.fetch_responses