
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
yf.pdr_override()

st.set_page_config(layout="wide")
st.title("Portfolio Tracker")

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

    donut_graph = donut()
    st.plotly_chart(donut_graph)
	   


def get_integer(number):
    number_lst = list(number)
    if number_lst[-1] == 'T':
        number_lst.pop(-1)
        number_lst.append((15-(len(number_lst)-number_lst.index('.'))-2)*'0')
        number_lst.pop(number_lst.index('.'))
        return int(''.join(number_lst))
    if number_lst[-1] == 'B':
        number_lst.pop(-1)
        number_lst.append((12-(len(number_lst)-number_lst.index('.'))-2)*'0')
        number_lst.pop(number_lst.index('.'))
        return int(''.join(number_lst))
    if number_lst[-1] == 'M':
        number_lst.pop(-1)
        number_lst.append((9-(len(number_lst)-number_lst.index('.'))-2)*'0')
        number_lst.pop(number_lst.index('.'))
        return int(''.join(number_lst))
    
class Company:
    def __init__(self, ticker):
        price_df = si.get_data(ticker, datetime.now()-timedelta(days=2*365), datetime.date(datetime.now()))
        overview_df = si.get_stats(ticker)
        overview_df = overview_df.set_index('Attribute')
        overview_dict = si.get_quote_table(ticker)
        income_statement = si.get_income_statement(ticker)
        balance_sheet = si.get_balance_sheet(ticker)
        cash_flows = si.get_cash_flow(ticker)

        self.year_end = overview_df.loc['Fiscal Year Ends'][0]
        self.market_cap = get_integer(overview_dict['Market Cap'])
        self.market_cap_cs = '{:,d}'.format(int(self.market_cap))
        self.prices = price_df['adjclose']

        self.sales = income_statement.loc['totalRevenue'][0]
        self.gross_profit = income_statement.loc['grossProfit'][0]
        self.ebit = income_statement.loc['ebit'][0]
        self.interest = - income_statement.loc['interestExpense'][0]
        self.net_profit = income_statement.loc['netIncome'][0]

        self.assets = balance_sheet.loc['totalAssets'][0]
        self.currenta = balance_sheet.loc['totalCurrentAssets'][0]
        self.currentl = balance_sheet.loc['totalCurrentLiabilities'][0]
        self.working_cap = self.currenta - self.currentl
        try:                                                                                                    # Apologies for the pathetic error handling
            self.debt = balance_sheet.loc['shortLongTermDebt'][0] + balance_sheet.loc['longTermDebt'][0]
        except Exception:
            self.debt = balance_sheet.loc['longTermDebt'][0]
        self.cash = balance_sheet.loc['cash'][0]
        self.net_debt = self.debt - self.cash
        try:
            self.inventory = balance_sheet.loc['inventory'][0]
        except Exception:
            self.inventory = 'NaN'
        self.receivables = balance_sheet.loc['netReceivables'][0]
        self.payables = balance_sheet.loc['accountsPayable'][0]
        self.equity = balance_sheet.loc['totalStockholderEquity'][0]
        self.ev = self.market_cap + self.net_debt
        self.ev_cs = '{:,d}'.format(int(self.ev))

        self.operating_cf = cash_flows.loc['totalCashFromOperatingActivities'][0]
        self.investing_cf = cash_flows.loc['totalCashflowsFromInvestingActivities'][0]
        self.financing_cf = cash_flows.loc['totalCashFromFinancingActivities'][0]
        self.capex = - cash_flows.loc['capitalExpenditures'][0]
        self.free_cash_flow = self.operating_cf - self.capex

    def get_overview(self):
        self.price_earnings_ratio = self.market_cap/self.net_profit
        self.ev_sales_ratio = self.ev/self.sales
        self.overview_dict = {
            'Values' : [str(self.ev_cs), str(self.market_cap_cs), str(self.ev_sales_ratio), str(self.price_earnings_ratio)]
            }	
    
    def get_profit_margins(self):
        self.gross_margin = self.gross_profit/self.sales
        self.operating_margin = self.ebit/self.sales
        self.net_margin = self.net_profit/self.sales
        self.profit_margin_dict = {
            'Values' : [self.gross_margin, self.operating_margin, self.net_margin]
            }
    
    def get_liquidity_ratios(self):
        self.current_ratio = self.currenta/self.currentl
        if self.inventory != 'NaN':
            self.quick_ratio = (self.currenta - self.inventory)/self.currentl
        else:
            self.quick_ratio = 0
        self.cash_ratio = self.cash/self.currentl
        self.liquidity_ratio_dict = {
            'Values' : [self.current_ratio, self.quick_ratio, self.cash_ratio]
            }

    def get_leverage_ratios(self):
        self.debt_ratio = self.debt/self.assets
        self.debt_equity_ratio = self.debt/self.equity
        self.interest_coverage_ratio = self.ebit / self.interest
        self.leverage_ratio_dict = {
            'Values' : [self.debt_ratio, self.debt_equity_ratio, self.interest_coverage_ratio]
            }
        
    def get_efficiency_ratios(self):
        self.asset_turnover = self.sales/self.assets
        self.receivables_turnover = self.sales/self.receivables
        if self.inventory != 'NaN':
            self.inventory_turnover = (self.sales-self.gross_profit)/self.inventory
        else:
            self.inventory_turnover = 0
        self.efficiency_ratio_dict = {
            'Values' : [self.asset_turnover, self.receivables_turnover, self.inventory_turnover]
            }

st.title('Financial Dashboard')
ticker_input = st.text_input('Please enter your company ticker:')
search_button = st.button('Search')

if search_button:
    company = Company(ticker_input)
    company.get_overview()
    company.get_profit_margins()
    company.get_liquidity_ratios()
    company.get_leverage_ratios()
    company.get_efficiency_ratios()

    st.header('Company overview')
    overview_index = ['Enterprise value', 'Market cap', 'EV/sales ratio', 'P/E ratio']
    overview_df = pd.DataFrame(company.overview_dict, index = overview_index)
    st.line_chart(company.prices)
    st.table(overview_df)

    with st.beta_expander('Profit margins (as of {})'.format(company.year_end)):
        profit_margin_index = ['Gross margin', 'Operating margin', 'Net margin']
        profit_margin_df = pd.DataFrame(company.profit_margin_dict, index = profit_margin_index)
        st.table(profit_margin_df)
        st.bar_chart(profit_margin_df)

    with st.beta_expander('Liquidity ratios (as of {})'.format(company.year_end)):  
        liquidity_ratio_index = ['Current ratio', 'Quick ratio', 'Cash ratio']
        liquidity_ratio_df = pd.DataFrame(company.liquidity_ratio_dict, index = liquidity_ratio_index)
        st.table(liquidity_ratio_df)
        st.bar_chart(liquidity_ratio_df)

    with st.beta_expander('Leverage ratios (as of {})'.format(company.year_end)):
        leverage_ratio_index = ['Debt/total assets ratio', 'Debt/equity ratio', 'Interest coverage ratio']
        leverage_ratio_df = pd.DataFrame(company.leverage_ratio_dict, index = leverage_ratio_index)
        st.table(leverage_ratio_df)
        st.bar_chart(leverage_ratio_df)

    with st.beta_expander('Efficiency ratios (as of {})'.format(company.year_end)):
        efficiency_ratio_index = ['Asset turnover', 'Receivables turnover', 'Inventory turnover']
        efficiency_ratio_df = pd.DataFrame(company.efficiency_ratio_dict, index = efficiency_ratio_index)
        st.table(efficiency_ratio_df)
        st.bar_chart(efficiency_ratio_df)