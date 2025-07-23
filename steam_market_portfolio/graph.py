import pandas as pd
import matplotlib.pyplot as plt


def plot_portfolio_balance():
    # Load the portfolio data
    df = pd.read_csv('output/portfolio.csv')

    # Ensure acted_on is a datetime
    df['acted_on'] = pd.to_datetime(df['acted_on'])

    # Sort by date if not already sorted
    df = df.sort_values('acted_on')

    # Calculate balance change per transaction
    df['balance_change'] = df.apply(
        lambda row: row['price'] if row['gain_or_loss'] == 'sold' else -row['price'],
        axis=1
    )

    # Calculate cumulative balance
    df['cumulative_balance'] = df['balance_change'].cumsum()

    # Get first and last date for x-axis limits
    first_date = df['acted_on'].iloc[0]
    last_date = df['acted_on'].iloc[-1]

    # Plot cumulative balance over time
    plt.figure(figsize=(10, 6))
    plt.plot(df['acted_on'], df['cumulative_balance'])
    plt.xlabel('Time')
    plt.ylabel('Cumulative Balance (€)')
    plt.title('Portfolio Cumulative Balance Over Time')
    plt.xlim(first_date, last_date)
    plt.tight_layout()
    plt.savefig("output/plot.png")
