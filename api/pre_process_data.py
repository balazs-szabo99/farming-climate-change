import json

import pandas as pd

from constants import chart_info, units


class PreprocessData:
    def __init__(self, from_year="1990", to_year="2020"):
        self.from_year = from_year
        self.to_year = to_year

    def cerealYieldAndTemperatureData(self, country="World"):
        cereal_yield_df = pd.read_csv("data/cereal_yield.csv")
        temperature_df = pd.read_csv("data/temperature_change.csv")
        return self.__process_data(
            df1=cereal_yield_df,
            df2=temperature_df,
            indicator1="Cereal",
            indicator2="Temperature",
            info="cereal_yield_and_temperature",
            df1_world_calc_mode="sum",
            df2_world_calc_mode="mean",
            country=country,
        )

    def temperatureAndWaterUsageData(self, country="World"):
        temperature_df = pd.read_csv("data/temperature_change.csv")
        water_usage_df = self.__preprocess_water_data(country)
        return self.__process_data(
            df1=temperature_df,
            df2=water_usage_df,
            indicator1="Temperature",
            indicator2="Water Usage",
            info="temperature_and_water_usage",
            df1_world_calc_mode="mean",
            df2_world_calc_mode="sum",
            country=country,
        )

    def greenhouseGasEmissionsAndTemperature(self, country="World"):
        emission_df = pd.read_csv("data/greenhouse_gas_emission.csv")
        temperature_df = pd.read_csv("data/temperature_change.csv")
        return self.__process_data(
            df1=emission_df,
            df2=temperature_df,
            indicator1="Emissions",
            indicator2="Temperature",
            info="emissions_and_temperature",
            df1_world_calc_mode="sum",
            df2_world_calc_mode="mean",
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
            df1_world_calc_mode="mean",
            df2_world_calc_mode="mean",
            country=country,
        )

    def __process_data(
        self,
        df1,
        df2,
        indicator1,
        indicator2,
        info,
        df1_world_calc_mode,
        df2_world_calc_mode,
        country="World",
    ):
        """Process two input DataFrames

        This function reshapes, filters, and merges two input Dataframes representing
        different indicators.

        Args:
        df1 (pd.DataFrame): The first DataFrame containing indicator1 data.
        df2 (pd.DataFrame): The second DataFrame containing indicator2 data.
        indicator1 (str): The name of the first indicator column.
        indicator2 (str): The name of the second indicator column.
        info (str): Key for chart information in the chart_info dictionary.
        df1_world_calc_mode (str): Mode to calculate world data, options "sum"/"mean".
        df2_world_calc_mode (str): Mode to calculate world data, options "sum"/"mean".
        country (str, optional): The country to filter the data for (default "World").

        Returns:
          A dictionary containing processed data, suitable for chart generation.
        """

        if (df1_world_calc_mode != "sum" and df1_world_calc_mode != "mean") or (
            df2_world_calc_mode != "sum" and df2_world_calc_mode != "mean"
        ):
            raise ValueError(
                "Invalid world_calc_mode option, possible values are 'sum' or 'mean'"
            )

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

        # Convert the 'indicator1' and 'indicator2' columns to numeric
        data1[indicator1] = pd.to_numeric(data1[indicator1], errors="coerce")
        data2[indicator2] = pd.to_numeric(data2[indicator2], errors="coerce")

        # Add world data to the data1 and data2 DataFrames
        data1 = self.__add_world_data(data1, indicator1, df1_world_calc_mode)
        data2 = self.__add_world_data(data2, indicator2, df2_world_calc_mode)

        # Merge filtered data1 and data2 based on 'Country Name' and 'Year'
        data = pd.merge(
            data1[data1["Year"].astype(int) >= int(self.from_year)],
            data2[data2["Year"].astype(int) >= int(self.from_year)],
            how="inner",
            on=["Country Name", "Year"],
        )

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

    def __preprocess_water_data(self, country="World"):
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

        # Drops rows with missing values between the from_year and to_year
        water_total_data = water_total_data.dropna(
            subset=[
                col
                for col in water_total_data.columns
                if col.isnumeric()
                and int(col) >= int(self.from_year) + 5
                and int(col) <= int(self.to_year) - 5
            ]
        )
        water_agro_data = water_agro_data.dropna(
            subset=[
                col
                for col in water_agro_data.columns
                if col.isnumeric()
                and int(col) >= int(self.from_year) + 5
                and int(col) <= int(self.to_year) - 5
            ]
        )

        # Drop rows with "World" in the "Country Name" column
        water_total_data = water_total_data[water_total_data["Country Name"] != "World"]
        water_agro_data = water_agro_data[water_agro_data["Country Name"] != "World"]

        # Reshape the water data from wide to long format
        water_total_data = water_total_data.melt(
            id_vars=["Country Name"],
            value_vars=[
                col
                for col in water_total_data.columns[:-2]
                if col.isnumeric()
                and int(col) >= int(self.from_year)
                and int(col) <= int(self.to_year)
            ],
            var_name="Year",
            value_name="Water Usage",
        )
        water_agro_data = water_agro_data.melt(
            id_vars=["Country Name"],
            value_vars=[
                col
                for col in water_agro_data.columns[:-2]
                if col.isnumeric()
                and int(col) >= int(self.from_year)
                and int(col) <= int(self.to_year)
            ],
            var_name="Year",
            value_name="Water Usage",
        )

        # Calculate world data to the water_total_data and water_agro_data DataFrames
        water_total_data = self.__add_world_data(water_total_data, "Water Usage", "sum")
        water_agro_data = self.__add_world_data(water_agro_data, "Water Usage", "mean")

        # Filter data by country argument
        water_total_data = water_total_data.query("`Country Name` == @country")
        water_agro_data = water_agro_data.query("`Country Name` == @country")

        data = pd.merge(
            water_total_data,
            water_agro_data,
            how="inner",
            on=["Country Name", "Year"],
        )

        data = data.dropna(subset=["Water Usage_x", "Water Usage_y"])
        data["Water Usage"] = (
            data["Water Usage_x"] * (data["Water Usage_y"] / 100) * 1000000
        )
        data = data.drop(["Water Usage_x", "Water Usage_y"], axis=1)
        data = data.pivot(index="Country Name", columns="Year", values="Water Usage")
        data.reset_index(inplace=True)
        data.rename_axis(None, axis=1, inplace=True)
        return data

    def __add_world_data(self, data, indicator, world_calc_mode):
        # Check if there is no "World" row in the data
        if "World" not in data["Country Name"].unique():
            world_data = (
                data.groupby("Year")
                .agg(
                    {
                        indicator: world_calc_mode,
                    }
                )
                .round(2)
                .reset_index()
            )
            world_data["Country Name"] = "World"
            data = pd.concat([data, world_data], ignore_index=True)
        return data
