import json

import pandas as pd

from constants import chart_info, units


class PreprocessData:
    def emissionsAndLand(country="World"):
        # Load data
        emissions = pd.read_csv("data/greenhouse_gas_emission.csv")
        land = pd.read_csv("data/agricultural_land.csv")

        # Reshape the emissions DF from wide to long format, keep necessary columns only
        emissions = emissions.melt(
            id_vars=["Country Name"],
            value_vars=[col for col in emissions.columns[:-2] if "YR" in col],
            var_name="Year",
            value_name="Emissions",
        )

        # Reshape the land DF from wide to long format, keep necessary columns only
        land = land.melt(
            id_vars=["Country Name"],
            value_vars=[col for col in land.columns[:-2] if "YR" in col],
            var_name="Year",
            value_name="Agricultural Land",
        )

        # Reformat Year "XXXX [YRXXXX]" column to "XXXX"
        emissions["Year"] = emissions["Year"].str.split(" ").str[0]
        land["Year"] = land["Year"].str.split(" ").str[0]

        # Merge the emissions and land dataframes on 'Country Name' and 'Year'
        data = pd.merge(emissions, land, how="inner", on=["Country Name", "Year"])

        # Convert the 'Emissions' and 'Land' columns to numeric
        data["Emissions"] = pd.to_numeric(data["Emissions"], errors="coerce")
        data["Agricultural Land"] = pd.to_numeric(
            data["Agricultural Land"], errors="coerce"
        )

        # Create world data
        world_data = data.groupby("Year").sum().round(2).reset_index()
        world_data["Country Name"] = "World"

        # Add world data to the `data` dataframe
        data = pd.concat([data, world_data], ignore_index=True)

        # Filter data by country argument
        data = data.query("`Country Name` == @country")
        # Round the 'Emissions' and 'Agricultural Land' columns to 2 decimal places
        data[["Emissions", "Agricultural Land"]] = data[
            ["Emissions", "Agricultural Land"]
        ].round(2)

        # Return the data as a dictionary
        return {
            "title": chart_info["emissions_and_land"]["title"],
            "description": chart_info["emissions_and_land"]["description"],
            "data": json.loads(data.to_json(orient="records", double_precision=2)),
            "units": {
                "Emissions": units["Emissions"],
                "Agricultural Land": units["Agricultural Land"],
            },
        }

    def emissionAndCerealYield(country="World"):
        # Load data
        emissions = pd.read_csv("data/greenhouse_gas_emission.csv")
        cereal = pd.read_csv("data/cereal_yield.csv")

        # Reshape the emissions DF from wide to long format, keep necessary columns only
        emissions = emissions.melt(
            id_vars=["Country Name"],
            value_vars=[col for col in emissions.columns[:-2] if "YR" in col],
            var_name="Year",
            value_name="Emissions",
        )

        # Reshape the cereal DF from wide to long format, keep necessary columns only
        cereal = cereal.melt(
            id_vars=["Country Name"],
            value_vars=[col for col in cereal.columns[:-2] if "YR" in col],
            var_name="Year",
            value_name="Cereal",
        )

        # Reformat Year "XXXX [YRXXXX]" column to "XXXX"
        emissions["Year"] = emissions["Year"].str.split(" ").str[0]
        cereal["Year"] = cereal["Year"].str.split(" ").str[0]

        # Merge the emissions and cereal dataframes on 'Country Name' and 'Year'
        data = pd.merge(emissions, cereal, how="inner", on=["Country Name", "Year"])

        # Convert the 'Emissions' and 'Cereal' columns to numeric
        data["Emissions"] = pd.to_numeric(data["Emissions"], errors="coerce")
        data["Cereal"] = pd.to_numeric(data["Cereal"], errors="coerce")

        # Create world data
        world_data = data.groupby("Year").sum().round(2).reset_index()
        world_data["Country Name"] = "World"

        # Add world data to the `data` dataframe
        data = pd.concat([data, world_data], ignore_index=True)

        # Filter data by country argument
        data = data.query("`Country Name` == @country")
        # Round the 'Emissions' and 'Cereal' columns to 2 decimal places
        data[["Emissions", "Cereal"]] = data[["Emissions", "Cereal"]].round(2)

        # Return the data as a dictionary
        return {
            "title": chart_info["emissions_and_cereal_yield"]["title"],
            "description": chart_info["emissions_and_cereal_yield"]["description"],
            "data": json.loads(data.to_json(orient="records", double_precision=2)),
            "units": {
                "Emissions": units["Emissions"],
                "Cereal": units["Cereal"],
            },
        }

    def populationAndArableLand(country="World"):
        # Load data
        population = pd.read_csv("data/population.csv")
        land = pd.read_csv("data/arable_land.csv")

        # Reshape population DF from wide to long format, keep necessary columns only
        population = population.melt(
            id_vars=["Country Name"],
            value_vars=[col for col in population.columns[:-2] if "YR" in col],
            var_name="Year",
            value_name="Population",
        )

        # Reshape the land DF from wide to long format, keep necessary columns only
        land = land.melt(
            id_vars=["Country Name"],
            value_vars=[col for col in land.columns[:-2] if "YR" in col],
            var_name="Year",
            value_name="Arable Land",
        )

        # Reformat Year "XXXX [YRXXXX]" column to "XXXX"
        population["Year"] = population["Year"].str.split(" ").str[0]
        land["Year"] = land["Year"].str.split(" ").str[0]

        # Merge the population and land DF on 'Country Name' and 'Year'
        data = pd.merge(population, land, how="inner", on=["Country Name", "Year"])

        # Convert the 'Population' and 'Land' columns to numeric
        data["Population"] = pd.to_numeric(data["Population"], errors="coerce")
        data["Arable Land"] = pd.to_numeric(data["Arable Land"], errors="coerce")

        # Create world data
        world_data = data.groupby("Year").sum().round(2).reset_index()
        world_data["Country Name"] = "World"

        # Add world data to the `data` dataframe
        data = pd.concat([data, world_data], ignore_index=True)

        # Filter data by country argument
        data = data.query("`Country Name` == @country")
        # Round the 'Population' and 'Arable Land' columns to 2 decimal places
        data[["Population", "Arable Land"]] = data[["Population", "Arable Land"]].round(
            2
        )

        # Return the data as a dictionary
        return {
            "title": chart_info["population_and_arable_land"]["title"],
            "description": chart_info["population_and_arable_land"]["description"],
            "data": json.loads(data.to_json(orient="records", double_precision=2)),
            "units": {
                "Population": units["Population"],
                "Arable Land": units["Arable Land"],
            },
        }

    def _preprocess_data(file1, file2, indicator1, indicator2, info, country="World"):
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
