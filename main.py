import analysis
import data_store_get
import pandas as pd
import yfinance as yf
import pandas as pd
import ml_data_prep
import make_predictions
from datetime import date, timedelta
import gspread
from google.oauth2.service_account import Credentials
scopes=[
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SERVICE_ACCOUNT_FILE="<credentials.json>"
SPREADSHEET_ID="<Google-Sheet-ID>"
try:
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID)
    print("Successfully connected to Google Sheets.")
except Exception as e:
    print(f"Error during Google Sheets authentication: {e}")
    exit()


nifty_50_stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS']

end_date = date.today()
start_date = end_date - timedelta(days=180)
nifty_data=data_store_get.fetch_stock_data(
    nifty_50_stocks,
    start_date,
    end_date,
    sheet
)

if nifty_data:
    for ticker in nifty_data:
        nifty_data[ticker]=analysis.calculate_indicators(nifty_data[ticker])
# print(nifty_data['RELIANCE.NS'].tail(10))

for ticker in nifty_data:
    nifty_data[ticker] = analysis.generate_signals(nifty_data[ticker])


backtest_results = {}
for ticker in nifty_data:
    backtest_results[ticker] = analysis.backtest_strategy(nifty_data[ticker])


print("\n--- Backtest Results ---")
print(pd.DataFrame(backtest_results).transpose())


data_store_get.log_trade_sugnals(nifty_data,sheet,backtest_results)
for ticker in nifty_50_stocks:
    nifty_data[ticker]=ml_data_prep.prepare_ml_data(nifty_data[ticker])

ml_result=make_predictions.train_and_evaluate_ml_model(nifty_data)
print(ml_result['accuracy'])

latest_reliance_data = nifty_data['RELIANCE.NS']
# Make a prediction
next_day_prediction = make_predictions.predict_next_day_movement(ml_result['model'], latest_reliance_data,ml_result['scaler'])
print(f"Predicted next day movement for RELIANCE.NS: {next_day_prediction}")