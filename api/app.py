from flask import Flask, jsonify, request
from flask_cors import CORS

from pre_process_data import PreprocessData

app = Flask(__name__)
CORS(app)

preprocessor = PreprocessData()


@app.route("/")
def index():
    return jsonify(message="Hello from Flask!")


@app.route("/cerealYieldAndTemperature")
def cereal_yield_and_temperature_data():
    country = request.args.get("country", "World")
    return preprocessor.cerealYieldAndTemperatureData(country)


@app.route("/temperatureAndWaterUsage")
def temperature_and_water_usage_data():
    country = request.args.get("country", "World")
    return preprocessor.temperatureAndWaterUsageData(country)


@app.route("/greenhouseGasEmissionsAndTemperature")
def greenhouse_gas_emissions_and_temperature_data():
    country = request.args.get("country", "World")
    return preprocessor.greenhouseGasEmissionsAndTemperature(country)


@app.route("/fertilizerAndCerealYield")
def fertilizer_and_cereal_yield_data():
    country = request.args.get("country", "World")
    return preprocessor.fertilizerAndCerealYield(country)


if __name__ == "__main__":
    app.run(debug=True)
