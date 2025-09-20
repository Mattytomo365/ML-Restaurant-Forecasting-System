import pandas as pd
from src.io import load_csv, save_csv
from src.cleaning import clean_data
from src.encoding import fit_onehot_schema, save_onehot_schema, load_onehot_schema, apply_onehot_schema

def main():

    # data cleaning
    df = load_csv('./data/training.csv')
    print(df)
    df_clean, report = clean_data(df)
    print(df_clean)
    print(report)

    # data encoding
    schema = fit_onehot_schema(df_clean)
    save_onehot_schema(schema, "models/onehot_schema.json")

    df_onehot = apply_onehot_schema(df_clean, schema, drop_original=False)
    print(df_onehot)
    df_onehot.to_csv("data/df_onehot.csv")
    

if __name__ == "__main__":
    main()