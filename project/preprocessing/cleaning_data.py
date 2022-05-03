from ast import Str
from tokenize import String
from typing import Dict
import pandas as pd
import numpy as np

#Clean scrapped data
def clean_data(raw_filename : String, clean_filename: String) -> None:
    df = pd.read_csv(raw_filename, encoding='latin-1')
    cleandf = df.copy()
    
    #Remove houses with no area data
    cleandf = cleandf.dropna(subset=['area'])

    #Calculate land_area 
    cleandf['land_area'] = cleandf.apply(lambda x: x["area"] + x["surface_area_plot"],axis=1)
    
    def calculate_facades(x):
        #print(x.amount_of_facades)
        if np.isnan(x.amount_of_facades):
            if x.type == 'apartment':
                return 2
            if x.type == 'house':
                return 4 
        else:
            return x.amount_of_facades
        
    
    cleandf['amount_of_facades'] = cleandf.apply(lambda x: calculate_facades(x),axis=1)
    
    
    #Fill in NaN values 
    cleandf['building_state'] = cleandf['building_state'].fillna("unknown")
    
    #Drop unused columns
    cleandf = cleandf.drop(columns='terrace_area')
    cleandf = cleandf.drop(columns='surface_area_plot')
    cleandf = cleandf.drop(columns='surface_land')
    
    #Reset index 
    cleandf.reset_index(drop=True,inplace=True)
    
    #Save cleaned data
    cleandf.to_csv(clean_filename,index_label=False)
    

#Adds postcodes to cleaned data
def add_postcodes(clean_filename : String,postc_filename: String) -> None:
    df = pd.read_csv(clean_filename)
    z = pd.read_csv(postc_filename)
    
    #Get postcode where citynames are the same
    def getzip(x):
        try:
            return (z.loc[z['locality'] == (x.locality)]).values[0][0]
        except:
            return None

    #turn city names to lowercase before comparing
    df['locality'] = df.apply(lambda x: x.locality.lower(),axis=1)
    z['locality'] = z.apply(lambda x: x.locality.lower(),axis=1)

    #get postcodes
    df['postcode'] = df.apply(lambda x : getzip(x),axis=1)

    #Drop listings without postcodes
    df = df.dropna(subset=['postcode'])
    
    #Create "Regions"
    df['region'] = df.apply(lambda x: round(x.postcode/100),axis=1)

    #Reset index
    df.reset_index(drop=True,inplace=True)
    
    #Save data
    df.to_csv(clean_filename,index_label=False)


def preprocess(input_data: Dict) -> pd.DataFrame:
    
    #Create empty dataframe
    column_names = [
        'amount_of_rooms',
        'area',
        'has_full_kitchen',
        'is_furnished',
        'has_open_fire',
        'has_terrace',
        'has_garden',
        'garden_area',
        'amount_of_facades',
        'has_pool',
        'land_area',
        'region'
        ]
    
    df = pd.DataFrame(columns=column_names)
    
    #Read json into a list 
    
    #Required Parameters    
    amount_of_rooms = input_data["rooms-number"]
    area = input_data["area"]
    region = input_data["zip-code"]
    region = region[:2]
    
    #Optional parameters
    has_full_kitchen = False
    try:
        has_full_kitchen = input_data["equipped-kitchen"]
    except:
        pass
    
    is_furnished = False
    try:
        is_furnished = input_data["furnished"]
    except:
        pass
    
    has_open_fire = False
    try:
        has_open_fire = input_data["open-fire"]
    except:
        pass
    
    has_terrace = False
    try:
        has_terrace = input_data["terrace"]
    except:
        pass
    
    has_garden = False
    try:
        has_garden = input_data["garden"]
    except:
        pass
    
    garden_area = 0
    try:
        garden_area = input_data["garden-area"]
    except:
        pass
    
    amount_of_facades = 0
    try:
        amount_of_facades = input_data["facades-number"]
    except:
        pass
    
    has_pool = False
    try:
        has_pool = input_data["swimming-pool"]
    except:
        pass
    
    land_area = 0
    try:
        land_area = input_data["land-area"]
    except:
        pass

    #Append input data to dataframe
    
    df.loc[len(df)] = [
        amount_of_rooms,
        area,
        has_full_kitchen,
        is_furnished,
        has_open_fire,
        has_terrace,
        has_garden,
        garden_area,
        amount_of_facades,
        has_pool,
        land_area,
        region
        ]
    
    return df


