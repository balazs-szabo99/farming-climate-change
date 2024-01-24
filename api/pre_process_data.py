import json

import pandas as pd
from constants import chart_info, units


class PreprocessData:
    def emissionsAndLand(self, country="World"):
        return self.__preprocess_data(
            file1="greenhouse_gas_emission",
            file2="agricultural_land",
            indicator1="Emissions",
            indicator2="Agricultural Land",
            info="emissions_and_land",
        )

    def emissionAndCerealYield(self, country="World"):
        return self.__preprocess_data(
            file1="greenhouse_gas_emission",
            file2="cereal_yield",
            indicator1="Emissions",
            indicator2="Cereal",
            info="emissions_and_cereal_yield",
        )

    def populationAndArableLand(self, country="World"):
        return self.__preprocess_data(
            file1="population",
            file2="arable_land",
            indicator1="Population",
            indicator2="Arable Land",
            info="population_and_arable_land",
        )

    def __preprocess_data(
        self, file1, file2, indicator1, indicator2, info, country="World"
    ):
        # File names = the name of the file containing data
        # Indicators = name of the value that you use in the given dataframe
        # Info = Given key of the chart_info dictionary that you are interested in
        # Load data
        data1 = pd.read_csv(f"data/{file1}.csv")
        data2 = pd.read_csv(f"data/{file2}.csv")

        # Reshape the data1 DF from wide to long format, keep necessary columns only
        data1 = data1.melt(
            id_vars=["Country Name"],
            value_vars=[col for col in data1.columns[:-2] if "YR" in col],
            var_name="Year",
            value_name=indicator1,
        )

        # Reshape the data2 DF from wide to long format, keep necessary columns only
        data2 = data2.melt(
            id_vars=["Country Name"],
            value_vars=[col for col in data2.columns[:-2] if "YR" in col],
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

        # Create world data
        world_data = data.groupby("Year").sum().round(2).reset_index()
        world_data["Country Name"] = "World"

        # Add world data to the `data` dataframe
        data = pd.concat([data, world_data], ignore_index=True)

        # Filter data by country argument
        data = data.query("`Country Name` == @country")

        # Round the 'indicator1' and 'indicator2' columns to 2 decimal places
        data[[indicator1, indicator2]] = data[[indicator1, indicator2]].round(2)

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
