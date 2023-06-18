import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px

#-----------------------------------------------------------------------
# Functions
#-----------------------------------------------------------------------

# processing the data
@st.cache_data
def load_data(data):
    data['Date']= pd.to_datetime(data['Date'], format='%Y-%m-%d')
    
    data.set_index('Date', inplace=True)
    data.sort_index(ascending=True, inplace=True)
    return data

# extract lowest price for the next x days (default: 30)
def find_lowest_price(data, window_length_in_days=30):
    indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=window_length_in_days)
    data['rolling_min_price_lookahead'] = data['Low'].rolling(window = indexer).min()
    return data

# extract highest price for the next x days (default: 30)
def find_highest_price(data, window_length_in_days=30):
    indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=window_length_in_days)
    data['rolling_max_price_lookahead'] = data['High'].rolling(window = indexer).max()
    return data

# calculate discount of best possible limit order vs. today's price
def calculate_discount(data):
    # data['discount_in_perc'] = 100 - data['rolling_min_price_lookahead'] / data['Open'] * 100
    # data['discount_in_perc_neg'] = data['discount_in_perc'] * (-1)
    data['discount_in_perc'] = (data['rolling_min_price_lookahead'] / data['Open'] * 100) - 100
    return data

# calculate discount of best possible limit order vs. today's price
def calculate_premium(data):
    data['premium_in_perc'] = (data['rolling_max_price_lookahead'] / data['Open'] * 100) - 100
    return data

#-----------------------------------------------------------------------
# Layout: Sidebar
#-----------------------------------------------------------------------

with st.sidebar:
    st.subheader('Parameters')

    uploaded_file = st.file_uploader(
        label='Please upload a CSV file with historical data from Yahoo Finance',
        type=['csv'])
    
    window_length_in_days = st.slider('Order to be executed in the next x days', 1, 180, 30)
    discount = st.number_input('with a discount of -x% vs. the price of today', 0., 100., 2., 0.1)
    premium = st.number_input('with a premium of +x% vs. the price of today', 0., 100., 2., 0.1)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    # fallback option: load UBS MSCI World Socially Responsible UCITS ETF (UIMM.DE), 17.06.2018-17.06.2023
    data = pd.read_csv('data/UIMM.DE.csv', sep=',', decimal='.')

data = load_data(data)

# price lookahead in time window
data = find_lowest_price(data, window_length_in_days)
data = find_highest_price(data, window_length_in_days)

# calculate discount based on prices
data = calculate_discount(data)
data = calculate_premium(data)

# calculate probability of executing the order
probability_discount = np.sum(data['discount_in_perc'] <= (-1 * discount)) / len(data.index) * 100
probability_premium = np.sum(data['premium_in_perc'] >= premium) / len(data.index) * 100

#-----------------------------------------------------------------------
# Layout: Main Elements
#-----------------------------------------------------------------------

st.title('Limit Order Optimizer 💰')

st.write('This Streamlit app is for people who want to buy or sell stocks or funds with limit orders. 💸')
         
st.write('If you specify a timeframe in which you would like to buy/sell and the corresponding limit in percent, the app will tell you the (historical) probability of your order being executed.')

st.write('You can **upload a CSV file** for the ISIN/ticker symbol that you have in mind. It works best with data from Yahoo Finance. The data processing assumes you have a `Date` column (in the `Y-m-d` format) as well as columns for the `Open`, `High` and `Low` price of a given day.')

st.write('**If you do *not* upload a file**, the app uses data for the UBS MSCI World SRI (ISIN LU0629459743) between June 2018 and June 2023 as the default data. ([Link to Yahoo Finance](https://finance.yahoo.com/quote/UIMM.DE/history?period1=1529193600&period2=1686960000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true))')

st.info('**This is information - not financial advice or any recommendation.** Always do your own research and seek independent financial advice when required. The value of investments and any income derived from them can fall as well as rise and you may not get back the original amount you invested.', icon="⚠️")

st.subheader('What is the probability of executing this order?')

col1, col2 = st.columns(2)
col1.metric(
    "Probability: Discount of -" + str(np.round(discount, 1)) + "%",
    str(np.round(probability_discount, 1))+"%")
col2.metric(
    "Probability: Premium of +" + str(np.round(premium, 1)) + "%",
    str(np.round(probability_premium, 1))+"%")

# Create plot with empirical cumulative density of executing a buy order based on discount level
fig_probability_discount_ecdf = px.ecdf(
    data,
    x='discount_in_perc',
    title='Probability of Executing a Limit Order with a Limit of At Least -x% vs. Today',
    labels={
        'discount_in_perc': 'Limit Discount vs. Today (in Percent)'
    })

# Create plot with empirical cumulative density of executing a sell order based on premium level
fig_probability_premium_ecdf = px.ecdf(
    data,
    x='premium_in_perc',
    title='Probability of Executing a Limit Order with Limit of At Least +x% vs. today',
    labels={
        'premium_in_perc': 'Limit Premium vs. Today (in Percent)'
    })

# show plots in different tabs
tab1, tab2 = st.tabs(["Buy with Discount", "Sell with Premium"])

# tab1: buy with a discount
with tab1:
   st.header("Executing a Buy with a Discount")
   st.plotly_chart(fig_probability_discount_ecdf, use_container_width=True)
   st.write("Empirical cumulative probability of executing a Buy order with varying discount levels vs. today's opening price. Pick the discount level on the x-axis and find the corresponding probability of executing an order with this discount level.")

# tab2: sell with a premium
with tab2:
   st.header("Executing a Sell with a Premium")
   st.plotly_chart(fig_probability_premium_ecdf, use_container_width=True)
   st.write("Empirical cumulative probability of executing a Sell order with varying premium levels vs. today's opening price. Pick the premiu level on the x-axis and find the corresponding probability of executing an order with this premium level.")
