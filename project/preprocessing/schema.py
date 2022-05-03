schema = {
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