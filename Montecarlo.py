import numpy as np
import pandas as pd
import random as rd
def montecarlo(num):
  x = pd.read_table("EURUSD_202001271400_202002101359.csv")
  ask = x.filter(items=['<ASK>'], axis=1).values
  bid = x.filter(items=['<BID>'], axis=1).values
  state_size = 1
  data = np.empty((1, 4), float)
  look_ahead = min(3000, ask.size - num)
  sell_reward = 0
  buy_reward = 0
  close_buy = 0
  close_sell = 0
  order = -1
  for i in range(state_size):
    trade = Trade()
    trade1 = Trade()
    trade.buy(ask[num], bid[num])
    trade1.sell(ask[num], bid[num])
    for j in range(look_ahead):
        if bid[j+num] > trade.holding:
            trade.close(ask[num+j], bid[num+j])
            close_buy = 1

        if trade1.holding > ask[j+num] :
            trade1.close(ask[num+j], bid[num+j])
            close_sell = 1

    if close_sell == 0:
        trade1.close(ask[num+look_ahead - 1], bid[num+look_ahead - 1])
    elif close_sell == 1:
        close_sell = 0
    
    if close_buy == 0:
        trade.close(ask[num+look_ahead - 1], bid[num+look_ahead - 1])
    elif close_buy == 1:
        close_buy = 0
    
    if trade.profit > 0 and trade.profit > trade1.profit:
        buy_reward = 1
        sell_reward = 0
    elif trade1.profit > 0 and trade.profit < trade1.profit:
        buy_reward = 0
        sell_reward = 1

    del trade
    del trade1

    # rand = np.random.randint(low=0, high=101)
    # buy_reward = buy_reward*rand
    # sell_reward = sell_reward*(100-rand)


    data[i] = np.array([[ask[num], bid[num], buy_reward, sell_reward]])

    buy_reward = 0
    sell_reward = 0
    close_flag = 0
    return data