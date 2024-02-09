import pandas as pd


class PreprocessData:
    def __init__(self, from_year="1990", to_year="2020"):
        self.from_year = from_year
        self.to_year = to_year

    def cerealYieldAndTemperatureData(self, country="World"):
        cereal_yield_df = pd.read_csv("data/cereal_yield.csv")
        temperature_df = pd.read_csv("data/temperature_change.csv")
        cereal_yield = self.__process_data(
            df=cereal_yield_df,
            indicator="Cereal",
            world_calc_mode="sum",
            country=country,
        )
        temperature = self.__process_data(
            df=temperature_df,
            indicator="Temperature",
            world_calc_mode="mean",
            country=country,
        )
        return [cereal_yield, temperature]

    def temperatureAndWaterUsageData(self, country="World"):
        temperature_df = pd.read_csv("data/temperature_change.csv")
        water_usage_df = self.__preprocess_water_data(country)
        temperature = self.__process_data(
            df=temperature_df,
            indicator="Temperature",
            world_calc_mode="mean",
            country=country,
        )
        water_usage = self.__process_data(
            df=water_usage_df,
            indicator="Water Usage",
            world_calc_mode="sum",
            country=country,
        )
        return [temperature, water_usage]

    def greenhouseGasEmissionsAndTemperature(self, country="World"):
        emission_df = pd.read_csv("data/greenhouse_gas_emission.csv")
        temperature_df = pd.read_csv("data/temperature_change.csv")
        emission = self.__process_data(
            df=emission_df,
            indicator="Emissions",
            world_calc_mode="sum",
            country=country,
        )
        temperature = self.__process_data(
            df=temperature_df,
            indicator="Temperature",
            world_calc_mode="mean",
            country=country,
        )
        return [emission, temperature]

    def fertilizerAndCerealYield(self, country="World"):
        fertilizer_df = pd.read_csv("data/fertilizer.csv")
        cereal_yield_df = pd.read_csv("data/cereal_yield.csv")
        fertilizer = self.__process_data(
            df=fertilizer_df,
            indicator="Fertilizer",
            world_calc_mode="sum",
            country=country,
        )
        cereal_yield = self.__process_data(
            df=cereal_yield_df,
            indicator="Cereal",
            world_calc_mode="sum",
            country=country,
        )
        return [fertilizer, cereal_yield]

    def __process_data(
        self,
        df,
        indicator,
        world_calc_mode,
        country="World",
    ):
        """
        Process the data by reshaping, filtering, and rounding.

        Args:
          df (pandas.DataFrame): The input DataFrame containing the data.
          indicator (str): The name of the indicator column.
          world_calc_mode (str): The calculation mode for world data. 'sum' or 'mean'.
          country (str, optional): The country to filter the data. Defaults to 'World'.

        Returns:
          pandas.DataFrame: The processed data DataFrame.
        """

        if world_calc_mode != "sum" and world_calc_mode != "mean":
            raise ValueError(
                "Invalid world_calc_mode option, possible values are 'sum' or 'mean'"
            )

        # Reshape the data1 DF from wide to long format, keep necessary columns only
        data = df.melt(
            id_vars=["Country Name"],
            value_vars=[
                col for col in df.columns[:-2] if "YR" in col or col.isnumeric()
            ],
            var_name="Year",
            value_name=indicator,
        )

        # Reformat Year "XXXX [YRXXXX]" column to "XXXX"
        data["Year"] = data["Year"].str.split(" ").str[0]

        # Convert the 'indicator' columns to numeric
        data[indicator] = pd.to_numeric(data[indicator], errors="coerce")

        # Add world data to the data DataFrame
        data = self.__add_world_data(data, indicator, world_calc_mode)

        # Filter data by country argument
        data = data.query("`Country Name` == @country")

        # Round the 'indicator1' and 'indicator2' columns to 2 decimal places
        data.loc[:, [indicator]] = data[[indicator]].round(2)

        return data

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
