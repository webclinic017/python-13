# %% [markdown]
# simple momentum strategy
# short-term MA vs long-term MA
# 

# %%
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt


# %%
gld = pdr.get_data_yahoo('GLD')
day = np.arange(1, len(gld) + 1)
gld['Day'] = day
gld.drop(columns=['Adj Close', 'Volume'], inplace=True)
gld = gld[['Day', 'Open', 'High', 'Low', 'Close']]
gld.head()


# %%
gld.info()


# %%
# BE CAREFUL: look-ahead bias.
# shift mean skip the first MA, because we use Close price so that we can only calculate the Close 9-day MA from day 10.
gld['9-day'] = gld['Close'].rolling(9).mean().shift()
# shift has the same meaning as above
gld['21-day'] = gld['Close'].rolling(21).mean().shift()
gld[19:25]


# %%
# if 9-day >21-day, signal = 1, else signal = 0.
gld['Signal'] = np.where(gld['9-day'] > gld['21-day'], 1, 0)
# if 9-day <21-day, signal = -1, else leave the value as before.
gld['Signal'] = np.where(gld['9-day'] < gld['21-day'], -1, gld['Signal'])
# In summary, 9-day > 21-day signal = 1, < signal = -1, = signal = 0.
gld[19:30]


# %%
# drop the NaN rows.
gld.dropna(inplace=True)
gld.head()


# %%
# instantaneous returns
gld['return'] = np.log(gld['Close']).diff()  # .diff = row(n+1) - row(n)
gld['system return'] = gld['Signal'] * gld['return']
# calculate the entry points entry= 2 means from short to long, -2 from long to short, 0 remains the same position.
gld['entry'] = gld.Signal.diff()
gld[15:25]


# %%
# I dont know why I got index with duplicate values in original index. Therefore this is the code to find and remove the duplcate indicies
gld[gld.index.duplicated()]
gld = gld[~gld.index.duplicated()]


# %%
# plot the strategy
plt.rcParams['figure.figsize'] = 12, 6
plt.grid(True, alpha=0.3)
plt.plot(gld.iloc[-252:]['Close'], label='GLD')
plt.plot(gld.iloc[-252:]['9-day'], label='9-day')
plt.plot(gld.iloc[-252:]['21-day'], label='21-day')
plt.plot(gld[-252:].loc[gld.entry == 2].index, gld[-252:]
         ['9-day'][gld.entry == 2], '^', color='g', markersize=8)
plt.plot(gld[-252:].loc[gld.entry == -2].index, gld[-252:]
         ['21-day'][gld.entry == -2], 'v', color='r', markersize=8)
plt.legend(loc=2)


# %%
# plot the performance
plt.plot(np.exp(gld['return']).cumprod(), label='Buy/Hold')
plt.plot(np.exp(gld['system return']).cumprod(), label='System')
plt.legend(loc=2)
plt.grid(True, alpha=0.3)


# %%
# overall return
return_buy_hold = np.exp(gld['return']).cumprod()[-1] - 1
return_buy_hold


# %%
return_sytem = np.exp(gld['system return']).cumprod()[-1] - 1
return_sytem


# %% [markdown]
# Well, the system is pretty bad as expected. If not, we are all living in LA by now
# One more import thing is that the shift() function in the calculations of MA. Without it, we face look-ahead bias which will give us a very promising strategy
# 


