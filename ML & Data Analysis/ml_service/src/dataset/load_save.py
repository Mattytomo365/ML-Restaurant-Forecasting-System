import pandas as pd

'''
Loading raw data & saving to csv
'''

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

    return df

def save_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)
