# value_screener
## General
This project was created out of personal interest in a data oriented approach of the stock market. The goal was to create
    an investing recommendation tool designed for our personal needs.

## Overview
This module uses the SimFin Python API to retrieve firms' last annual financial
    statements (income statement, balance sheet and cash flow statement) and some basic data about the stock price. Using 
    this data, it allows the  calculation of financial metrics and relations, to help decide whether the firm's stock
    should be bought, sold, or held. To summarize the calculations, it allows generating a conclusive report. The metrics
    and relations in the report are all based on benchmarks that were defined by famous investors: Benjamin Graham,
    Warren Buffet, Peter Lynch and James P O'shaughnessy.
<br>**Important note #1** - the SimFin API's free version supplies financial reports with a delay of 1 year.
    Using this project with the free API version might return false or stale results.
<br>**Important note #2** - For now, this module only analyzes annual reports. In the future, we might add features to
    support analyzing the quarterly reports.

##Usage
The Firm class holds all the attributes and methods required for the analysis.
    An instance of this class represents a publicly traded firm. Once instantiated, the object reads the firm's last 
    annual financial statements (income statement, balance sheet and cash flow statement), and some basic data about the
    firm's stock value from Simfin's API. Using this data, it allows the calculation of financial metrics and relations,
    to help decide whether the firm's stock should be bought, sold, or held.
    To summarize the calculations, it allows generating a conclusive report. The metrics and relations in the report are
    all based on benchmarks that were defined by famous investors: Benjamin Graham, Warren Buffet, Peter Lynch and James
    P O'shaughnessy.
<br>**To analyze a firm, we recommend using the generate_firm_report method of the Firm class**. All the rest of the methods in this
    class are being called under the hood to create the report. The generated report is a Python Pandas DataFrame object.
    Each row in the dataframe is a benchmark used by one of the famous investors to asses whether a stock is an
    attractive investment. The dataframe contains a written explanation on the benchmark, all the related values that
    were included in the calculation, and a bottom-line recommendation by the famous investor's theory.
<br>In case that you want to use some of the other methods separately, note the naming conventions:
<br>1. Methods that start with the word 'get' are used to calculate a ratio or a metric.
<br>2. Methods that end with the word 'test' are used to check if the stock is attractive according to a specific benchmark,
    and will return a boolean value.

## Usage example
`# Instantiating  
Apple = Firm(ticker='AAPL', market='us', write_data_dir='data')`  
`Apple_report = Apple.generate_firm_report()`