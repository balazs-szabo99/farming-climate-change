import pandas as pd

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
