import json

import pandas as pd

from constants import chart_info, units


class PreprocessData:
    def __init__(self, from_year="1990"):
        self.from_year = from_year

    def emissionsAndLand(self, country="World"):
        emission_df = pd.read_csv("data/greenhouse_gas_emission.csv")
        agricultural_land_df = pd.read_csv("data/agricultural_land.csv")
        return self.__process_data(
            df1=emission_df,
            df2=agricultural_land_df,
            indicator1="Emissions",
            indicator2="Agricultural Land",
            info="emissions_and_land",
            country=country,
        )

    def emissionAndCerealYield(self, country="World"):
        emission_df = pd.read_csv("data/greenhouse_gas_emission.csv")
        cereal_yield_df = pd.read_csv("data/cereal_yield.csv")
        return self.__process_data(
            df1=emission_df,
            df2=cereal_yield_df,
            indicator1="Emissions",
            indicator2="Cereal",
            info="emissions_and_cereal_yield",
            country=country,
        )

    def populationAndArableLand(self, country="World"):
        population_df = pd.read_csv("data/population.csv")
        arable_land_df = pd.read_csv("data/arable_land.csv")
        return self.__process_data(
            df1=population_df,
            df2=arable_land_df,
            indicator1="Population",
            indicator2="Arable Land",
            info="population_and_arable_land",
            country=country,
        )

    def __process_data(self, df1, df2, indicator1, indicator2, info, country="World"):
        # File names = the name of the file containing data
        # Indicators = name of the value that you use in the given dataframe
        # Info = Given key of the chart_info dictionary that you are interested in

        # Reshape the data1 DF from wide to long format, keep necessary columns only
        data1 = df1.melt(
            id_vars=["Country Name"],
            value_vars=[col for col in df1.columns[:-2] if "YR" in col],
            var_name="Year",
            value_name=indicator1,
        )

        # Reshape the data2 DF from wide to long format, keep necessary columns only
        data2 = df2.melt(
            id_vars=["Country Name"],
            value_vars=[col for col in df2.columns[:-2] if "YR" in col],
            var_name="Year",
            value_name=indicator2,
        )

        # Reformat Year "XXXX [YRXXXX]" column to "XXXX"
        data1["Year"] = data1["Year"].str.split(" ").str[0]
        data2["Year"] = data2["Year"].str.split(" ").str[0]

        # Merge the data1 and data2 DF on 'Country Name' and 'Year'
        data = pd.merge(data1, data2, how="inner", on=["Country Name", "Year"])

        # Convert the 'indicator1' and 'indicator2' columns to numeric
        data[indicator1] = pd.to_numeric(data[indicator1], errors="coerce")
        data[indicator2] = pd.to_numeric(data[indicator2], errors="coerce")

        # Filter data by years starting from self.from_year
        data = data[data["Year"].astype(int) >= int(self.from_year)]

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
