import datetime

import pandas as pd
import numpy as np

df_betas = pd.read_pickle('df_betas.pkl')
df_tickers = pd.read_pickle('df_tickers.pkl')

# transformations
df_tickers['market_cap_log'] = np.log(df_tickers['market_cap'])
df_tickers['market_cap_decile'] = pd.qcut(df_tickers['market_cap'], 10, labels=False)

start_date = datetime.datetime(2010,1,1)
end_date = datetime.datetime(2016,1,1)
market = 'SPY'
test_ticker = 'AAPL'
window = 100
ticker_limit = 300
ticker_choice = 'MARKETCAP' # either MARKETCAP or RANDOM
handle_nans = 'KEEP'        # either KEEP or FILLZERO
save_pickles = False        # overwrite the pickle files?

nasdaq_url = 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'

def read_nasdaq():
    df_tickers = pd.read_csv(nasdaq_url)
    df_tickers.rename(columns={ 'Symbol': 'ticker', 'Name': 'name', 'LastSale': 'last_price', 'MarketCap': 'market_cap',
                           'IPOyear': 'ipo_year', 'Sector': 'sector', 'Industry': 'industry'}, inplace=True)
    df_tickers['ipo_year'] = df_tickers['ipo_year'].convert_objects(convert_numeric=True)
    df_tickers.dropna(subset=['ipo_year'], inplace=True)
    df_tickers = (df_tickers[(df_tickers['market_cap'] > 1e9) & (df_tickers['ipo_year'] < 2010)]
        .sort_values(by='market_cap', ascending=False))
    return df_tickers

def read_market():
    import Quandl # don't import unless required
    df_market = Quandl.get('GOOG/NYSE_'+market)
    df_market.rename(columns={'Close': market}, inplace=True)
    df_market[market] = df_market[market].pct_change()
    return df_market

def build_quandl(tickers, df_changes):
    import Quandl # don't import unless required
    for t in tickers:
        try:
            df_stock = Quandl.get('WIKI/'+t, start_date='2010-01-01', end_date="2005-12-31")
        except:
            print ('{} not found in Quandl '.format(t))
            continue
        df_changes[t] = df_stock[(df_stock.index >= start_date) & (df_stock.index < end_date)]['Adj. Close']
        df_changes[t] = df_changes[t].pct_change()
        print('{} successfully pulled'.format(t))
    return df_changes

def build_betas(tickers, df_changes):
    covs = df_changes[tickers].rolling(window=window).cov(df_changes[market], pairwise=True)
    var = df_changes[market].rolling(window=window).var()
    df_betas = covs.div(var,axis=0)
    return df_betas

def recalculate():
    global df_betas, df_tickers # we'll be changing global values

    # build changes
    df_tickers = read_nasdaq()
    df_market = read_market()
    df_changes = df_market[(df_market.index >= start_date) & (df_market.index < end_date)][[market]]
    # choose tickers to work with
    if ticker_choice == 'RANDOM': tickers = np.random.choice(df_tickers['ticker'], size=ticker_limit, replace=False)
    else: tickers = list(df_tickers['ticker'].head(ticker_limit))
    if test_ticker not in tickers: tickers.append(test_ticker) # ensure test_ticker is part of our set
    df_changes = build_quandl(tickers, df_changes)
    df_changes.dropna(subset=[test_ticker], inplace=True) # drop holidays using test_ticker's calendar
    if handle_nans == 'FILLZERO': df_changes.fillna(0)
    tickers = list(set.intersection(set(df_changes.columns), tickers)) # update tickers list, drop tickers if not pulled

    # build betas
    df_betas = build_betas(tickers, df_changes)

    # build tickers
    today = df_betas.index.max()
    sr_beta_today = df_betas.loc[today]
    df_tickers = df_tickers[df_tickers['ticker'].isin(tickers)].set_index('ticker')
    df_tickers['ticker'] = df_tickers.index
    df_tickers['beta'] = sr_beta_today
    ticker_fields = ['ticker', 'name', 'beta', 'ipo_year', 'market_cap', 'sector', 'industry', 'last_price']
    df_tickers = df_tickers[ticker_fields]

    # transformations
    df_tickers['market_cap_log'] = np.log(df_tickers['market_cap'])
    df_tickers['market_cap_decile'] = pd.qcut(df_tickers['market_cap'], 10, labels=False)
    df_tickers['market_cap_mm'] = df_tickers['market_cap'] / 1e6

    # save results to pickles
    if save_pickles == True:
        df_changes.to_pickle('df_changes.pkl')
        df_betas.to_pickle('df_betas.pkl')
        df_tickers.to_pickle('df_tickers.pkl')

    # done!
    return True