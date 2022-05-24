import os
from pathlib import Path

import numpy as np
import pandas as pd
from pandas import DataFrame

COLUMNS = ['id', 'neighbourhood_group_cleansed', 'property_type', 'room_type', 'latitude', 'longitude', 'accommodates', 'bathrooms', 'bedrooms', 'beds','amenities', 'price']

AMENITIES = ['TV', 'Internet', 'Air_conditioning', 'Kitchen', 'Heating','Wifi', 'Elevator', 'Breakfast']

def get_csv_file_path(dir: str) -> str:
    for element in os.listdir(dir_input):
        name, extension = os.path.splitext(element)
        if extension == ".csv":
            return dir / element
        raise Exception("Can't found any csv files in {}".format(dir))
    
# Get number of bathrooms from `bathrooms_text`
def num_bathroom_from_text(text):
    try:
        if isinstance(text, str):
            bath_num = text.split(" ")[0]
            return float(bath_num)
        else:
            return np.NaN
    except ValueError:
        return np.NaN

def loadInitialData(dir: str) -> DataFrame:
    FILEPATH_DATA = get_csv_file_path(dir)

    df_raw = pd.read_csv(FILEPATH_DATA)

    df_raw.drop(columns=['bathrooms'], inplace=True)

    df_raw['bathrooms'] = df_raw['bathrooms_text'].apply(num_bathroom_from_text)

    df = df_raw[COLUMNS].copy()

    df.rename(columns={'neighbourhood_group_cleansed': 'neighbourhood'}, inplace=True)
    return df

def preprocess_amenities_column(df: DataFrame) -> DataFrame:
    
    for amenity in AMENITIES:
        df[amenity] = df['amenities'].str.contains(amenity).astype(int)

    df.drop('amenities', axis=1, inplace=True)
    
    return df

def set_category_column(df: DataFrame) -> DataFrame:
    df['category'] = pd.cut(df['price'], bins=[10, 90, 180, 400, np.inf], labels=[0, 1, 2, 3])
    return df

def prepare_airbnb_data(dir_input: str, output_file_path: str) -> None:

    df = loadInitialData(dir_input)

    df = df.dropna(axis=0)

    df = preprocess_amenities_column(df)

    df = set_category_column(df)

    df.to_csv(output_file_path)
