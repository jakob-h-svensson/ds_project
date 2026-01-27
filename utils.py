import pandas as pd
import yfinance as yf
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
from xgboost import XGBClassifier
import os
import json
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine
import inspect

# Settings and data ---------------------------

# Pathing

DATA_PATH = "data"
RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"
DB_PATH = "data/database/tickers.sqlite"

# Defining tickers/stocks
swe_stocks = {
    "ALFA.ST": "Alfa Laval",
    "ASSA-B.ST": "Assa Abloy",
    "ATCO-A.ST": "Atlas Copco A",
    "ATCO-B.ST": "Atlas Copco B",
    "AZN.ST": "AstraZeneca",
    "BOL.ST": "Boliden",
    "ELUX-B.ST": "Electrolux",
    "ERIC-B.ST": "Ericsson",
    "ESSITY-B.ST": "Essity",
    "GETI-B.ST": "Getinge",
    "HEXA-B.ST": "Hexagon",
    "HM-B.ST": "H&M",
    "INVE-B.ST": "Investor B",
    "NDA-SE.ST": "Nordea",
    "SAND.ST": "Sandvik",
    "SCA-B.ST": "SCA",
    "SEB-A.ST": "SEB A",
    "SHB-A.ST": "Handelsbanken A",
    "SKF-B.ST": "SKF B",
    "SSAB-A.ST": "SSAB A",
    "SWED-A.ST": "Swedbank A",
    "TELIA.ST": "Telia Company",
    "VOLV-B.ST": "Volvo B",
    "KINV-B.ST": "Kinnevik B",
    "LATO-B.ST": "Latour B",
    "NIBE-B.ST": "Nibe Industrier",
    "SAAB-B.ST": "Saab B",
    "LIFCO-B.ST": "Lifco B",
    "EVO.ST": "Evolution",
    "SINCH.ST": "Sinch"
}

usa_stocks = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Alphabet",
    "AMZN": "Amazon",
    "META": "Meta Platforms",
    "NVDA": "Nvidia",
    "TSLA": "Tesla",
    "AVGO": "Broadcom",
    "INTC": "Intel",
    "AMD": "Advanced Micro Devices",
    "CSCO": "Cisco Systems",
    "PEP": "PepsiCo",
    "COST": "Costco Wholesale",
    "ADBE": "Adobe",
    "NFLX": "Netflix",
    "TXN": "Texas Instruments",
    "QCOM": "Qualcomm",
    "AMGN": "Amgen",
    "HON": "Honeywell",
    "INTU": "Intuit",
    "MDLZ": "Mondelez International",
    "SBUX": "Starbucks",
    "BKNG": "Booking Holdings",
    "GILD": "Gilead Sciences",
    "ISRG": "Intuitive Surgical",
    "LRCX": "Lam Research",
    "MU": "Micron Technology",
    "REGN": "Regeneron Pharmaceuticals",
    "VRTX": "Vertex Pharmaceuticals",
    "ADP": "Automatic Data Processing"
}

# Data start and end dates
start = "2014-01-01"
start_journey = "2015-01-01"
end = "2025-12-31"


# Database functions ------------------------------------------------------
def get_db_connection():
    return create_engine(f"sqlite:///{DB_PATH}")


def interact_with_db(interaction, purpose, table=None, list_tickers=None, tickers=None, ticker_values=None): 
    """Interacting with the database, takes interaction, purpose, table, list_tickers, tickers and desired 
    ticker_values as arguments. Returns a dataframe (if reading) or a string (if writing)"""

    conn = get_db_connection()
    
    # Creating WHERE clause
    where_clause = ""
    if list_tickers:
        where_clause = f"WHERE ticker_name IN ({', '.join(['"' + ticker + '"' for ticker in list_tickers])})"
    
    # Reading from the database
    ## Getting tickers (potentially a future feature where user can select any tickers for comparison)
    if interaction == "read" and purpose == "get tickers":
        return pd.read_sql(f"SELECT * FROM tickers", conn)
    
    ## Getting ticker values
    if interaction == "read" and purpose == "get values":

        query = f"""
        SELECT 
            ticker_price.Date,
            ticker_price.Ticker,
            ticker_price.Open,
            ticker_price.High,
            ticker_price.Low,
            ticker_price.Close,
            ticker_price.Volume,
            tickers.Market
        FROM ticker_price
        JOIN tickers ON ticker_price.Ticker = tickers.Ticker
        {where_clause}
        """
        return pd.read_sql(query, conn)
        

    # Writing to the database
    ## Posting tickers and prices
    if interaction == "write" and purpose == "post tickers":
        try:
            tickers.to_sql(
                name=table,
                con=conn,
                if_exists="append",
                index=False
            )
            return True
        except Exception as e:
            print(f"Error writing to {table}: {e}")
            raise


