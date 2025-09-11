from src.io import load_csv, save_csv
from src.cleaning import clean_data

def main():
    df = load_csv('./data/training.csv')
    print(df)
    clean_df = clean_data
    print(clean_df)

if __name__ == "__main__":
    main()