import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from joblib import dump


def create_model(data_dir, model_dir):

    #Import data
    df = pd.read_csv(data_dir)

    #Creature Features & target
    features = [
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
    'region']

    X = df[features]
    y = df['price']

    #Create test & training data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    #From testing gradientbooster gave us the best results
    reg = GradientBoostingRegressor(n_estimators=200,max_depth=10)
    reg.fit(X_train, y_train)
    _score = reg.score(X_test, y_test)

    #output model score
    print(f"Model Created with score {_score}")
    
    #Save model to file
    dump(reg, model_dir)