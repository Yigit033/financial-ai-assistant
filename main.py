from neuralintents.assistants import BasicAssistant  # Use BasicAssistant
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import mplfinance as mpf


import pickle
import sys
import datetime as dt




with open("AI_Assistant/stocks.pkl", "rb") as f:
   # rb = read binary
   stocks = pickle.load(f)  # load the object from the file
   
# print(stocks)

# 
def save_stocks(): # save the stocks to the file every time when we run this function
   with open("AI_Assistant/stocks.pkl", "wb") as f:
      # wb = write binary
      pickle.dump(stocks, f)


def add_stocks():
   ticker = input("Which stock do you want to add?: ")
   amount = input("How many shares do you want to add?: ")

   if ticker in stocks.keys():
      stocks[ticker] += int(amount)
   else:
      stocks[ticker] = int(amount)

def remove_stocks():
   ticker = input("Which stock do you want to remove?: ")
   amount = input("How many shares do you want to remove?: ")

   if ticker in stocks.keys():
      if stocks[ticker] > int(amount):
         stocks[ticker] -= int(amount)
      else:
         print("You do not have that much shares to remove")
   else:
      print(f"You do not own any shares of {ticker}")
save_stocks()

def show_stocks():
   print("Your Portfolio: ")
   for ticker in stocks.keys():
      print(f" Your own {stocks[ticker]} shares of {ticker}")




def stocks_worth():
   total_worth = 0
   for ticker in stocks.keys():
      stock = web.DataReader(ticker, "yahoo") # get the stock data from yahoo finance, "yahoo" = data source, 
      current_price = stock.iloc[-1]["Close"] # last close price of the stock(hisse senedinin son kapanış fiyatı)  , iloc[-1] = last row(son satır), ["Close"] = close price,   
      total_worth += stocks[ticker] * current_price # 
   print(f"Your total portfolio worth is: {total_worth} USD")

def stocks_gains():
   starting_data = input("Enter a data for comparison (yyyy-mm-dd): ") # get the date from the user
   
   sum_now = 0
   sum_then = 0

   try:
      for ticker in stocks.keys(): # iterate over the stocks
         data  = web.DataReader(ticker, "yahoo") # get the stock data from yahoo finance, "yahoo" = data source,
         price_now = data.iloc[-1]["Close"]
         price_then = data.loc[data.index == starting_data]["Close"].values[0]  # get the price of the stock on the given date
         sum_now += price_now 
         sum_then += price_then

         print(f"Relative Gains: {((sum_now - sum_then) / sum_then) * 100}%")
         print(f"Absulute Gains: {sum_now - sum_then} USD")
   except IndexError:
      print("There is no any trading on this day")

def plot_chart():
   ticker = input("Which stock do you want to plot?: ")
   starting_string = input("Enter a starting date for the chart (yyyy-mm-dd): ")

   plt.style.use("dark_background") # set the style of the chart

   start = dt.datetime.strptime(starting_string, "%d/%m/%Y") # convert the string to datetime object
   end = dt.datetime.now() # get the current date

   data = web.DataReader(ticker, "yahoo", start, end) # get the stock data from yahoo finance, "yahoo" = data source,

   colors = mpf.make_marketcolors(up="g", down="r", inherit=True) # set the colors of the chart

   mpf_style = mpf.make_mpf_style(base_mpf_style = "nightclouds", marketcolors = colors) # set the style of the chart

   mpf.plot(data, type="candle", volume=True, style=mpf_style) # plot the chart of the stock


def bye():
   print("Goodbye")
   sys.exist(0)


mappings = {
   "plot_chart" : plot_chart,
   "add_stocks" : add_stocks,
   "remove_stocks" : remove_stocks,
   "show_stocks" : show_stocks,
   "stocks_worth" : stocks_worth,
   "stocks_gains" : stocks_gains,
   "bye" : bye
}

assistant = BasicAssistant("AI_Assistant/intents.json", mappings, "financial_assistant_model")

assistant.fit_model() # train the model

assistant.save_model()

while True:
   message = input(" Enter a message:")
   assistant.request(message)

# from neuralintents.assistants import BasicAssistant


# stocks = ['AAPL', 'META', 'TSLA', 'NVDA']


# def print_stocks():
#     print(f'Stocks: {stocks}')


# assistant = BasicAssistant('intents1.json', method_mappings={
#     "stocks": print_stocks,
#     "goodbye": lambda: exit(0)
# })

# # assistant.fit_model(epochs=50)
# # assistant.save_model()

# assistant.load_model()

# done = False

# while not done:
#     message = input("Enter a message: ")
#     if message == "STOP":
#         done = True
#     else:
#         print(assistant.process_input(message))