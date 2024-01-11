import pandas as pd
import json


class PreprocessData:
    def emissionsAndLand(country="World"):
        # Load data
        emissions = pd.read_csv("data/greenhouse_gas_emission.csv")
        land = pd.read_csv("data/agricultural_land.csv")

        # Reshape the emissions dataframe from wide to long format, keep necessary columns only
        emissions = emissions.melt(
            id_vars=["Country Name"],
            value_vars=[col for col in emissions.columns[:-2] if "YR" in col],
            var_name="Year",
            value_name="Emissions",
        )

        # Reshape the land dataframe from wide to long format, keep necessary columns only
        land = land.melt(
            id_vars=["Country Name"],
            value_vars=[col for col in land.columns[:-2] if "YR" in col],
            var_name="Year",
            value_name="Land",
        )

        # Reformat Year "XXXX [YRXXXX]" column to "XXXX"
        emissions["Year"] = emissions["Year"].str.split(" ").str[0]
        land["Year"] = land["Year"].str.split(" ").str[0]

        # Merge the emissions and land dataframes on 'Country Name' and 'Year'
        data = pd.merge(emissions, land, how="inner", on=["Country Name", "Year"])

        # Convert the 'Emissions' and 'Land' columns to numeric
        data["Emissions"] = pd.to_numeric(data["Emissions"], errors="coerce")
        data["Land"] = pd.to_numeric(data["Land"], errors="coerce")

        # Create world data
        world_data = data.groupby("Year").sum().round(2).reset_index()
        world_data["Country Name"] = "World"

        # Add world data to the `data` dataframe
        data = pd.concat([data, world_data], ignore_index=True)

        # Filter data by country argument
        data = data.query("`Country Name` == @country")
        # Round the 'Emissions' and 'Land' columns to 2 decimal places
        data[["Emissions", "Land"]] = data[["Emissions", "Land"]].round(2)

        # Return the data as a dictionary
        return {
            "title": "Change of greenhouse gas emission and agricultural land",
            "description": (
                "This chart represents the change in greenhouse gas emissions and "
                "agricultural land use over time for a selected country. The 'Emissions' "
                "data indicates the total greenhouse gas emissions in kilotonnes, while "
                "the 'Land' data represents the total agricultural land area in square "
                "kilometers. By visualizing these two factors together, we can gain "
                "insights into the relationship between agricultural practices and their "
                "impact on the environment."
            ),
            "data": json.loads(data.to_json(orient="records", double_precision=2)),
        }
