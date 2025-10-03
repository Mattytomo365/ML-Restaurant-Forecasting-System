import numpy as np, pandas as pd
'''
Orchestrates ml model training using splitted preprocessed data
'''

exclude = {"date","sales","covers","weather","internal_events","external_events","holiday"}

# chooses appropriate model input features
def training_cols(df):
    return [c for c in df.columns if c not in exclude]

# forms time-aware train/test split on dataset
def time_split(df):
    cutoff = df["date"].max() - pd.Timedelta(days=56) # splitting date
    train = df[df["date"] <= cutoff].reset_index(drop=True)
    test = df[df["date"] > cutoff].reset_index(drop=True)
    return train, test

def train_model():
    return

def save_model(): # Writes model artifact .joblib (Binary model artifact used for inference)
    return