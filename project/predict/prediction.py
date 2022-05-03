from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd

def predict(model : GradientBoostingRegressor, _input : pd.DataFrame ) -> int:
    prediction = model.predict(_input)
    return prediction[0]