# Data fetching and transformation ------------------------------------------------------
def fetch_and_transform_data(tickers, start, end, market):
    """Takes list of tickers, start- and end date and market as arguments. 
    Fetching data from yfinance and returns:
    - Long-format price dataframe
    - Unique tickers dataframe with market info
    """

    list_tickers = []
    unique_tickers = {} 
    
    for ticker, name in tickers.items():
        list_tickers.append(ticker)
    try:
        df = yf.download(
            list_tickers,
            start=start,
            end=end,
            progress=False
        )
    
        df_long = df.stack(level=1).rename_axis(['Date', 'Ticker']).reset_index()
        

        for i in df_long['Ticker'].unique():
            unique_tickers[i] = market
        
        unique_tickers = pd.DataFrame(unique_tickers.items(), columns=["Ticker", "Market"])

        return df_long, unique_tickers
        
    except Exception as e:
        print(e)
        return "Data not fetched"

def test():
    check_db_values = interact_with_db("read", "get values")
    return check_db_values

def extract_load():
    """Using fetch_and_transform_data to fetch data from yfinance and loading it into the database with interact_with_db"""
    try:
        check_db_values = interact_with_db("read", "get values")
        check_db_values['Date'] = pd.to_datetime(check_db_values['Date'])

        if check_db_values is not None and check_db_values['Date'].max() <= pd.to_datetime(end) and check_db_values['Date'].min() >= pd.to_datetime(start):
            status = "Success"
            return "Databasen är redan uppdaterad för åren som resan avser!", status
        
        else:    
            data_swe, unique_tickers_swe = fetch_and_transform_data(swe_stocks, start, end, market="SWE")
            return1 = interact_with_db("write", "post tickers", table="ticker_price", tickers=data_swe)
            return2 = interact_with_db("write", "post tickers", table="tickers", tickers=unique_tickers_swe)

            data_usa, unique_tickers_usa = fetch_and_transform_data(usa_stocks, start, end, market="USA")
            return3 = interact_with_db("write", "post tickers", table="ticker_price", tickers=data_usa)
            return4 = interact_with_db("write", "post tickers", table="tickers", tickers=unique_tickers_usa)

            
            if all([return1, return2, return3, return4]):
                status = "Success"
                return "Data har blivit extraherad, transformerad och laddad till databasen!", status
            else:
                status = "Fail"
                return "FEL: Data extrahering, transformation eller laddning misslyckades", status
            
    except Exception as e:
        status = "Fail"
        print(e)
        return f"FEL: Data extrahering, transformation eller laddning misslyckades: {e}", status


def create_calculated_columns():
    """Creating calculated column 'pct_change_30' for the tickers in the database."""
    df_all_tickers = interact_with_db("read", "get values")
    df_all_tickers = df_all_tickers.copy()
    df_all_tickers['pct_change_30'] = df_all_tickers.groupby('Ticker')['Close'].transform(lambda x: x.pct_change(periods=30))
    return df_all_tickers


def calculate_index():
    """Calculates the index and Index-KPIs for the tickers in the database."""

    # Reading from DB. Sorting by ticker/date and filtering to keep data from start_journey onwards
    df_long = interact_with_db("read", "get values")
    df_long = df_long.sort_values(["Ticker", "Date"]).copy()
    df_long = df_long[df_long['Date'] >= start_journey]

    # Normalizing the closing price for each ticker
    df_long["norm_close"] = df_long.groupby(["Ticker", 'Market'])["Close"].transform(
        lambda x: x / x.iloc[0]
    )


    # Calculating the index using the mean of the normalized closing price, and summing the volume for each market and date.
    # Mean values are used to get equally weighted averages (all tickers have the same weight). 
    df_norm_index = df_long.groupby(["Date", "Market"]).agg({
        "norm_close": "mean",
        "Volume": "sum"}).reset_index()


    # Calculates the volatility of the index.
    ## Starting with daily return
    df_norm_index['Daily_return'] = df_norm_index.groupby('Market')['norm_close'].pct_change()

    ## Then calculating rolling standard deviation (risk) and getting yearly volatility (x root of 252 trading days)
    df_norm_index['Volatility'] = df_norm_index.groupby('Market')['Daily_return'].transform(
        lambda x: x.rolling(30).std() * (252**0.5) * 100
    )

    # Calculates the percentage change of the index column over the last 30 days.
    df_norm_index['Pct_change_30'] = df_norm_index.groupby('Market')['norm_close'].transform(lambda x: x.pct_change(periods=30))
    return df_norm_index

# Helper functions -----------------------------------------------
def get_nearest_trading_day(df, selected_date):
    """
    Takes the index or tickers dataframe, also takes selected date from GUI.
    Returns the nearest trading day to the selected date (used for KPIs)
    """
    return (
        df
        .set_index("Date")
        .sort_index()
        .loc[:selected_date]
        .iloc[-1]
    )

def get_stocks():
    """Returns the defined tickers"""
    return swe_stocks, usa_stocks



def get_events():
    """Returns the events dataframe from the CSV"""
    events_df = pd.read_csv(f"{PROCESSED_DATA_PATH}/events.csv")
    events_df["date"] = pd.to_datetime(events_df["date"])
    events_df = events_df.sort_values("date", ascending=False)
    return events_df