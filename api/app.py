from flask import Flask, jsonify, request
from flask_cors import CORS
from pre_process_data import PreprocessData

app = Flask(__name__)
CORS(app)

preprocessor = PreprocessData()


@app.route("/")
def index():
    return jsonify(message="Hello from Flask!")


@app.route("/emissionsAndLandData")
def emissions_and_land_data():
    country = request.args.get("country", "World")
    return preprocessor.emissionsAndLand(country)


@app.route("/emissionAndCerealYieldData")
def emission_and_cereal_yield_data():
    country = request.args.get("country", "World")
    return preprocessor.emissionAndCerealYield(country)


@app.route("/populationAndArableLand")
def population_and_arable_land():
    country = request.args.get("country", "World")
    return preprocessor.populationAndArableLand(country)


if __name__ == "__main__":
    app.run(debug=True)
