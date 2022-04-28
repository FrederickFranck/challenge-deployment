import pandas as pd
import numpy as np
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

RAW_DATA = os.path.join(ROOT_DIR,'data','Immoweb_Data_Scraper.csv')
POSTC_DATA = os.path.join(ROOT_DIR,'data','zipcode-belgium.csv')
CLEAN_DATA = os.path.join(ROOT_DIR,'data','Immoweb_Data_Clean.csv')

#Clean scrapped data
def clean_data(raw_filename, clean_filename):
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
def add_postcodes(clean_filename,postc_filename):
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
    df.reset_index(drop=True,inplace=True)
    
    #Save data
    df.to_csv(clean_filename,index_label=False)


def preprocess(input_data):
    #TODO
    return

clean_data(RAW_DATA, CLEAN_DATA)
add_postcodes(CLEAN_DATA, POSTC_DATA)
