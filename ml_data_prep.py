import pandas as pd
import numpy as np


def prepare_ml_data(df):
    #12-period ewm
    exp12=df['Close'].ewm(span=12,adjust=False).mean()
    #26-period ewm
    exp26=df['Close'].ewm(span=26,adjust=False).mean()
    df['MACD']=exp12-exp26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
     # 1 if next day's Close is higher, 0 otherwise
    df['Next_Day_Movement'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
    
    # Drop any NaN values that result from indicator calculations
    df.dropna(inplace=True)

    return df


