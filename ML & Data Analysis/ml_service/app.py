from flask import Blueprint, request, jsonify
import pandas as pd
from dataset import load_csv       
from analysis import eda
'''
Flask web service
'''

# HTTP GET
@app.get("/models")
def models_list():
    return

# monthly averages for chosen metric, used in frontend for user-facing visualisations
@app.get("/analytics/monthly-avg")
def monthly_avg(): # call twice from angular code to get both sales and covers
    metric = request.args.get("metric", "sales") # reads metric from query param or defaults to "sales"
    df = load_csv("data/df_feature.csv") 
    out = eda.monthly_avg(df, metric)
    return jsonify(out.to_dict(orient="records")) # returns list of row dictionaries

# weekday averages for specified month and metric, used in frontend for user-facing visualisations
@app.get("/analytics/weekday-avg")
def weekday_avg():
    metric = request.args.get("metric", "sales")
    month = int(request.args.get("month"))
    df = load_csv("data/df_feature.csv") # change with name of dataset!
    out = eda.weekday_avg(df, month, metric)
    return jsonify({"month": month, "label": eda.month_labels.get(month, str(month)), # adds month and label properties on top-level rather than for every column in dataset like monthly_avg
                    "data": out.to_dict(orient="records")})

# HTTP POST
@app.post("/models/activate")
def models_activate():
    return

@app.post("/train")
def train():
    return

@app.post("/forecast")
def forecast():
    return