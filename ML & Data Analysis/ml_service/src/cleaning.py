import pandas as pd, hashlib, datetime as dt, numpy as np
'''
Data pre-processing & cleaning
'''

# data normalisation to adhere to naming conventions
def normalise_headers(df):
    out = df.copy() # returning new dataframes avoids input mutation
    out.columns = [col.strip().lower().replace(" ", "_") for col in out.columns]
    return out

# cleanup of string-based columns, improving standardisation
def standardise_strings(df):
    out = df.copy()
    for col in ["internal_events", "external_events", "holiday"]:
        if col in out:
            out[col] = out[col].fillna("").astype(str).str.strip() # fills null values with space and removes leading/trailing spaces
    return out

# parsing dates to datetime objects
def parse_dates(df):
    out = df.copy()
    out["date"] = pd.to_datetime(out["date"], errors="raise") # coverts and raises any exceptions encountered, fails fast
    return out

# ensures necessary columns are numerical in type and erronous data is surfaced
def coerce_numeric(df):
    out = df.copy()
    for col in ["sales", "covers"]:
        str_col = out[col].astype(str).str.strip()
        str_col = str_col.str.replace("£,", "", regex=True)
        out[col] = pd.to_numeric(str, errors="coerce") # converts back to numeric, erronous values are nulled
    return out

# handles missing values according to column
def handle_missing(df):
    out = df.copy()
    out["weather"] = (out["weather"].astype("string").str.strip().str.lower().fillna("cloudy")) # fill null weather with 'cloudy' and normalises non-null values

    out["dow"] = out["date"].dt.weekday # adds day-of-week feature for day-specific apc

    valid = out["sales"].notna() & out["covers"].notna & (out["covers"] > 0)
    apc_global = (out.loc[valid, "sales"] / out.loc[valid, "covers"]).median() # median avg £ per cover for fallback use
    apc_dow = ( # median avg £ per cover for each day of the week
        (out.loc[valid, "sales"] / out.loc[valid, "covers"])
        .groupby(out.loc[valid, "dow"])
        .median()
    )

    m_sales = out["covers"].notna() & out["sales"].isna() # missing sales values with present covers values
    m_cov = out["covers"].isna() & out["sales"].notna() # missing cover values with present sales values
    m_both = out["covers"].isna() & out["sales"].isna() # missing sales & covers

    # impute sales (sales = covers * apc)
    if m_sales.any():
        apc = (out.loc[m_sales, "dow"].map(apc_dow)).fillna(apc_global) # maps imputable sales rows through day-specific apc using apc_global as fallback
        out.loc[m_sales, "sales"] = (out.loc[m_sales, "covers"] * apc).round(0)
    
    # impute covers (covers = sales / apc)
    if m_cov.any():
        apc = (out.loc[m_cov, "dow"].map(apc_dow)).fillna(apc_global) # maps imputable covers rows through day-specific apc using apc_global as fallback
        out.loc[m_sales, "covers"] = (out.loc[m_sales, "sales"] / apc).round().clip(lower=0)  

    out = out.loc[~m_both].reset_index(drop=True) # drops rows with no present sales or covers

    summary = { # summry report of imput & drop sums
        "datast cleaned: "
        "imputed_sales_rows": int(m_sales.sum()),
        "imputed_covers_rows": int(m_cov.sum()),
        "dropped_rows_both_missing": int(m_both.sum()),
        "apc_global": float(apc_global),
    }     

    return out, summary

# drop all duplicate dates
def handle_duplicates(df):
    out = df.drop_duplicates(subset=["date"]).copy() # uses subset to treat rows with the same dates as duplicates
    return out

def handle_outliers(df):
    out = df.copy()
    
    return

def clean_data(df):
    return(df
           .pipe(normalise_headers)
           .pipe(standardise_strings)
           .pipe(parse_dates)
           .pipe(coerce_numeric)
           .pipe(handle_missing)
           .pipe(handle_duplicates)
           .pipe(handle_outliers))