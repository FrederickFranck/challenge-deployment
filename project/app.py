import os
from flask_expects_json import expects_json
from flask import Flask, request, render_template
from joblib import load

# Local files
from preprocessing.cleaning_data import add_postcodes, clean_data, preprocess
from preprocessing.schema import schema
from model.model import create_model
from predict.prediction import predict

# Declare Pathnames
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))
RAW_DATA = os.path.join(ROOT_DIR, "data", "Immoweb_Data_Scraper.csv")
POSTC_DATA = os.path.join(ROOT_DIR, "data", "zipcode-belgium.csv")
CLEAN_DATA = os.path.join(ROOT_DIR, "data", "Immoweb_Data_Clean.csv")
MODEL_DIR = os.path.join(ROOT_DIR, "model", "GBR.joblib")


# Build model
# Set this to 1 if you want to rebuild the model on startup
BUILD_MODEL = 0
if BUILD_MODEL:
    # Clean data & build the model
    clean_data(RAW_DATA, CLEAN_DATA)
    add_postcodes(CLEAN_DATA, POSTC_DATA)
    create_model(CLEAN_DATA, MODEL_DIR)

# Load model
model = load(MODEL_DIR)

# Create app & routes
app = Flask(__name__)

# Default API route
@app.route("/api", methods=["GET"])
def route_api():
    return "Still Alive !"


# Predict API route
# GET returns the json schema which is accepted by POST
# POST returns predicted value , needs a json body which conforms with the schema
@app.route("/api/predict", methods=["GET", "POST"])
@expects_json(schema, ignore_for=["GET"])
def route_api_predict():

    if request.method == "GET":
        return schema

    if request.method == "POST":
        json = request.json
        df = preprocess(json)
        value = round(predict(model, df))
        return f"Predicted price is € {value:,}"


# Default route
# Returns welcome page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# Predict Route
# Returns HTML form which can be used as input for model predictions
@app.route("/predict", methods=["GET", "POST"])
def route_predict(data=None):

    if request.method == "GET":
        return render_template("predict.html")

    if request.method == "POST":

        df = preprocess(data)
        value = round(predict(model, df))
        return render_template("predict.html", price=value)


# Internal route to turn form data into json
@app.route("/predict/jsonify", methods=["POST"])
def route_jsonify():

    # Turn form data into a dictionary
    form = request.form.to_dict(flat=True)

    # Check boolean values
    # Turn string or missing values into booleans
    keys = [
        "garden",
        "equipped-kitchen",
        "swimming-pool",
        "furnished",
        "open-fire",
        "terrace",
    ]
    for key in keys:
        if key in form:
            form[key] = True
        else:
            form[key] = False

    # Check integer values
    # Turn all values from string to int
    # If values are missing replace them by 0
    keys = [
        "area",
        "rooms-number",
        "facades-number",
        "land-area",
        "garden-area",
        "terrace-area",
    ]
    for key in keys:
        if key in form:
            try:
                form[key] = int(form[key])
            except ValueError:
                form[key] = 0
        else:
            form[key] = 0
                    
    if form['zip-code'] == '':
        form['zip-code'] = '0000'
            
    return route_predict(form)


if __name__ == "__main__":
    # You want to put the value of the env variable PORT if it exist (some services only open specifiques ports)
    port = int(os.environ.get("PORT", 5000))
    # Threaded option to enable multiple instances for
    # multiple user access support
    # You will also define the host to "0.0.0.0" because localhost will only be reachable from inside de server.
    app.run(host="0.0.0.0", threaded=True, port=port, debug=True)
