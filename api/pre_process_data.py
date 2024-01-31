import json

import pandas as pd

from constants import chart_info, units


class PreprocessData:
    def __init__(self, from_year="1990", to_year="2020"):
        self.from_year = from_year
        self.to_year = to_year

    def cerealYieldAndTemperatureData(self, country="World"):
        cereal_yield_df = pd.read_csv("data/cereal_yield.csv")
        temperature_df = pd.read_csv("data/temperature.csv")
        return self.__process_data(
            df1=cereal_yield_df,
            df2=temperature_df,
            indicator1="Cereal Yield",
            indicator2="Temperature",
            info="cereal_yield_and_temperature",
            country=country,
        )

    def temperatureAndWaterUsageData(self, country="World"):
        temperature_df = pd.read_csv("data/temperature.csv")
        water_usage_df = self.__preprocess_water_data()
        return self.__process_data(
            df1=temperature_df,
            df2=water_usage_df,
            indicator1="Temperature",
            indicator2="Water Usage",
            info="temperature_and_water_usage",
            country=country,
        )

    def greenhouseGasEmissionsAndTemperature(self, country="World"):
        emission_df = pd.read_csv("data/greenhouse_gas_emission.csv")
        temperature_df = pd.read_csv("data/temperature.csv")
        return self.__process_data(
            df1=emission_df,
            df2=temperature_df,
            indicator1="Emissions",
            indicator2="Temperature",
            info="emissions_and_temperature",
            country=country,
        )

    def fertilizerAndCerealYield(self, country="World"):
        fertilizer_df = pd.read_csv("data/fertilizer.csv")
        cereal_yield_df = pd.read_csv("data/cereal_yield.csv")
        return self.__process_data(
            df1=fertilizer_df,
            df2=cereal_yield_df,
            indicator1="Fertilizer",
            indicator2="Cereal",
            info="fertilizer_and_cereal_yield",
            country=country,
        )

    def __process_data(self, df1, df2, indicator1, indicator2, info, country="World"):
        """Process two input DataFrames

        This function reshapes, filters, and merges two input Dataframes representing
        different indicators.

        Args:
        df1 (pd.DataFrame): The first DataFrame containing indicator1 data.
        df2 (pd.DataFrame): The second DataFrame containing indicator2 data.
        indicator1 (str): The name of the first indicator column.
        indicator2 (str): The name of the second indicator column.
        info (str): Key for chart information in the chart_info dictionary.
        country (str, optional): The country to filter the data for (default "World").

        Returns:
          A dictionary containing processed data, suitable for chart generation.
        """

        # Reshape the data1 DF from wide to long format, keep necessary columns only
        data1 = df1.melt(
            id_vars=["Country Name"],
            value_vars=[
                col for col in df1.columns[:-2] if "YR" in col or col.isnumeric()
            ],
            var_name="Year",
            value_name=indicator1,
        )
        data2 = df2.melt(
            id_vars=["Country Name"],
            value_vars=[
                col for col in df2.columns[:-2] if "YR" in col or col.isnumeric()
            ],
            var_name="Year",
            value_name=indicator2,
        )

        # Reformat Year "XXXX [YRXXXX]" column to "XXXX"
        data1["Year"] = data1["Year"].str.split(" ").str[0]
        data2["Year"] = data2["Year"].str.split(" ").str[0]

        # Merge filtered data1 and data2 based on 'Country Name' and 'Year'
        data = pd.merge(
            data1[data1["Year"].astype(int) >= int(self.from_year)],
            data2[data2["Year"].astype(int) >= int(self.from_year)],
            how="inner",
            on=["Country Name", "Year"],
        )

        # Convert the 'indicator1' and 'indicator2' columns to numeric
        data[indicator1] = pd.to_numeric(data[indicator1], errors="coerce")
        data[indicator2] = pd.to_numeric(data[indicator2], errors="coerce")

        # Create world data
        world_data = data.groupby("Year").sum().round(2).reset_index()
        world_data["Country Name"] = "World"

        # Add world data to the `data` dataframe
        data = pd.concat([data, world_data], ignore_index=True)

        # Filter data by country argument
        data = data.query("`Country Name` == @country")

        # Round the 'indicator1' and 'indicator2' columns to 2 decimal places
        data.loc[:, [indicator1, indicator2]] = data[[indicator1, indicator2]].round(2)

        # Return the data as a dictionary
        return {
            "title": chart_info[info]["title"],
            "description": chart_info[info]["description"],
            "data": json.loads(data.to_json(orient="records", double_precision=2)),
            "units": {
                indicator1: units[indicator1],
                indicator2: units[indicator2],
            },
        }

    def __preprocess_water_data(self):
        """Preprocess water data

        This function reads the total water usage (billion cubic meters) and
        agricultural water usage (percentage of total) data, processes it to
        return a dataframe containing the agricultural water usage in billion
        cubic meters.

        Returns:
          Dataframe containing processed water data.
        """

        water_total_data = pd.read_csv("data/water_total.csv")
        water_agro_data = pd.read_csv("data/water_agro.csv")

        # print("water_total_data", water_total_data)
        print("dtypes", water_total_data.dtypes)

        # Reshape the water data from wide to long format
        water_total_data = water_total_data.melt(
            id_vars=["Country Name"],
            value_vars=[
                col for col in water_total_data.columns[:-2] if col.isnumeric()
            ],
            var_name="Year",
            value_name="Water Usage",
        )
        water_agro_data = water_agro_data.melt(
            id_vars=["Country Name"],
            value_vars=[col for col in water_agro_data.columns[:-2] if col.isnumeric()],
            var_name="Year",
            value_name="Water Usage",
        )

        data = pd.merge(
            water_total_data[
                water_total_data["Year"].astype(int) >= int(self.from_year)
            ],
            water_agro_data[water_agro_data["Year"].astype(int) >= int(self.from_year)],
            how="inner",
            on=["Country Name", "Year"],
        )

        data = data.dropna(subset=["Water Usage_x", "Water Usage_y"])
        data["Water Usage"] = data["Water Usage_x"] * (data["Water Usage_y"] / 100)
        data = data.drop(["Water Usage_x", "Water Usage_y"], axis=1)

        return data
