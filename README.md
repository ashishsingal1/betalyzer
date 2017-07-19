# Betalyzer: A Full Stack Fintech Application

Betalyzer is a web application that I’ve cobbled together using various new, open source technologies that make building and deploying a fintech project easy but powerful.

Betalyzer calculates the betas of top stocks trading on the NASDAQ exchange. It displays these stocks and their betas in a table, with pages for each stock that contains details and charts about 

However, the purpose of this app is more illustrative than functional -- it serves as a guide to those who want to quickly get started . Also note that the data is frozen point in time when I created this (in Jan 2017).

To access Betalyzer, head over to [betalyzer.co]().

## Table of Contents

 - *Functionality*: Overview of the summary page and ticker page
 - Architecture: Technologies we use and our file structure.
 - Data & Calculations
 - Web & Frontend
 - REST API & Excel
 - Analyzing the Results

## Functionality

Betalyzer consists of two templates --

1. The summary page, which contains information about all stocks
2. A ticker page, which contains information about a specific ticker

### Summary Page



### Ticker Page

## Architecture

### Technologies

Betalyzer makes use of many technologies, tools and services, primarily from the scientific Python libraries, but also others for specific purposes, such as data ingestion and web front end. Here's a brief overview of some of the key components --

 - (Anaconda)[]: A scientific Python distribution that comes with many packages required here.
 - pandas (Python): Powerful data analysis package modeled after R. 
 - Bokeh (Python): Relatively new charting package that plays well with the rest of our stack while displaying results in JS.
 - Flask (Python): Lightweight Python web framework that lets us get up and running quickly.
 - Jupyter Notebook: A great research environment used for scripting and visualization.
 - Quandl: A repository for financial data with an easy to use API.
 - Bootstrap: A front end CSS package with easy to use components.
 - Datatables: A very cool JS component that makes displaying tabular data on the web a breeze.
 - Github: A Git repository with many open sourced projects.
 - PyCharm: A fantastic Python IDE.
 
Note that we don’t actually use a database in the whole project. Instead, we use pandas DataFrames converted into pickles. However, Postgres or even SQLite would suffice as a data store.

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

The first order of business is getting the data that we need. There are two primary calls that we need to make:

 - Ticker List: A list of all stocks 
 - Historical Prices: For each stock, we need historical prices

For this project, we restrict ourselves to free sources that can be accessed via an API.

### Beta Calculations

## Web & Front End

### Flask App Framework

### Templates

### Bootstrap

### Datatables.js

### Charting with Bokeh

## REST API & Excel

We make a REST API available for users that need to get the data programmatically. 

## Analyzing the Results

Now that we have a fully functional app, let's dig into how to analyze the results and how we may use this.
