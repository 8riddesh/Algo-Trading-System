from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import pandas as pd


def train_and_evaluate_ml_model(data_dict):
    """
    Trains a Logistic Regression model on combined stock data and evaluates its accuracy.
    
    Args:
        data_dict (dict): Dictionary of DataFrames with prepared ML data.
        
    Returns:
        dict: A dictionary containing the model's accuracy.
    """
    # Combine all DataFrames into a single one for training
    combined_df = pd.concat(data_dict.values(), axis=0)

    # Define features and target
    features = ['RSI', 'MACD', 'MACD_Signal', 'Volume']
    target = 'Next_Day_Movement'

    X = combined_df[features]
    y = combined_df[target]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train.values)
    X_test_scaled = scaler.transform(X_test.values)
    # Initialize and train the model (Logistic Regression in this example)
    model = LogisticRegression(random_state=42, max_iter=900)
    
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Model prediction accuracy: {accuracy:.2f}")

    return {'accuracy': accuracy,'model':model,'scaler':scaler}

def predict_next_day_movement(model,df,scaler):
    """
    Uses the trained model to predict the next day's stock movement.
    
    Args:
        model: The trained scikit-learn model.
        df (pd.DataFrame): The DataFrame containing the latest stock data, with indicators.
        
    Returns:
        str: A string indicating the predicted movement ('Up' or 'Down').
    """
    # Use the last row of the DataFrame for prediction
    latest_data = df.iloc[[-1]]
    
    # Define features, making sure they match the ones used for training
    features = ['RSI', 'MACD', 'MACD_Signal', 'Volume']
    
    # Select the features for the latest data point
    X_latest = latest_data[features].values

    X_latest_scaled=scaler.transform(X_latest)
    
    # Use the model to predict the next day's movement
    prediction = model.predict(X_latest_scaled)
    
    # Interpret the prediction
    if prediction[0] == 1:
        return 'Up'
    else:
        return 'Down'