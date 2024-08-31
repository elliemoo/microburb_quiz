import pandas as pd
import numpy as np

# Load the CSV file
file_path = "forecast_history.csv"
forecast_data = pd.read_csv(file_path)
# forecast_data = forecast_data.apply(lambda x: x.astype(str).str.strip())
# Data Cleaning
# removing $ and %
forecast_data.replace({"\$": "", "%": "", "O": "0", "I": "1"}, regex=True, inplace=True)


# # Handle missing data by dropping rows with NaN values
forecast_data.dropna(inplace=True)

forecast_data = forecast_data.apply(lambda x: x.astype(str).str.strip())

# # # Extract actual median house prices and forecasts
actual_prices = pd.to_numeric(forecast_data["Median house price"])
westpac_forecast = pd.to_numeric(forecast_data["Westpac: 4 year forecast"])
joe_bloggs_forecast = pd.to_numeric(forecast_data["Joe Bloggs: 2 year forecast"])
harry_spent_forecast = pd.to_numeric(forecast_data["Harry Spent: 5 year forecast"])

# # # Normalise the forecasts to the actual price
westpac_forecast_adjusted = actual_prices * (1 + westpac_forecast / 100)
joe_bloggs_forecast_adjusted = actual_prices * (1 + joe_bloggs_forecast / 100)
harry_spent_forecast_adjusted = actual_prices * (1 + harry_spent_forecast / 100)

# Comparative Analysis
# Calculate deviations
westpac_deviation = np.abs(westpac_forecast_adjusted - actual_prices)
joe_bloggs_deviation = np.abs(joe_bloggs_forecast_adjusted - actual_prices)
harry_spent_deviation = np.abs(harry_spent_forecast_adjusted - actual_prices)

# Metric Calculation
# Calculate Mean Absolute Percentage Error (MAPE) for each forecaster
westpac_mape = np.mean(westpac_deviation / actual_prices) * 100
joe_bloggs_mape = np.mean(joe_bloggs_deviation / actual_prices) * 100
harry_spent_mape = np.mean(harry_spent_deviation / actual_prices) * 100

# Calculate Root Mean Squared Error (RMSE) for each forecaster
westpac_rmse = np.sqrt(np.mean(westpac_deviation**2))
joe_bloggs_rmse = np.sqrt(np.mean(joe_bloggs_deviation**2))
harry_spent_rmse = np.sqrt(np.mean(harry_spent_deviation**2))

# Compile results
results = {
    "Forecaster": ["Westpac", "Joe Bloggs", "Harry Spent"],
    "MAPE (%)": [westpac_mape, joe_bloggs_mape, harry_spent_mape],
    "RMSE": [westpac_rmse, joe_bloggs_rmse, harry_spent_rmse],
}

results_df = pd.DataFrame(results)

# Ranking based on MAPE and RMSE
results_df.sort_values(by=["MAPE (%)", "RMSE"], ascending=[True, True], inplace=True)

# Display the results
print("Forecaster Accuracy Analysis:")
print(results_df)

# Optionally, save the results to a CSV file
results_df.to_csv("forecaster_accuracy_results.csv", index=False)
