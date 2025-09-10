import pandas as pd, hashlib, datetime as dt

'''
Loading raw data & saving to csv
'''

def load_csv(path: str):
    df = pd.read_csv(path)
    return df

def save_csv(df, path:str):
    df = save_csv(path, index=False)