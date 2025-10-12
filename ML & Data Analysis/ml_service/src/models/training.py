from pathlib import Path
from model_factory import make_estimator, feature_cols, grid_search
from evaluation import calculate_metrics
from registry import save_manifest
import json, joblib, time
import numpy as np, pandas as pd
'''
Orchestrates ml model training, tuning, testing, and saving using preprocessed data
'''
# forms train and test datasets using time-aware split
def time_split(df, days=56):
    if df is None or len(df) == 0: # enforcing datetime
        raise ValueError("Empty dataframe provided to time_split")
    cutoff = df["date"].max() - pd.Timedelta(days=56) # splitting date
    train = df[df["date"] <= cutoff].reset_index(drop=True)
    test = df[df["date"] > cutoff].reset_index(drop=True)
    return train, test

# model trained using previously split data and evaluated against test data
def train_model(df, kind, param_grid, target="sales"):
    features = feature_cols(df)
    if len(features) == 0: # feature validation
        raise ValueError("No training features found after applying exclude set")
    train, test = time_split(df)

    builder = lambda params: make_estimator(kind, params) # uses model factory 
    best = grid_search(train, target, param_grid=param_grid, builder=builder) # determines best hyper-parameter combination
    
    model = builder(best["params"]) # accesses "param" element within "best" dictionary
    X_train, y_train = train[features].to_numpy, train[target].to_numpy # feature matrix and target vector
    X_test, y_test = test[features].to_numpy(), test[target].to_numpy() # unseen testing data
    model.fit(X_train, y_train) # using whole training dataset - no train/test masks required
    preds = model.predict(X_test)

    metrics = calculate_metrics(y_test, preds, kind) # evaluates tuned model performance
    return model, features, best["params"], metrics

# Writes model artifact .joblib (Binary model artifact used for inference) and saves manifest (model metadata)
def save_model(model, target, features, best_params, metrics): 
    t = time.strftime("%Y%m%d-%H%M%S") # time snapshot for model id
    model_id = f"{metrics["kind"]}_{t}"
    out = Path("models") / model_id # model artifact path
    out.mkdir(parents=True, exist_ok=True) # validate path
    joblib.dump({"estimator": model, "features": features}, out / "model.joblib") # saves model artifact
    manifest = save_manifest(model_id, target, features, best_params, metrics, t, out) # saves model manifest
    return str(out)