import numpy as np, pandas as pd
'''
Engineering additional features to produce more meaningful data
'''

# adds cyclical features for day of week and day of year to capture and help models understand periodic data
def add_cyclical_features(df):
    out = df.copy()
    d = out["date"]

    # day of week (7 day cycle)
    dow = d.dt.weekday.astype(float) # day of week represented as float
    out["dow_sin"] = np.sin((2 * np.pi * dow) / 7.0).astype("float32") # y-coordinate on circle
    out["dow_cos"] = np.cos((2 * np.pi * dow) / 7.0).astype("float32") # x-coordinate on circle

    # day of year (~365 day cycle)
    doy = d.dt.dayofyear.astype(float) # day of year represented as float
    denom = np.where(d.dt.is_leap_year, 366.0, 365.0) # adds leap-year precision
    out["doy_sin"] = np.sin((2 * np.pi * (doy - 1.0)) / denom).astype("float32") # (doy - 1) so Jan 1st is angle 0
    out["doy_cos"] = np.cos((2 * np.pi * (doy - 1.0)) / denom).astype("float32")

    return out

# bringing all feature engineering methods together
def add_all_features(df):
    df = add_cyclical_features(df)
    return df