import os, numpy as np, pandas as pd, datetime as dt
import matplotlib.pyplot as plt
'''
User-facing eda on historical data to uncover trends and patterns
'''

dow_order = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
month_labels = {i: pd.Timestamp(2024, i, 1).strftime("%b") for i in range(1,13)} # month labels based off dates within dataset

# mean metric per calendar month
def monthly_avg(df, metric):
    d = df["date"]
    month_m = (df.groupby(d.dt.month)[metric].agg(value="mean", n_days="count") # aggregating groups to compute mean and n_days 
               .reindex(1, 13).fillna({"value": 0, "n_days": 0})) # maintains clean fixed order with no missing months

    # additional columns for user interface refinement
    month_m["label"] = month_m["month"].map(month_labels) # labelling to remove numerics
    month_m["value"] = month_m["value"].astype(float).round(2) # rounding
    month_m["n_days"] = month_m["n_days"].astype(int)
    return month_m[["month", "label", "value", "n_days"]]

# mean metric by weekday for a specified month
def weekday_avg(df, month, metric):
    d = df["date"]
    m = df["date"].month.eq(int(month)) # locates month within dataset
    # fallback
    if not m.any():
        return pd.DataFrame({"dow": dow_order, "value": [0]*7}) # => [0, 0, 0, 0, 0, 0, 0]
    dow = d.dt.day_name().str[:3]
    day_m = (df.loc[m].groupby(dow)[metric].mean()
             .reindex(dow_order).fillna(0.0) # maintains fixed order with no missing days
             .reset_index().rename(columns={"index": "dow", metric: "value"})) # consistent column names
    day_m["value"] = day_m["value"].astype(float).round(2) # rounding for user interface
    return day_m[["dow", "value"]]


def uplift(df):
    return