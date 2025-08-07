# **Algo-Trading System with ML & Automation**

This repository contains a Python-based mini algo-trading prototype designed and developed as a solution for the given assignment. The project's objective is to demonstrate proficiency in data ingestion, implementing trading logic, automation, and basic machine learning for financial analysis.

The code is structured to be modular and well-documented, addressing the core deliverables and bonus tasks outlined in the assignment.

### **Project Features and Deliverables**

This prototype successfully implements the following key features:

* **Data Ingestion:** Fetches daily stock data for at least three NIFTY 50 stocks (RELIANCE.NS, TCS.NS, HDFCBANK.NS) for a 6-month period using the Yahoo Finance API.  
* **Trading Strategy Logic:** Implements a specific trading strategy that generates a buy signal when the Relative Strength Index (RSI) is below 30, confirmed by a 20-Day Moving Average (DMA) crossover above the 50-DMA. The system backtests this strategy to calculate performance metrics.  
* **Google Sheets Automation:** Automatically logs all relevant output to a designated Google Sheet. This includes:  
  * Raw and processed stock data for each ticker in a separate worksheet.  
  * A Trade Log containing any generated buy/sell signals.  
  * A Summary P\&L tab displaying the total P\&L, trade count, and win ratio from the backtest.  
* **Modular Code & Documentation:** The codebase is organized into logical modules with clear function definitions, extensive comments, and logging.  
* **ML Automation (Bonus):** A bonus task was implemented to create a simple machine learning model. A Logistic Regression model is trained on a combined dataset of stock indicators (RSI, MACD, Volume) to predict next-day price movement. The model's prediction accuracy is calculated and reported.

### **Project Structure**

The project is organized into the following files:

* main.py: The primary script that orchestrates the entire workflow. It fetches data, performs analysis, and logs the results.  
* data\_store\_get.py: A dedicated module for all data-related tasks, including fetching stock data and interacting with the Google Sheets API for automation.  
* analysis.py: A module containing the core analysis logic for calculating technical indicators like RSI and moving averages, and generating the rule-based trading signals.  
* ml\_data\_prep.py: This module handles the preparation of data specifically for the machine learning model, including calculating indicators like MACD and creating the target variable.  
* make\_predictions.py: This module contains the functions for training, evaluating, and using the machine learning model to make predictions.

### **How to Run the Project**

To run this project, please follow these steps:

1. **Prerequisites:** Ensure you have Python installed. Install the required libraries using pip:  
   pip install yfinance gspread pandas scikit-learn

2. **Google Sheets Setup:**  
   * Enable the Google Sheets and Google Drive APIs in the Google Cloud Console.  
   * Create a service account and download the .json key file.  
   * Share your Google Sheet with the service account's email address and grant it Editor access.  
   * Update the SERVICE\_ACCOUNT\_FILE and SPREADSHEET\_ID variables in data\_store\_get.py with your file path and spreadsheet ID.  
3. **Execution:** Run the main script from your terminal:  
   python main.py

### **Expected Output**

Upon successful execution, the script will produce the following outputs:

* **Console Output:** The terminal will display logs for data fetching, the ML model's prediction accuracy (e.g., Model prediction accuracy: 0.61), and the final backtest results.  
* **Google Sheets:** The specified Google Sheet will be populated with new tabs:  
  * Worksheets named after each stock (e.g., RELIANCE.NS) containing historical data and calculated indicators.  
  * A Trade Log tab, which will show any generated signals (e.g., a 'Sell' signal).  
  * A Summary P\&L tab, which for the given backtest period will show a P\&L, trade count, and win ratio of zero, a valid result of the backtested strategy.  
  * An ML Predictions tab (if implemented) showing the model's predictions.

### **Video Walkthroughs**

As per the assignment requirements, two short videos have been recorded to accompany this submission:

1. **Strategy and Code Flow:** A video explaining the logic behind the RSI and DMA crossover strategy, as well as a high-level overview of the modular code structure.  
2. **Console and Google Sheets Output:** A video demonstrating the execution of the script and walking through the generated output on both the console and the Google Sheets document.

This project successfully fulfills all the requirements of the assignment, demonstrating a comprehensive understanding of algo-trading principles, data analysis, and software engineering best practices.