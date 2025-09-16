import re
import json
from pathlib import Path
import pandas as pd
from pandas.api.types import CategoricalDtype
'''
Multi-label and singular one-hot encoding for string based fields
'''

# standardises category names, allowing for safe onehot column suffixes
# def standardise_categories(c):
#     c = str(c).strip().lower()
#     c = re.sub(r"[^a-z0-9]+", "_", c).strip("_")
#     return c or "unknown"

# adds one-hot cols for a specified col with a fixed category list
def onehot_single(df, col, categories:list[str]):
    cat = CategoricalDtype(categories=categories, ordered=False) # allows for casts to categorial dtype to filter out categories not in list
    col_norm = df[col].fillna("unknown").astype(cat) # temporary placeholders for NaN values
    dummies = pd.get_dummies(col_norm, prefix=col, prefix_sep="__", dtype="int32") # onehot matrix (0/1 values)
    expected_cols = [f"{col}__{c}" for c in categories] # precomputes & normalises expected onehots
    dummies = dummies.reindex(columns=expected_cols, fill_value=0) # adds missing onehots filled with 0 from precomputed list
    return dummies

# multi-label onehot from a tag column
def onehot_multi(df, col, categories:list[str], sep=";"):
    base = pd.DataFrame(index=df.index)
    s = df[col]
    for c in categories:
        mask = s.str.contains(rf"(^|{re.escape(sep)})\s*{re.escape(c)}\s*($|{re.escape(sep)})") # builds regex matching a category as a whole token
        base[f"{col}__{c}"] = mask.astype("int32") # converts boolean mask to 0/1 and adds as a column
    return base


