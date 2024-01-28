import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# Load and preprocess the data
data = pd.read_csv("./data/greenhouse_gas_emission.csv")
data = data.filter(regex=r"Country Name|YR\d+")
data.columns = data.columns.str.replace(r"\s\[YR\d+\]", "", regex=True)
# Remove last 2021 and 2022 columns (no data available)
data = data.iloc[:, :-2]
# Mark NA
data = data.replace("..", pd.NA)

# Convert year columns to numeric type
for col in data.columns[1:]:
    data[col] = pd.to_numeric(data[col], errors="coerce")

# Calculate the mean of the other years for each country
mean_emissions = data.loc[:, data.columns != "Country Name"].mean(axis=1)

# Fill the missing values with the mean emissions
data = data.T.fillna(mean_emissions).T
data = data.dropna(subset=data.columns[1:], how="all")

# Convert year columns to numeric type
for col in data.columns[1:]:
    data[col] = pd.to_numeric(data[col])

data.set_index("Country Name", inplace=True)


def predict_next_5_years(series):
    """
    Predicts the values for the next 5 years using ARIMA model.

    Args:
      series (pandas.Series): Time series data.

    Returns:
      numpy.ndarray: Array of predicted values for the next 5 years.
    """
    try:
        series.index = pd.DatetimeIndex(series.index, freq="AS-JAN")
        model = ARIMA(series, order=(2, 0, 2))
        model_fit = model.fit()
        output = model_fit.forecast(steps=5)
        return output
    except Exception as e:
        print(f"Failed to fit model for country: {series.name}, Error: {str(e)}")
        return None


predictions = data.apply(predict_next_5_years, axis=1)
predictions.columns = predictions.columns.year
predictions.reset_index(inplace=True)
print(predictions.head(20))
