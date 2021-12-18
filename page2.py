
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yahoo_fin.stock_info as si

import pandas as pd
from glob import glob
from time import strftime, sleep
import numpy as np
from datetime import datetime, timedelta

from pandas_datareader import data as pdr
from pandas.tseries.offsets import BDay
import yfinance as yf

import plotly.express as px
def app():
    yf.pdr_override()

    st.title("Portfolio Tracker")

    



    # Getting input for new transaction
    st.subheader('Add new transaction:')
    ticker1 = st.text_input(label="Ticker", value="", placeholder="AAPL")
    quantity1 = st.number_input(
        "Quantity", min_value=0.01, max_value=None, step=0.01)
    date1 = st.date_input("Date", value=None)
    time1 = st.time_input("Time", value=None)
    type1 = st.radio(
        "Type",
        ('Buy', 'Sell'))
    fees1 = st.number_input("Fees", min_value=0.00, step=0.01)


    path = './inputs/transactions_all/transactions.xlsx'
    df = pd.read_excel(path)





    if st.button('Add'):
        stonk = yf.Ticker(f'{ticker1}')
        today = date1
        tomorrow = date1 + timedelta(1)
        stonk_hist = stonk.history(period='1d', start=today, end=tomorrow)
        ticker_prev_units = 0
        ticker_cml_units = 0
        ticker_cml_cost = 0
        ticker_prev_cost = 0
        price = round(stonk_hist['Open'][0],2)
        transact_val = quantity1*price
        cashflow = 0
        avg_price = 0
        unique_tickers1 = list(df['ticker'].unique())
        if ticker1 in unique_tickers1:

            df_temp = df[df['ticker'] == ticker1].iloc[-1]

            if type1 == 'Buy':
                ticker_cml_units = df_temp['cml_units'] + quantity1
            elif type1 == 'Sell':
                ticker_cml_units = df_temp['cml_units'] - quantity1

            ticker_prev_units = df_temp['cml_units']

            if type1 == 'Buy':
                ticker_cml_cost = df_temp['cml_cost'] + transact_val
            elif type1 == 'Sell':
                ticker_cml_cost = df_temp['cml_cost'] - transact_val

            ticker_prev_cost = df_temp['cml_cost']

            if type1 == 'Buy':
                cashflow = -1 * transact_val
            elif type1 == 'Sell':
                cashflow = transact_val

            avg_price = ticker_cml_cost/ticker_cml_units

        else:
            stonk = yf.Ticker(f'{ticker1}')
            today = date1
            tomorrow = date1 + timedelta(1)
            stonk_hist = stonk.history(period='1d', start=today, end=tomorrow)
            ticker_prev_units = 0
            ticker_cml_units = quantity1
            ticker_cml_cost = transact_val
            ticker_prev_cost = 0
            price = round(stonk_hist['Open'][0],2)
            transact_val = quantity1*price
            cashflow = -1 * transact_val
            avg_price = 0

        data = {"date": str(date1)+' '+str(time1),
            "type": type1,
            "ticker": ticker1,
            "quantity": quantity1,
            "price": price ,
            "fees": fees1,
            "transact_val": transact_val,
            "cashflow": cashflow,
            "prev_units": ticker_prev_units,
            "cml_units": ticker_cml_units,
            "prev_cost": ticker_prev_cost,
            "cml_cost": ticker_cml_cost,
            "avg_price": avg_price}
        df = df.append(data, ignore_index=True)
        df.to_excel('./inputs/transactions_all/transactions.xlsx', index = False)
        'Stock updated'
        df = pd.read_excel('./inputs/transactions_all/transactions.xlsx') #reading file
        df.date = pd.to_datetime(df.date, format='%d/%m/%Y')
        initial_date = '2020-05-30'  
        unique_tickers = list(df['ticker'].unique())

        # need to blacklist delisted tickers
        blacklist = ['VSLR', 'HTZ']
        filt_tickers = [tick for tick in unique_tickers if tick not in blacklist]
        print(f'You traded {len(unique_tickers)} different stocks')
        final_filtered = df[~df.ticker.isin(blacklist)] #filtered ticker list
        CHART_THEME = 'seaborn'  # Other themes like plotly_dark, seaborn, ggplot2


        # make clean headers
        def clean_header(df):
            df.columns = df.columns.str.strip().str.lower().str.replace('.', '').str.replace(
                '(', '').str.replace(')', '').str.replace(' ', '_').str.replace('_/_', '/')



        # timestamp for file names
        def get_now():
            now = datetime.now().strftime('%Y-%m-%d_%Hh%Mm')
            return now


        def donut():
            last_positions = final_filtered.groupby(['ticker']).agg({'cml_units': 'last', 'cml_cost': 'last',
                                                                 'cashflow': 'sum'}).reset_index()
            curr_prices = []
            runloop = True
            if runloop:
                for tick in last_positions['ticker']:
                    stock = yf.Ticker(tick)
                    price = stock.info['regularMarketPrice']
                    curr_prices.append(price)
                    print(f'Done for {tick}')
                runloop = False


            last_positions['price'] = curr_prices
            last_positions['current_value'] = (last_positions['price']*last_positions['cml_units']).round(2)
            last_positions['avg_price'] = (last_positions['cml_cost']/last_positions['cml_units']).round(2)
            last_positions = last_positions.sort_values(by='current_value',ascending=False)
            donut_top = go.Figure()
            donut_top.layout.template = CHART_THEME
            donut_top.add_trace(go.Pie(labels = last_positions.head(15).ticker, values = last_positions.head(15).current_value))
            donut_top.update_traces(hole=0.7,hoverinfo='label+value+percent')
            donut_top.update_traces(textposition='outside', textinfo='label+value')
            donut_top.update_layout(showlegend = False)
            donut_top.update_layout(margin = dict(t=50, b=50, l=25, r=25))
            return donut_top

        donut_graph = donut()
        st.plotly_chart(donut_graph)
    	   


        
