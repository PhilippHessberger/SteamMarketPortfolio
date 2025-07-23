from steam_market_portfolio.fetcher import Fetcher
from steam_market_portfolio.retirever import Retriever
from steam_market_portfolio.graph import plot_portfolio_balance


username = 'your_username'
password = 'your_password'

fetcher = Fetcher(username, password)

responses = fetcher.fetch_items()

retriever = Retriever()

for i, response in enumerate(responses):
    print(f"Processing response {i + 1}/{len(responses)}")
    retriever.retrieve(response)

retriever.calculate_balance()
retriever.print_balance()
retriever.to_csv("output/portfolio.csv")
plot_portfolio_balance()