from flask import Flask, jsonify, request
from flask_cors import CORS

from post_process import PostProcess
from pre_process_data import PreprocessData
from predict import Predictor

app = Flask(__name__)
CORS(app)

preprocessor = PreprocessData()
predictor = Predictor(10)  # 10 years
postprocessor = PostProcess()


@app.route("/")
def index():
    return jsonify(message="Hello from Flask!")


@app.route("/cerealYieldAndTemperature")
def cereal_yield_and_temperature_data():
    country = request.args.get("country", "World")
    dfs = preprocessor.cerealYieldAndTemperatureData(country)
    predicted_dfs = []
    for df in dfs:
        predicted_dfs.append(predictor.predict(df))

    return postprocessor.process(
        predicted_dfs, "Cereal", "Temperature", "cereal_yield_and_temperature"
    )


@app.route("/temperatureAndWaterUsage")
def temperature_and_water_usage_data():
    country = request.args.get("country", "World")
    dfs = preprocessor.temperatureAndWaterUsageData(country)
    predicted_dfs = []
    for df in dfs:
        predicted_dfs.append(predictor.predict(df))

    return postprocessor.process(
        predicted_dfs, "Temperature", "Water Usage", "temperature_and_water_usage"
    )


@app.route("/greenhouseGasEmissionsAndTemperature")
def greenhouse_gas_emissions_and_temperature_data():
    country = request.args.get("country", "World")
    dfs = preprocessor.greenhouseGasEmissionsAndTemperature(country)
    predicted_dfs = []
    for df in dfs:
        predicted_dfs.append(predictor.predict(df))

    return postprocessor.process(
        predicted_dfs, "Emissions", "Temperature", "emissions_and_temperature"
    )


@app.route("/fertilizerAndCerealYield")
def fertilizer_and_cereal_yield_data():
    country = request.args.get("country", "World")
    dfs = preprocessor.fertilizerAndCerealYield(country)
    predicted_dfs = []
    for df in dfs:
        predicted_dfs.append(predictor.predict(df))

    return postprocessor.process(
        predicted_dfs, "Fertilizer", "Cereal", "fertilizer_and_cereal_yield"
    )


if __name__ == "__main__":
    app.run(debug=True)
