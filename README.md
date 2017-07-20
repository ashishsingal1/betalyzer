# Betalyzer: A Full Stack Fintech Application

Betalyzer is a web application that I’ve cobbled together using various new, open source technologies that make building and deploying a fintech project easy but powerful.

Betalyzer calculates the betas of top stocks trading on the NASDAQ exchange. It displays these stocks and their betas in a table, with pages for each stock that contains details and charts about 

However, the purpose of this app is more illustrative than functional -- it serves as a guide to those who want to quickly get started . Also note that the data is frozen point in time when I created this (in Jan 2017).

To access Betalyzer, head over to [betalyzer.co]().

## Table of Contents

 - **[Functionality](#functionality)**: Overview of the summary page and ticker page.
 - **[Architecture](#architecture)**: Technologies we use and our file structure.
 - **[Data & Calculations]()**:
 - **[Web & Frontend]()**:
 - REST API & Excel
 - Analyzing the Results

## Functionality

Betalyzer consists of two templates --

1. The summary page, which contains information about all stocks
2. A ticker page, which contains information about a specific ticker

### Summary Page

This is the main landing page when a user visits the app. It includes the header, some charts on the overall market, and a table showing all the tickers.

#### Header

<< header >>

After our header and short intro, the Recalculation button allows us to refresh and recalculate the data.

#### Charts

<< charts >>

The charts show various views on 

 - Beta by Sector
 - Beta by Market Cap Decile
 - Scatter: Beta v Market Cap
 - Top Three Stocks Beta Timeseries

#### All Tickers

<< all tickers >>

The ticker table displays the list of all 

### Ticker Page

The ticker page, for example for AAPL, shows information related to a particular company.

<< analysis >>

This reference data is the same as what is displayed on the *All Tickers* table above.

<< charts >>

Three charts follow ..

 - **Beta Timeseries**: A historical timeseries of the ticker's beta versus the market.
 - **Returns Scatter**: Using the last 100 days, this is a scatter plot of market returns versus the ticker's returns.
 - **Returns Histogram**: Using the last 500 days, this is a histogram of market returns and ticker's returns.

## Architecture

### Technologies

Betalyzer makes use of many technologies, tools and services, primarily from the scientific Python libraries, but also others for specific purposes, such as data ingestion and web front end. Here's a brief overview of some of the key components --

 - [Anaconda](https://www.continuum.io/downloads): A scientific Python distribution that comes with many packages required here. Used for installing Python and related packages all at once.
 - [pandas (Python)](http://pandas.pydata.org/): Powerful data analysis package modeled after R. Used for data manipulation and calculations. 
 - [Bokeh (Python)](http://bokeh.pydata.org/en/latest/): Relatively new charting package that plays well with the rest of our stack while displaying results in JS. Used for charting on the front end.
 - [Flask (Python)](http://flask.pocoo.org/): Lightweight Python web framework that lets us get up and running quickly. 
 - [Jupyter Notebook](http://jupyter.org/): A great research environment used for scripting and visualization. Used for prototyping code as well as experimenting with different calculation methods.
 - [Quandl](https://www.quandl.com/): A repository for financial data with an easy to use API. Used as a data source.
 - [Bootstrap](http://getbootstrap.com/): A front end CSS package with easy to use components.
 - [Datatables](https://datatables.net/): A very cool JS component that makes displaying tabular data on the web a breeze.
 - [Github](https://github.com/): A Git repository with many open sourced projects.
 - [PyCharm](https://www.jetbrains.com/pycharm/): A fantastic Python IDE. Used during development.
 
Note that we don’t actually use a database in the whole project. Instead, we use pandas DataFrames stored as pickles. However, Postgres or even SQLite would suffice as a data store if some scalability is needed.

### Workflow

<< workflow image >>

 - **Get Data**: We grab data from a couple sources, including prices from Quandl and reference data from NASDAQ.
 - **Parse Data**: We parse the data, doing a bit of cleaning and then doing the calculations, primarily using pandas. 
 - **Serve Display**: We use Flask to serve the correct HTML, CSS and Javascript to the user. 
 - **Display Data**: Finally, we display the data using front end libraries like Bokeh, Bootstrap and Datatables.

### File Structure

 - **[/app.py](https://github.com/ashishsingal1/betalyzer/blob/master/app.py)**: The Flask application.
 - **[/betalyzer.py](https://github.com/ashishsingal1/betalyzer/blob/master/betalyzer.py)**: The back end code for data and calculations.
 - **/templates/**: Contains the HTML for the view layer.
   - **[index.html](https://github.com/ashishsingal1/betalyzer/blob/master/templates/index.html)**: 
   - **[main.html](https://github.com/ashishsingal1/betalyzer/blob/master/templates/main.html)**:
   - **[ticker.html](https://github.com/ashishsingal1/betalyzer/blob/master/templates/ticker.html)**:
 - **/data/**: Contains the pickled DataFrames that store the relevant data.
   - **df_betas.pkl**: Timeseries of the betas for each ticker across history.
   - **df_changes.pkl**: Timeseries of the price changes in percentage for each ticker across history.
   - **df_tickers.pkl**: Reference data for the tickers, including company name, sector, etc.
 - **/nb/**: Contains the Jupyter Notebooks that are helpful for reference.
   - **[beta-calc-optimizations.ipynb](https://github.com/ashishsingal1/betalyzer/blob/master/nb/beta-calc-optimizations.ipynb)**: Details about performant beta calculations using several methodologies.
   - **[betalyzer.ipynb](https://github.com/ashishsingal1/betalyzer/blob/master/nb/betalyzer.ipynb)**: Details about the project including answers to several common questions. 

## Data & Calculations

### Pulling Data

The first order of business is getting the data that we need. At the end of this process, we want to have two DataFrames -- one with the reference data from Nasdaq and one with price changes computed from Quandl data. The steps and code are below:

1. **[recalculate](https://github.com/ashishsingal1/betalyzer/blob/master/betalyzer.py#L73)**: First, the recalculate function is called, which takes care of both pulling the data and doing the calculations.
2. **[read_nasdaq](https://github.com/ashishsingal1/betalyzer/blob/master/betalyzer.py#L37-L45)**: We grab the data from the Nasdaq website, where the endpoint is stored in [nasdaq_url](https://github.com/ashishsingal1/betalyzer/blob/master/betalyzer.py#L24). We rename the columns, and filter the tickers to include only stocks that IPOed before 2010 (so we have enough history) and with a market cap above $1bn.
3. **[read_market](https://github.com/ashishsingal1/betalyzer/blob/master/betalyzer.py#L47-L52)**: This separately gets the index fund that we use (SPY), which is sourced from a different dataset than single stock tickers because of certain data issues.
4. **[Choosing tickers](https://github.com/ashishsingal1/betalyzer/blob/master/betalyzer.py#L80-L83)**: We choose which tickers we want to keep using our settings found at the top of the file.
5. **[build_quandl](https://github.com/ashishsingal1/betalyzer/blob/master/betalyzer.py#L54-L65)**: This is the meat of the code that injests price history. A `try` block wraps the ping to pull data, in case the data does not exist. We keep the `Adj. Close` column and calculate the `pct_change` using a convenient built in `pandas` function.
6. **[Data cleaning](https://github.com/ashishsingal1/betalyzer/blob/master/betalyzer.py#L85-L94)**: We do a bit of data cleaning -- using our reference ticker, we generate a daily schedule. We also handle missing values as specified in our settings.

We now have a cleaned pandas DataFrame that we can use to do the beta calculations.

### Beta Calculations

The code for the beta calculations is simple --

In [build_betas](https://github.com/ashishsingal1/betalyzer/blob/master/betalyzer.py#L67-L71), we use pandas' `rolling` functionality to calculate covariances and variances, and the `div` function to complete the calculation.

For a detailed look into calculation optimization, take a look at the [beta-calc-optimizations](https://github.com/ashishsingal1/betalyzer/blob/master/nb/beta-calc-optimizations.ipynb) notebook. This notebook explores three approaches (a) numpy (cov), (b) numpy (least squares) and (c) pandas rolling. The pandas function is much more highly optimized and runs all calculations in under 6 seconds, versus hours using methods (a) or (b).

### Finalizing Output

After the betas are calculated, we do a few final steps --

1. **[Build tickers](https://github.com/ashishsingal1/betalyzer/blob/master/betalyzer.py#L99-L106)**: We build a tickers DataFrame with current information, including the latest beta calculated, and only select the tickers and columns that we need to display.
2. **[Transformations](https://github.com/ashishsingal1/betalyzer/blob/master/betalyzer.py#L108-L111)**: We do a couple of transformations on market cap data for both viewability as well as charting.
3. **[Pickles](https://github.com/ashishsingal1/betalyzer/blob/master/betalyzer.py#L113-L117)**: Finally, we save down the pickles to the file system so that they can be persisted.

## Web & Front End

We now have built both the data layer as well as the calculation / quantitative layer, so we can focus on building the user interface.

### Flask App Routes

We use Flask, a lightweight Python web framework, to serve the app. A couple of [lines](https://github.com/ashishsingal1/betalyzer/blob/master/app.py#L96-L97) at the end of the file runs the app on the in built Flask web server. Should we need scale, we'd probably integrate a server like nginx.

We have three routes total -- two that correspond to the web front end, and a final one for the API.

 - **[main](https://github.com/ashishsingal1/betalyzer/blob/master/app.py#L19-L49)**: 
 - **[ticker](https://github.com/ashishsingal1/betalyzer/blob/master/app.py#L19-L49)**: 
 - **[api](https://github.com/ashishsingal1/betalyzer/blob/master/app.py#L74-L94)**: The code for this is discussed in the REST API section.

### Templates

We have three templates -- one master template and two child templates that correspond to our two pages:

 - **[index.html](https://github.com/ashishsingal1/betalyzer/blob/master/templates/index.html)**: 
 - main.html
 - ticker.html

### Front End Components

 - **Bootstrap
 - Datatables.net
 - Charting with Bokeh

## REST API & Excel

We make a REST API available for users that need to get the data programmatically. 

## Analyzing the Results

Now that we have a fully functional app, let's dig into how to analyze the results and how we may use this.
