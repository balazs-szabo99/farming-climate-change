# AgroAware Farming Climate Change Data API

## Overview

This API serves as the backend for the "Farming Climate Change Data Visualization" app. It provides access to essential climate change data and supports the interactive features of the application.

## Recommended VS Code Extensions

For a better development experience and automated linting/formatting, we recommend installing the following extensions for Visual Studio Code:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python): Provides rich support for Python in Visual Studio Code.

- [Flake8](https://marketplace.visualstudio.com/items?itemName=me-dutour-mathieu.vscode-flake8): A linter for Python based on flake8. It helps you avoid syntax errors and keep a consistent coding style.

- [Black](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance): A Python code formatter. It helps you keep your code clean and readable.

## Activation

1. Make sure you are in the `api` folder of the project.

2. Create a virtual environment and activate it:

- On Unix or MacOS, run:

```
python -m venv venv
source venv/bin/activate
```

- On Windows, run:

```
python -m venv venv
.\venv\Scripts\activate
```

## Installing Dependencies

With the virtual environment activated, you can install the required dependencies:

1. Make sure you have Python installed on your machine.
2. Install dependencies:

```
pip install -r requirements.txt
```

## Running the API

1. Make sure you are in the `api` folder of the project.
2. Run the following command:

```
flask run --debug
```

The API will be accessible at http://127.0.0.1:5000/ by default.

## API Endpoints

`/`

- Method: GET
- Description: Retrieve a simple welcome message.
- Example Response:

```
{
  "message": "Hello from Flask!"
}
```

## Usage

You can interact with the API using tools like curl or the app's React frontend.

Example using curl:

```
curl http://127.0.0.1:5000/
```

## Data Collection & Analysis

1. Identification of specific data relevant to climate change
2. Data analysis: to be defined...

### Charts

1. Change of greenhouse gas emission and agricultural land from 1990
* Data used: 
  * Greenhouse gas emission
    * Source: https://data.worldbank.org/indicator/EN.ATM.GHGT.KT.CE
    * CSV: `greenhouse_gas_emission.csv`
  * Agricultural land
    * Source: https://data.worldbank.org/indicator/AG.LND.AGRI.K2
    * CSV: `agricultural_land.csv`
  
2. Change of greenhouse gas and cereal yield from 1990 
* Data used: 
  * Greenhouse gas emission
    * Source: https://data.worldbank.org/indicator/EN.ATM.GHGT.KT.CE
    * CSV: `greenhouse_gas_emission.csv`
  * Cereal yield
    * Source: https://data.worldbank.org/indicator/AG.YLD.CREL.KG
    * CSV: `cereal_yield.csv`

3. Change of population and arable land from 1990
* Data used: 
  * Population
    * Source: https://data.worldbank.org/indicator/SP.POP.TOTL?end=2022&start=1990
    * CSV: `population.csv`
  * Arable land
    * Source: https://data.worldbank.org/indicator/AG.LND.ARBL.HA.PC
    * CSV: `arable_land.csv`
