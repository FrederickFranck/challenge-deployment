import os
from model.model import create_model
from preprocessing.cleaning_data import add_postcodes, clean_data

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))

RAW_DATA = os.path.join(ROOT_DIR,'data','Immoweb_Data_Scraper.csv')
POSTC_DATA = os.path.join(ROOT_DIR,'data','zipcode-belgium.csv')
CLEAN_DATA = os.path.join(ROOT_DIR,'data','Immoweb_Data_Clean.csv')
MODEL_DIR = os.path.join(ROOT_DIR,'model','GBR.joblib')


clean_data(RAW_DATA, CLEAN_DATA)
add_postcodes(CLEAN_DATA, POSTC_DATA)
create_model(CLEAN_DATA, MODEL_DIR)