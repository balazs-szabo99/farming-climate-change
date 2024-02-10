import json

import pandas as pd

from constants import chart_info, units


class PostProcess:
    def __init__(self, from_year="1990"):
        self.from_year = from_year

    def process(self, dfs, indicator1, indicator2, info):
        """
        Process the filtered data and return a dictionary containing the processed data.

        Args:
          dfs (list): A list with 2 pandas DataFrames containing the filtered data.
          indicator1 (str): The name of the first indicator.
          indicator2 (str): The name of the second indicator.
          info (str): The information key used to retrieve chart information.

        Returns:
          dict: A dictionary containing the processed data, including the chart title,
              description, processed data in JSON format, and units for the indicators.
        """

        data = pd.merge(
            dfs[0][dfs[0]["Year"].astype(int) >= int(self.from_year)],
            dfs[1][dfs[1]["Year"].astype(int) >= int(self.from_year)],
            how="inner",
            on=["Country Name", "Year"],
        )

        return {
            "title": chart_info[info]["title"],
            "description": chart_info[info]["description"],
            "data": json.loads(data.to_json(orient="records", double_precision=2)),
            "units": {
                indicator1: units[indicator1],
                indicator2: units[indicator2],
            },
        }
