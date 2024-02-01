import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import requests
from datetime import timedelta, date
from pandas.tseries.offsets import BDay
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def create_main_dict(excel_file):
    df = pd.read_excel(excel_file)
    symbol = df['Symbol']
    company = df['Security']
    stocks = symbol.tolist()
    companies = company.to_list()

    stock_symbols = []
    for stock in stocks:
        symbol = stock + '.NS'
        stock_symbols.append(symbol)

    main_dict = {}
    for key, value in zip(companies, stock_symbols):
        main_dict[key] = value
    return main_dict

def download_stock_data(stock_symbols, start_date, end_date):
    stock_dict = {}
    for symbol in stock_symbols:
        try:
            data = yf.download(symbol, start=start_date, end=end_date, interval='1d')
            if not data.empty:
                stock_dict[symbol] = data
            else:
                print(f"WARNING: {symbol}: Data is empty, skipping.")
        except Exception as e:
            print(f"ERROR: {symbol}: {e}")
    return stock_dict


def custom_strategy(stock_dict):
    results = []

    for stock, data in stock_dict.items():
        # 52 WEEK ALL TIME HIGH
        stock_yf = yf.Ticker(stock)

        # RECENT CLOSE
        today = datetime.datetime.now()
        ndays = datetime.timedelta(days = 1)
        date = today - ndays
        end_date = date.date()

        recent_close = round(data['Close'].iloc[-1], 2)

        # REFERENCE VALUE CALCULATIONS

        # DATA FOR REFERENCE VALUE
        end_date_reference = today - datetime.timedelta(days=5)
        end_date_reference = pd.to_datetime(end_date_reference)
        data_filtered = data[data.index <= end_date_reference]

        # REFERENCE VALUE
        highest_close_candle = data_filtered[data_filtered['Close'] == data_filtered['Close'].max()]
        highest_open_candle = data_filtered[data_filtered['Open'] == data_filtered['Open'].max()]

        # Check if data_filtered is not empty
        if not data_filtered.empty:
            # Calculate highest_close_candle and highest_open_candle
            highest_close_candle = data_filtered[data_filtered['Close'] == data_filtered['Close'].max()]
            highest_open_candle = data_filtered[data_filtered['Open'] == data_filtered['Open'].max()]

            if not highest_close_candle.empty and not highest_open_candle.empty:
                if highest_close_candle['Close'].values[0] > highest_open_candle['Open'].values[0]:
                    # If the highest closing price is used, store the reference value and date
                    reference_value = round(highest_close_candle['Close'].values[0], 2)
                    reference_date = highest_close_candle.index[0]
                else:
                    # If the highest opening price is used, store the reference value and date
                    reference_value = round(highest_open_candle['Open'].values[0], 2)
                    reference_date = highest_open_candle.index[0]

        # DAYS SINCE REFERENCE VALUE
        end_date = pd.to_datetime(end_date)
        days_since_reference_day = (end_date - reference_date).days

        # MAX DIP CALCULATIONS

        # Find the rows starting from the reference date
        data_after_reference = data[data.index >= reference_date]

        # Find the minimum of 'Open' and 'Close' prices after the reference date
        min_open_or_close = min(data_after_reference['Open'].min(), data_after_reference['Close'].min())

        # Find the day (date) of the lowest open or close
        min_open_or_close_day = data_after_reference[(data_after_reference['Open'] == min_open_or_close) | (data_after_reference['Close'] == min_open_or_close)].index[0].date()
        min_open_or_close_day = pd.to_datetime(min_open_or_close_day)

        # Assign max_dip as the minimum of 'Open' and 'Close' prices
        max_dip = round(min_open_or_close, 2)

        # Days since max dip
        days_since_max_dip = (end_date - min_open_or_close_day).days


        # CROSSED DAYS CALCULATIONS

        # Number of Days where the High of the Day was more than the Reference Value
        crossed_days = data[data.index > reference_date]
        crossed_days = crossed_days[crossed_days['High'] > reference_value]
        num_crossed_days = len(crossed_days)

        results.append([stock, recent_close, reference_value, reference_date, days_since_reference_day, max_dip, min_open_or_close_day, days_since_max_dip, num_crossed_days])

    res_df = pd.DataFrame(results, columns=['Stock Symbol', 'Recent Close', 'Ref. Val', 'Ref. Date', 'Days Since Ref. Val', 'Max Dip', 'Max Dip Day', 'Days Since Max Dip', 'No. Days Threshold Breached'])

    return res_df

def main():
    # Define the paths and parameters
    excel_file = "moneycontrol/52weekhighNSE.xlsx"
    today = datetime.datetime.now()
    ndays = datetime.timedelta(days=1)
    date = (today - ndays).date()
    end_date = date.strftime("%Y-%m-%d")
    date_range = pd.date_range(end=end_date, periods=365)
    trading_dates = date_range.date.tolist()
    start_date = trading_dates[0]

    # Create the main dictionary
    main_dict = create_main_dict(excel_file)

    # Download stock data
    stock_symbols = list(main_dict.values())
    stock_dict = download_stock_data(stock_symbols, start_date, end_date)

    # Apply custom strategy
    res_df = custom_strategy(stock_dict)
    # Format dates to prevent incorrect formatting in Excel
    res_df['Ref. Date'] = res_df['Ref. Date'].dt.strftime('%Y-%m-%d')
    res_df['Max Dip Day'] = res_df['Max Dip Day'].dt.strftime('%Y-%m-%d')
    
    # Save the DataFrame to Excel with date_format specified
    res_df.to_excel("customStratRes.xlsx", index=False)
    print(res_df)

if __name__ == '__main__':
    main()

