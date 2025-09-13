from src.io import load_csv, save_csv
from src.cleaning import clean_data

def main():
    df = load_csv('./data/training.csv')
    print(df)
    clean_df, report = clean_data(df)
    print(clean_df)
    print(report)

if __name__ == "__main__":
    main()