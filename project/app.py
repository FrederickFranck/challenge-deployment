import os
from model.model import create_model
from preprocessing.cleaning_data import add_postcodes, clean_data
from flask import Flask,request
from joblib import load

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))
RAW_DATA = os.path.join(ROOT_DIR,'data','Immoweb_Data_Scraper.csv')
POSTC_DATA = os.path.join(ROOT_DIR,'data','zipcode-belgium.csv')
CLEAN_DATA = os.path.join(ROOT_DIR,'data','Immoweb_Data_Clean.csv')
MODEL_DIR = os.path.join(ROOT_DIR,'model','GBR.joblib')

#Clean data & build the model
clean_data(RAW_DATA, CLEAN_DATA)
add_postcodes(CLEAN_DATA, POSTC_DATA)
create_model(CLEAN_DATA, MODEL_DIR)

model = load(MODEL_DIR)

#Create app & routes
app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "I am alive"

@app.route("/predict", methods=['GET','POST'])
def route_predict():
    
    if request.method == 'GET':
        return 'get'
    
    if request.method == 'POST':
        return 'post'


if __name__ == '__main__':
    # You want to put the value of the env variable PORT if it exist (some services only open specifiques ports)
    port = int(os.environ.get('PORT', 5000))
    # Threaded option to enable multiple instances for
    # multiple user access support
    # You will also define the host to "0.0.0.0" because localhost will only be reachable from inside de server.
    app.run(host="0.0.0.0", threaded=True, port=port)
