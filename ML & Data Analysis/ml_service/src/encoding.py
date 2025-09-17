import re
import json
from pathlib import Path
import pandas as pd
from pandas.api.types import CategoricalDtype
'''
Multi-label and singular one-hot encoding for string based fields
'''

# standardises category names, allowing for safe onehot column suffixes
def standardise_categories(c):
    c = str(c).strip().lower()
    c = re.sub(r"[^a-z0-9]+", "_", c).strip("_")
    return c or "unknown"

# adds one-hot cols for a specified col with a fixed category list
def onehot_single(df, col, categories:list[str]):
    category = CategoricalDtype(categories=categories, ordered=False) # allows for casts to categorial dtype to filter out categories not in list
    col_norm = df[col].fillna("unknown").astype(category) # temporary placeholders for NaN values
    dummies = pd.get_dummies(col_norm, prefix=col, prefix_sep="__", dtype="int32") # onehot matrix (0/1 values)
    expected_cols = [f"{col}__{standardise_categories(c)}" for c in categories] # precomputes & normalises expected onehots
    dummies = dummies.reindex(columns=expected_cols, fill_value=0) # adds missing onehots filled with 0 from precomputed list
    return dummies

# multi-label onehot from a tag column
def onehot_multi(df, col, categories:list[str], sep=";"):
    base = pd.DataFrame(index=df.index)
    s = df[col]
    for c in categories:
        mask = s.str.contains(rf"(^|{re.escape(sep)})\s*{re.escape(c)}\s*($|{re.escape(sep)})") # builds regex matching a category as a whole token
        base[f"{col}__{standardise_categories(c)}"] = mask.astype("int32") # converts boolean mask to 0/1 and adds as a column
    return base

# discover categories in historical dataset, returns schema to apply onehot
def fit_onehot(df, weather_col="weather", internal_col="internal_events", external_col="external_events", holiday_col="holiday", dow_col="day_of_week"):
    schema = {}

    # weather / internal events (single)
    for col, key in [(weather_col, "weather"), (internal_col, "internal_events")]:
        if col in df.columns:
            s = df[col]
            categories = s[s.ne("")].unique().tolist() # determines unqiue categories listed not empty
            schema[f"{key}"] = sorted(categories) # stable order for consistency
    
    # external events/ holiday (multi-label)
    for col, key in [(external_col, "external_events"), (holiday_col, "holiday")]:
        if col in df.columns:
            categories = set() # using set removes duplicates
            for val in df[col]:
                for category in [t.strip() for t in val.split(";") if t.strip()]: # separates into individual categories
                    categories.add(category)
            schema[f"{key}"] = sorted(categories)
    
    # day of week (single)
    if dow_col in df.columns:
        ordered = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        days_present = df[dow_col].str[:3] # abbreviate category names
        days = [d for d in ordered if d in set(days_present)] # avoids errenous data
        schema["day_of_week"] = days
    
    return schema

    



