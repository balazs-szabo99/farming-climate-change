from flask import Flask, jsonify, request
from flask_cors import CORS
from pre_process_data import PreprocessData

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return jsonify(message="Hello from Flask!")


@app.route("/landing")
def landing():
    country = request.args.get("country")
    preprocessor = PreprocessData()
    emissionsAndLandData = preprocessor.emissionsAndLand(country)
    emissionAndCerealYieldData = preprocessor.emissionAndCerealYield(country)
    populationAndArableLand = preprocessor.populationAndArableLand(country)

    return [emissionsAndLandData, emissionAndCerealYieldData, populationAndArableLand]


if __name__ == "__main__":
    app.run(debug=True)
