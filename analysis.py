import pandas as pd
import numpy as np
import gspread

def calculate_indicators(df):
    df['20-DMA'] = df['Close'].rolling(window=20).mean()
    df['50-DMA'] = df['Close'].rolling(window=50).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

def generate_signals(df):
    """
    Generates 'Buy' and 'Sell' signals based on the trading strategy.
    
    Args:
        df (pd.DataFrame): DataFrame with indicator columns ('20-DMA', '50-DMA', 'RSI').
        
    Returns:
        pd.DataFrame: The DataFrame with a new 'Signal' column.
    """
    df['Signal'] = 'Hold'
    #this is to check weather the short-term dma is > than long-term dma
    dma_crossover = df['20-DMA'] > df['50-DMA']
    buy_conditions = (df['RSI'] < 30) & (dma_crossover) & (~dma_crossover.shift(1).fillna(False))
    sell_conditions = (~dma_crossover) & (dma_crossover.shift(1).fillna(False))
    df.loc[buy_conditions, 'Signal'] = 'Buy'
    df.loc[sell_conditions, 'Signal'] = 'Sell'
    
    return df


def backtest_strategy(df, initial_capital=100000):
    """
    Backtests the strategy on a single stock DataFrame and calculates P&L.
    
    Args:
        df (pd.DataFrame): DataFrame with 'Close' prices and 'Signal' column.
        initial_capital (int): The starting capital for the backtest.
        
    Returns:
        dict: A dictionary containing backtest results (P&L, win ratio, etc.).
    """
    trades = []
    position_open = False
    buy_price = 0
    trade_count = 0
    win_count = 0
    
    df = df.dropna()

    for index, row in df.iterrows():
        if row['Signal'] == 'Buy' and not position_open:
            buy_price = row['Close']
            position_open = True
            print(f"Buy Signal for {index.strftime('%Y-%m-%d')} at {buy_price:.2f}")

        elif row['Signal'] == 'Sell' and position_open:
            sell_price = row['Close']
            pnl = sell_price - buy_price
            trades.append(pnl)
            
            trade_count += 1
            if pnl > 0:
                win_count += 1
                
            position_open = False
            print(f"Sell Signal for {index.strftime('%Y-%m-%d')} at {sell_price:.2f}. P&L: {pnl:.2f}")

    total_pnl = sum(trades)
    win_ratio = (win_count / trade_count) * 100 if trade_count > 0 else 0
    
    return {
        'total_pnl': total_pnl,
        'trade_count': trade_count,
        'win_ratio': win_ratio
    }
