import numpy as np, pandas as pd
from model_factory import make_estimator
from metrics import metrics
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

# model trained using previously split data and evaluated against test data
def train_model(df, kind, target="sales"):
    features = training_cols(df)
    train, test = time_split(df)

    X_train, Y_train = train[features].values, train[target].values # used to fit model
    X_test, Y_test = test[features].values, test[target].values # establishes unseen data to evaluate model against and forecasting variables for predictions

    estimator = make_estimator(kind) # uses model factory to produce estimator for algorithm specified
    estimator.fit(X_train, Y_train)
    pred = estimator.predict(X_test) # rest of dataset utilised to predict Y_test

    metrics = metrics(Y_test, pred, kind, target)
    return estimator, features, metrics

def save_model(): # Writes model artifact .joblib (Binary model artifact used for inference)
    return