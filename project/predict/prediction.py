from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd

# Returns prediction from model based on input
def predict(model: GradientBoostingRegressor, _input: pd.DataFrame) -> int:
    prediction = model.predict(_input)
    return prediction[0]
