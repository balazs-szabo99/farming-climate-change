from flask import Flask, jsonify, request
from flask_cors import CORS

from post_process import PostProcess
from pre_process_data import PreprocessData

app = Flask(__name__)
CORS(app)

preprocessor = PreprocessData()
postprocessor = PostProcess()


@app.route("/")
def index():
    return jsonify(message="Hello from Flask!")


@app.route("/cerealYieldAndTemperature")
def cereal_yield_and_temperature_data():
    country = request.args.get("country", "World")
    dfs = preprocessor.cerealYieldAndTemperatureData(country)
    # TODO: predict here
    # for df in dfs:
    #    ...some code that adds the predicted values to the dataframe...
    #    df = predictor.predict(df)
    return postprocessor.process(
        dfs, "Cereal", "Temperature", "cereal_yield_and_temperature"
    )


@app.route("/temperatureAndWaterUsage")
def temperature_and_water_usage_data():
    country = request.args.get("country", "World")
    dfs = preprocessor.temperatureAndWaterUsageData(country)
    # TODO: predict here
    # for df in dfs:
    #    ...some code that adds the predicted values to the dataframe...
    #    df = predictor.predict(df)
    return postprocessor.process(
        dfs, "Temperature", "Water Usage", "temperature_and_water_usage"
    )


@app.route("/greenhouseGasEmissionsAndTemperature")
def greenhouse_gas_emissions_and_temperature_data():
    country = request.args.get("country", "World")
    dfs = preprocessor.greenhouseGasEmissionsAndTemperature(country)
    # TODO: predict here
    # for df in dfs:
    #    ...some code that adds the predicted values to the dataframe...
    #    df = predictor.predict(df)
    return postprocessor.process(
        dfs, "Emissions", "Temperature", "emissions_and_temperature"
    )


@app.route("/fertilizerAndCerealYield")
def fertilizer_and_cereal_yield_data():
    country = request.args.get("country", "World")
    dfs = preprocessor.fertilizerAndCerealYield(country)
    # TODO: predict here
    # for df in dfs:
    #    ...some code that adds the predicted values to the dataframe...
    #    df = predictor.predict(df)
    return postprocessor.process(
        dfs, "Fertilizer", "Cereal", "fertilizer_and_cereal_yield"
    )


if __name__ == "__main__":
    app.run(debug=True)
