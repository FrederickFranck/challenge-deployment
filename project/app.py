import os
from flask_expects_json import expects_json
from flask import Flask, request, render_template
from joblib import load

from preprocessing.cleaning_data import add_postcodes, clean_data , preprocess
from preprocessing.schema import schema
from model.model import create_model
from predict.prediction import predict


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))
RAW_DATA = os.path.join(ROOT_DIR,'data','Immoweb_Data_Scraper.csv')
POSTC_DATA = os.path.join(ROOT_DIR,'data','zipcode-belgium.csv')
CLEAN_DATA = os.path.join(ROOT_DIR,'data','Immoweb_Data_Clean.csv')
MODEL_DIR = os.path.join(ROOT_DIR,'model','GBR.joblib')


MODEL = 0
if (MODEL):
#Clean data & build the model
    clean_data(RAW_DATA, CLEAN_DATA)
    add_postcodes(CLEAN_DATA, POSTC_DATA)
    create_model(CLEAN_DATA, MODEL_DIR)

model = load(MODEL_DIR)

#Create app & routes
app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


@app.route("/api", methods=['GET'])
def route_api():
    
    return "I am alive !"

@app.route("/api/predict", methods=['GET','POST'])
@expects_json(schema, ignore_for=['GET'])
def route_api_predict():
    
    if request.method == 'GET':
        return schema
    
    if request.method == 'POST':
        json = request.json
        print(json)
        df = preprocess(json)
        print(df)   
        
        value = round(predict(model,df))
        return f"Predicted price is € {value:,}"  


@app.route("/predict", methods=['GET','POST'])
def route_predict(data=None):
    
    if request.method == 'GET':   
        return render_template('predict.html')
    
    if request.method == 'POST':
        print(data)
        #json = request.json
        df = preprocess(data)
        print(df)   
        
        value = round(predict(model,df))
        return render_template('predict.html', price=value) 

@app.route("/predict/jsonify", methods=['POST'])
def route_jsonify():
    form = request.form.to_dict(flat=True)
    
    #Check boolean values
    keys = ["garden","equipped-kitchen","swimming-pool","furnished","open-fire","terrace"]
    for key in keys:
        if key in form:
            form[key] = True
        else:
            form[key] = False
    
    #Check integer values
    keys = ["area","rooms-number","facades-number","land-area","garden-area","terrace-area"]
    for key in keys:
        form[key] = int(form[key])

    return route_predict(form)


if __name__ == '__main__':
    # You want to put the value of the env variable PORT if it exist (some services only open specifiques ports)
    port = int(os.environ.get('PORT', 5000))
    # Threaded option to enable multiple instances for
    # multiple user access support
    # You will also define the host to "0.0.0.0" because localhost will only be reachable from inside de server.
    app.run(host="0.0.0.0", threaded=True, port=port,debug=True)
