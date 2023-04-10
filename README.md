# MACD trading indicator

This is a python implementation of a MACD trading indicator.

The program reads data from a given .csv file, appropriately transforms it and calculates MACD and SIGNAL lines' values.
The calculated indicators for the given data are plotted on a graph, with buy/sell signals added as markers.
These buy/sell signals are also visible on a second graph that shows price history of the given data. This allows for easy analysis of the results.

The data included in this project was the price history of Alior Bank (ALR) stocks.
It includes just over a thousand days, but only the thousand last days are used in calculations.

This project was made for a university assignment. 
I've included a report written in LaTeX that was necessary to pass the task.

## Profit simulation

Apart from the indicator implementation, there is a very simple profit simulation included in the project. 
It's span is all of the data samples, which is a thousand days.

It works by a simple principle of spending all of the budget during buy signals, and selling all of the stocks on sell signals.

## Dependencies

- `pandas >= 1.5.2`
- `numpy >= 1.23.5`
- `matplotlib >= 3.6.2`

## Sources

The data that was used in this project was downloaded from [https://stooq.pl/](stooq.pl).
