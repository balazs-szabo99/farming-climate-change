import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


class Predictor:
    def __init__(self, num_years=5):
        self.num_years = num_years

    def __predict_next_X_years(self, series):
        """
        Predicts the values for the next `self.num_years` years using ARIMA model.

        Args:
          series (pandas.Series): Time series data.

        Returns:
          numpy.ndarray: Array of predicted values for the next `self.num_years` years.
        """
        try:
            series.index = pd.DatetimeIndex(series.index, freq="AS-JAN")
            model = ARIMA(series, order=(4, 0, 4))
            model_fit = model.fit()
            output = model_fit.forecast(steps=self.num_years)
            return output
        except Exception as e:
            print(f"Failed to fit model for country: {series.name}, Error: {str(e)}")
            return None

    def predict(self, data):
        copy_df = data.copy()
        copy_df.set_index("Country Name", inplace=True)
        indicator_column = copy_df.columns[
            ~copy_df.columns.isin(["Country Name", "Year"])
        ][0]
        df_wide = copy_df.pivot(columns="Year", values=indicator_column)

        predictions = df_wide.apply(self.__predict_next_X_years, axis=1)

        predictions.columns = predictions.columns.year
        predictions.reset_index(inplace=True)
        predictions_long = predictions.melt(
            id_vars=["Country Name"], var_name="Year", value_name=indicator_column
        )
        copy_df.reset_index(inplace=True)

        final_data = pd.concat([copy_df, predictions_long], ignore_index=True)

        return final_data
