# Farming Climate Change Data API

## Overview
This API serves as the backend for the "Farming Climate Change Data Visualization" app. It provides access to essential climate change data and supports the interactive features of the application.

## Installation
1. Make sure you have Python installed on your machine.
2. Install dependencies:
```
pip install -r requirements.txt
```

## Activation
1. Ensure that the virtual environment is activated. That varies based on your Python setup.

## Running the API
1. Make sure you are in the `api` folder of the project.
2. Run the following command:
```
flask run
```
The API will be accessible at http://127.0.0.1:5000/ by default.

## API Endpoints
`/`
* Method: GET
* Description: Retrieve a simple welcome message.
* Example Response:
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
