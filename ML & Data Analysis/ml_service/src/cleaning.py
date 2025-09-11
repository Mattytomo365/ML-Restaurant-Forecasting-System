import pandas as pd, hashlib, datetime as dt
'''
Data pre-processing & cleaning
'''

required_cols = ["date","sales","covers","weather","internal_events","external_events","holiday"]
string_cols = ["weather","internal_events","external_events","holiday"]

# data normalisation to adhere to naming conventions
def normalise_headers(df):
    out = df.copy() # returning new dataframes avoids input mutation
    out.columns = [c.strip().lower().replace(" ", "_") for c in out.columns]
    return out

# cleanup of string-based columns, improving standardisation
def standardise_strings(df):
    out = df.copy()
    for c in string_cols:
        if c in out:
            out[c] = out[c].fillna("").astype(str).str.strip() # does this remove spaces too???
    return out

# parsing dates to datetime objects
def parse_dates(df):
    out = df.copy()
    out["date"] = pd.to_datetime(out["date"], errors="raise")
    return out

def clean_data(df):
    return(df
           .pipe(normalise_headers)
           .pipe(standardise_strings)
           .pipe(parse_dates))