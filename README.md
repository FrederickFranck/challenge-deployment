# Immo Eliza Deployment App

# Description

This is a web app that implements a machine learning model that can predict house prices on the belgian market based on given parameters.

The model used is a Gradient boosting Regression model & was trained with data scraped from [Immoweb](https://www.immoweb.be).

There is a website and an api availble.

# Usage

Website : https://immo-eliza-app.herokuapp.com/

API : https://immo-eliza-app.herokuapp.com/api


The API has one function call [/predict](https://immo-eliza-app.herokuapp.com/api/predict) 

which expects a JSON body according to following schema

```json
{   
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "https://frederickfranck.info/shemas/input.json",
    "title": "API INPUT",
    "description": "Input for https://immo-eliza-app.herokuapp.com/api/predict POST requests",

    "type":"object",
    "properties":{

        "area":{
            "description": "area of the house",
            "type":"integer",
            "minimum": 0
        },
        
        "property-type":{
            "description": "Type of property : ['House','Apartment']",
            "type":"string"
        },

        "rooms-number":{
            "description": "The amount of rooms",
            "type":"integer",
            "minimum": 0
        },

        "zip-code":{
            "description": "Postcode of the property",
            "type":"string"
        },

        "land-area":{
            "description": "Total area of the property (Optional)",
            "type":"integer"
        },

        "garden":{
            "description": "Does the property have a garden (Optional)",
            "type":"boolean"
        },

        "garden-area":{
            "description": "Area of the garden (Optional)",
            "type":"integer",
            "minimum": 0
        },

        "equipped-kitchen":{
            "description": "Does the property have a fully equipped kitchen (Optional)",
            "type":"boolean"
        },

        "swimming-pool":{
            "description": "Does the property have a pool (Optional)",
            "type":"boolean"
        },

        "furnished":{
            "description": "Is the propety furnished (Optional)",
            "type":"boolean"
        },

        "open-fire":{
            "description": "Does the property have an open fire (Optional)",
            "type":"boolean"
        },

        "terrace":{
            "description": "Does the property have a terrace (Optional)",
            "type":"boolean"
        },

        "terrace-area":{
            "description": "Area of the terrace (Optional)",
            "type":"integer",
            "minimum": 0
        },

        "facades-number":{
            "description": "Amount of facades of the property (Optional)",
            "type":"integer",
            "minimum": 0
        },

        "building-state":{
            "description": "Current state of the building (Optional)",
            "type":"string"
        }       
    },
    "required": ["area","property-type","rooms-number","zip-code"]
}
```

Returns a simple response containing the predicted price e.g.

```
Predicted price is € 506,465
```


# Installation

## Required packages

[Flask](https://flask.palletsprojects.com/en/2.1.x/)

[flask_expects_json](https://github.com/fischerfredl/flask-expects-json)

[joblib](https://joblib.readthedocs.io/en/latest/)

[numpy](https://numpy.org/)

[pandas](https://pandas.pydata.org/)

[scikit_learn](https://scikit-learn.org/stable/)

check [requirments.txt](/project/requirements.txt) for versions

# Usage

The main application is a flask app which can be either run locally or in a docker container

### local 
```bash
$ python app.py
```

### Docker

Build the image
```bash     
$ docker build . -t immo-deploy
```

Run a container with the created image
```bash
$ docker run -d -p 5000:5000 immo-deploy
```

Afterwards the app should be running at http://localhost:5000/