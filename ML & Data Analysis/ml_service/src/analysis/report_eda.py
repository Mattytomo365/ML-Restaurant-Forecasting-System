import os, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from src.dataset import load_csv
'''
Data visualisations supporting points raised in report
'''
# generates DOW/DOY unit-circle plots
def cyclical_plots(df, x_col, y_col, title):
    fig, ax = plt.subplots()
    df.plot.scatter(x=x_col, y=y_col, ax=ax)
    ax.set_aspect("equal", adjustable="box") # creates circle
    t = np.linspace(0, 2*np.pi, 512)
    ax.plot(np.cos(t), np.sin(t), linewidth=1) # unit circle line
    if title:
        ax.set_title(title)
    # group and highlight weekday/monthly means?
    return ax

def plot_all(df):
    cyclical_plots(df, "dow_cos", "dow_sin", "Cyclical day-of-week scatter plot")
    cyclical_plots(df, "dow_cos", "dow_sin", "Cyclical day-of-year scatter plot")
    plt.show()


if __name__ == "__main__":
    df = load_csv("../data/df_feature.csv")
    plot_all(df)