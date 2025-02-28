# Limit Order Optimizer 💰

This repository contains the code for a small app that helps to design limit orders for stocks and ETFs. :money_with_wings:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://limit-order-optimizer.streamlit.app/)

The app uses historical data of the fund to calculate the probability of executing a buy order with a certain discount or a sell order with a certain premium vs. today's price within a given number of days. (For instance, what is the probability of buying with a discount of -2% vs. today's price within the next 30 days?) The results are also visualized for different levels of discounts.

Users can easily upload historical data from Yahoo Finance for the stock or ETF they are interested in. If nothing is uploaded, the app shows the results for the UBS MSCI World SRI ETF (ISIN LU0629459743) between June 2018 and June 2023 as a default ([data from Yahoo Finance here](https://finance.yahoo.com/quote/UIMM.DE/history?period1=1529193600&period2=1686960000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true))

The app is built with Python :snake: , [pandas](pandas.pydata.org/) and [streamlit](https://streamlit.io/) (see also the [streamlit documentation](https://docs.streamlit.io)).

**This is information - not financial advice or any recommendation.** The content and material is for information and educational purposes only. It does not constitute financial advice or recommendation and should not be considered as such. I am not a financial advisor and not authorized to offer financial advice. Always do your own research and seek independent financial advice when required. The value of investments and any income derived from them can fall as well as rise and you may not get back the original amount you invested.
