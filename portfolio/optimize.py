import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

def Optimize(array):
    df = pd.read_csv('latest_stock_prices.csv',parse_dates=True, index_col="date")

    data = df[df.columns.intersection(array)]
    data.dtypes

    mu = expected_returns.mean_historical_return(data)
    S = risk_models.sample_cov(data)

    # Optimise for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    raw_weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()

    ef.save_weights_to_file("weights.csv")  # saves to file
    print(cleaned_weights)
    ef.portfolio_performance(verbose=True)

