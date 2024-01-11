from flask import Flask, jsonify
from flask_cors import CORS

from pre_process_data import PreprocessData

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return jsonify(message="Hello from Flask!")


@app.route("/landing")
def landing():
    emissionsAndLandData = PreprocessData.emissionsAndLand()
    return emissionsAndLandData


if __name__ == "__main__":
    app.run(debug=True)
