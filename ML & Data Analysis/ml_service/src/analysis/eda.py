import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from figures.save_figure import save_figure
'''
User-facing eda on historical data to uncover trends and patterns
'''

DOW_ORDER = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"] # set order
month_labels = {i: pd.Timestamp(2024, i, 1).strftime("%b") for i in range(1, 13)}


def _prepare_dates(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Ensure downstream analysis always receives datetimelike values.
    '''
    out = df.copy()
    out["date"] = pd.to_datetime(out["date"], dayfirst=True, errors="coerce")
    return out.loc[out["date"].notna()].copy()


def monthly_avg(df: pd.DataFrame, 
                metric: str) -> pd.DataFrame:
    '''
    Mean metric per calendar month
    '''
    df = _prepare_dates(df)
    d = df["date"]
    month = d.dt.to_period("M") # year-month keys for year-month grouping
    month_m = (df.groupby(month)[metric].agg(value="mean", n_days="count")
               .rename_axis("month")
               .reset_index())

    # additional labelling
    month_ts = month_m["month"].dt.to_timestamp()
    month_m["period"] = month_m["month"].astype(str)
    month_m["label"] = month_m["month"].dt.strftime("%b %Y")
    month_m["month"] = month_m["month"].dt.month.astype(int)
    month_m["value"] = month_m["value"].astype(float).round(2)
    month_m["n_days"] = month_m["n_days"].astype(int)

    fig, ax = plt.subplots()
    a = month_m["value"]

    ax.bar(month_ts, a, width=20, alpha=0.35, label="daily avg")
    ax.plot(month_ts, a, marker="o", linewidth=1.5, label="trend")

    ax.set_xlabel("month")
    ax.set_ylabel(f"average {metric}")
    ax.set_title(f"Average daily {metric} per month")
    ax.grid(True, which="major", linestyle=":", linewidth=0.8, alpha=0.7)
    monthly_labels(ax)
    save_figure(fig, f"monthly_average_{metric}", "eda_figures")

    return pd.DataFrame(month_m[["month", "period", "label", "value", "n_days"]])


def weekday_avg(df: pd.DataFrame, 
                month: str, 
                metric: str) -> pd.DataFrame:
    '''
    Mean metric by weekday for a specified month
    '''
    df = _prepare_dates(df)
    d = df["date"]
    m = d.dt.month.eq(int(month)) # locates month within dataset

    if not m.any(): # fallback
        return pd.DataFrame({"dow": DOW_ORDER, "value": [0]*7})
    
    dow = d.dt.day_name().str[:3] # day name abbreviation
    day_m = (df.loc[m].groupby(dow)[metric].agg(value="mean") # weekday-based average
            .reindex(DOW_ORDER).fillna(0.0) # maintain fixed order
            .rename_axis("dow")
            .reset_index()) 
    
    day_m["value"] = day_m["value"].astype(float).round(2)
    return pd.DataFrame(day_m[["dow", "value"]])


def weekday_avg_plot(weekday_averages: list[pd.DataFrame]) -> None:
    '''
    Visualisation of weekday averages across all months
    '''

    df = pd.concat(weekday_averages, ignore_index=True)

    fig, ax = plt.subplots()

    by_dow = df.groupby("dow")["value"].mean().reindex(DOW_ORDER)
    ax.bar(by_dow.index, by_dow.values, alpha=0.35, label="weekday avg")
    ax.plot(by_dow.index, by_dow.values, marker="o", linewidth=1.5, label="trend")
    ax.set_xlabel("weekday")
    ax.set_ylabel("average sales")
    ax.set_title("Average weekday sales across all months")
    ax.grid(True, which="major", linestyle=":", linewidth=0.8, alpha=0.7)
    save_figure(fig, "weekday_average_total", "eda_figures")


def monthly_labels(ax) -> None:
    '''
    Helper function to improve visibility of values on x-axis
    '''
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.figure.autofmt_xdate()

# compute uplift of specified factors against specified metric
def uplift(df: pd.DataFrame,
            factor: str, 
            month: str, 
            metric: str, 
            sep=";") -> pd.DataFrame:
    df = _prepare_dates(df)
    d = df["date"]
    m = d.dt.month.eq(int(month))

    if not m.any(): # fallback
        return pd.DataFrame(columns=["tag", "n_days", "avg", "uplift_tag"])
    
    sub = df.loc[m].copy()
    s = sub[factor].fillna("").astype(str).str.strip().str.lower() # forces robust strings

    tags_list = s.apply(lambda val: [tag.strip() for tag in val.split(sep) if tag.strip() and tag.strip() != "none"])
    base_mask = tags_list.str.len().eq(0) # baseline = days without events
    baseline = (sub.loc[base_mask])[metric].mean() # mean metric of days without events
    baseline_weather = float(df[metric].mean()) # baseline for entire metric

    # add helper columns 
    sub["tags"] = tags_list # attach tag if any

    # explode tags to individual rows
    sub = (sub.explode("tags").rename(columns={"tags": "tag"}))
    sub = sub[["date", "tag", metric]].drop_duplicates(subset=["date", "tag"])

    if factor == "weather":
        sub["baseline"] = baseline_weather

        # filter out rows with an invalid baseline
        sub = sub.loc[sub["baseline"].notna() & sub["baseline"].ne(0)]

        # fallback
        if sub.empty:
            return pd.DataFrame(columns=["tag", "n_days", "avg", "uplift_tag"])

    else:
        sub["baseline"] = baseline

        # filter out rows with no event or an invalid baseline
        sub = sub.loc[~base_mask & sub["baseline"].notna() & sub["baseline"].ne(0)]

        # fallback
        if sub.empty:
            return pd.DataFrame(columns=["tag", "n_days", "avg", "uplift_tag"])
        
    # calculate percentage uplift per row against baseline
    sub["uplift_row"] = 100.0 * (sub[metric] - sub["baseline"]) / sub["baseline"]

    # aggregate per tag - collapse daily rows into a few group-level numbers
    tab = (sub.groupby("tag")
        .agg(n_days=("date", "nunique") # unique days tag occurs
             , avg=(metric, "mean") # mean metric on tagged days
             , uplift_tag=("uplift_row", "mean")) # mean % uplift across occurrences
        .reset_index().sort_values("avg", ascending=False))
    
    return tab
    
        
            



    

