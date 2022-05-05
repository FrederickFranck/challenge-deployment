import pandas as pd
df = pd.Dataframe
#Remove castles
df = df.drop(df[df['sub_type']  == 'castle'].index)

#Drop price outliers
df = df.drop(df[df['price'] > 8000000].index)

#Drop rooms outliers
df = df.drop(df[df['amount_of_rooms'] > 60].index)

#Drop area outliers
df = df.drop(df[df['area'] > 4000].index)
#Drop garden area outliers
df = df.drop(df[df['garden_area'] > 60000].index)
#Drop total land area outliers
df = df.drop(df[df['land_area'] > 300000].index)
