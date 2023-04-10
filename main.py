import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None


def calculateEMA(N, values):
    alpha = 2 / (N + 1)
    ema = np.zeros(data_n)
    for day in range(0, data_n):
        numerator = 0
        denominator = 0
        for j in range(0, (N + 1)):
            if day - j < 0:
                break
            p = values[day - j]
            numerator += p * ((1 - alpha) ** j)
            denominator += (1 - alpha) ** j
        ema[day] = numerator / denominator
    return ema


def simulateProfits(start, days, values, buy_days, sell_days, is_verbose):
    balance = start
    shares = 0
    for day in range(0, days):
        if buy_days[day]:
            if is_verbose:
                print("Day " + str(day) + ": bought for " + str(round(balance, 2)) + ", value was " + str(values[day]))
            shares = balance // values[day]
            balance -= shares * values[day]
        if sell_days[day]:
            balance += shares * values[day]
            shares = 0
            if is_verbose:
                print("Day " + str(day) + ": sold for " + str(round(balance, 2)) + ", value was " + str(values[day]))
    if shares != 0:
        balance = shares * values[days - 1]
    return balance - start


# Preparation of stocks data
data_n = 1000
raw_data = pd.read_csv("data/alr_d.csv")      # data from Alior stocks, from 02/01/2019 to 15/03/2023
raw_data = raw_data[:data_n]                  # only the first 1000 days will be taken into consideration
data = raw_data[["Data", "Zamkniecie"]].copy()
data.rename(columns={"Data": "Date", "Zamkniecie": "Value"}, inplace=True)

# EMA, MACD and SIGNAL calculation
ema_12 = calculateEMA(12, data["Value"])
ema_26 = calculateEMA(26, data["Value"])
data["macd"] = ema_12 - ema_26
data["signal"] = calculateEMA(9, data["macd"])

# Intersection points calculation
buy, sell = [False], [False]
last_comparison = data["macd"][0] <= data["signal"][0]
for i in range(1, data_n):
    comparison = data["macd"][i] <= data["signal"][i]
    if comparison != last_comparison:
        if comparison:                    # MACD crossed SIGNAL from above
            sell.append(True)
            buy.append(False)
        else:                             # MACD crossed SIGNAL from below
            buy.append(True)
            sell.append(False)
    else:
        sell.append(False)
        buy.append(False)
    last_comparison = comparison
data["Buy"] = buy
data["Sell"] = sell

# Elimination of edge cases, where there is a decision to buy and sell both on the same day
for i in range(0, data_n):
    if data["Buy"][i] and data["Sell"][i]:
        data["Buy"][i] = data["Sell"][i] = False

# Indicator values with buy/sell markers
plt.plot(data.index.values, data["macd"], label="MACD")
plt.plot(data.index.values, data["signal"], label="SIGNAL")
plt.plot(data.index.values[data["Buy"]], data["signal"][data["Buy"]],
         label="Buy", marker="x", markersize=10, color="blue", linewidth=0)
plt.plot(data.index.values[data["Sell"]], data["signal"][data["Sell"]],
         label="Sell", marker="x", markersize=10, color="red", linewidth=0)
plt.title("MACD and SIGNAL lines")
plt.xlabel("Days from starting date (02/02/2019)")
plt.ylabel("Indicator value")
plt.legend()
plt.show()

# Stock values with buy/sell markers
plt.plot(data.index.values, data["Value"], label="Value")
plt.plot(data.index.values[data["Buy"]], data["Value"][data["Buy"]],
         label="Buy", marker="x", markersize=10, color="blue", linewidth=0)
plt.plot(data.index.values[data["Sell"]], data["Value"][data["Sell"]],
         label="Sell", marker="x", markersize=10, color="red", linewidth=0)
plt.title("ALR stock values")
plt.xlabel("Days from starting date (02/02/2019)")
plt.ylabel("Value [PLN]")
plt.legend()
plt.show()

# Profits simulation
initial_investment = 1000
profit = simulateProfits(initial_investment, data_n, data["Value"], data["Buy"], data["Sell"], is_verbose=True)
print("Initial balance:", initial_investment)
print("Profit:", round(profit, 2))
print("Total balance:", round(initial_investment + profit, 2))
