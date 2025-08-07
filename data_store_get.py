import yfinance as yf
import pandas as pd
from datetime import date, timedelta
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd



def fetch_stock_data(nifty_50_stocks,start_date,end_date,sheet):
    stock_data={}
    for ticker in nifty_50_stocks:
        print(f"Fetching data for {ticker}...")
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            if not data.empty:
                stock_data[ticker] = data
            else:
                print(f"No data found for {ticker} in the specified date range.")
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    for ticker, df in stock_data.items():
        print(f"Processing data for {ticker}")
        if df.empty:
            print(f"Skipping empty data for {ticker}.")
            continue
        temp=[]
        for col in df.columns:
            temp.append(col[0])
        df.columns=temp
        if not df.index.name:
            df.index.name = 'Date'
        df_reset = df.reset_index()
        df_reset['Date'] = df_reset['Date'].dt.strftime('%Y-%m-%d')
        try:
            worksheet=sheet.worksheet(ticker)
            worksheet.clear()
        except gspread.WorksheetNotFound:
            print(f"Worksheet for {ticker} not found, creating a new one.")
            worksheet = sheet.add_worksheet(title=ticker, rows=df_reset.shape[0] + 1, cols=df_reset.shape[1])
        data_to_write = [df_reset.columns.tolist()] + df_reset.values.tolist()
        try:
            worksheet.update(data_to_write)
            print(f"Successfully updated worksheet for {ticker}.")
        except Exception as e:
            print(f"Failed to write data for {ticker}: {e}")
    return stock_data


def log_trade_sugnals(data,sheet,backtest_data):
    """
    Logs trade signals and backtest results to a Google Sheet.
    
    Args:
        data_dict (dict): Dictionary with stock tickers as keys and DataFrames as values.
        spreadsheet (gspread.Spreadsheet): The gspread spreadsheet object to write to.
        backtest_results (dict): Dictionary containing P&L, trade count, etc.
    """
    try:
        trade_log_ws=sheet.worksheet('Trade Log')
        trade_log_ws.clear()
    except gspread.WorksheetNotFound:
        trade_log_ws = sheet.add_worksheet(title='Trade Log', rows=100, cols=20)
    all_signals_data = []
    header = ['Date', 'Ticker', 'Close', 'Signal']
    all_signals_data.append(header)

    for ticker, df in data.items():
        signals_df = df[df['Signal'] != 'Hold'].copy()
        if not signals_df.empty:
            signals_df = signals_df.reset_index()
            signals_df['Date'] = signals_df['Date'].dt.strftime('%Y-%m-%d')
            signals_df['Ticker'] = ticker
            signals_to_write = signals_df[['Date', 'Ticker', 'Close', 'Signal']].values.tolist()
            all_signals_data.extend(signals_to_write)
    if len(all_signals_data) > 1:
        trade_log_ws.update(all_signals_data)
    else:
        trade_log_ws.update([['No trade signals generated in this period.']])
        
    print("Trade signals logged successfully.")
    try:
        summary_ws = sheet.worksheet('Summary P&L')
        summary_ws.clear()
    except gspread.WorksheetNotFound:
        summary_ws = sheet.add_worksheet(title='Summary P&L', rows=10, cols=10)
    results_df = pd.DataFrame(backtest_data).transpose().reset_index()
    results_df.rename(columns={'index': 'Ticker'}, inplace=True)
    
    pnl_data_to_write = [results_df.columns.tolist()] + results_df.values.tolist()
    summary_ws.update(pnl_data_to_write)
    print("Summary P&L logged successfully.")