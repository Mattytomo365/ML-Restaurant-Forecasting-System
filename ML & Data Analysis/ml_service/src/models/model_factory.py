from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
'''
A factory returning the right estimator for a specified ML algorithm
'''
def make_estimator(type):
    # Random Forest
    if type == "rf":
         return RandomForestRegressor(n_estimators=400, max_depth=None, random_state=42, n_job=-1) # enough trees to stabalise without increasing process time (n_estimators), uses all cores (n_job)
    # XGBoost
    if type == "xgb":
         return XGBRegressor(n_estimators=600, max_depth=6, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1)
    # pipelines used with linear models to fit StandardScaler (scales data) before fitting the estimator
    # plain Linear Regression (OLS)
    if type == "linear":
         return make_pipeline(StandardScaler(with_mean=True, with_std=True), LinearRegression()) # standard z-score scaling
    # Ridge
    if type == "ridge":
         return make_pipeline(StandardScaler(), Ridge(alpha=1.0, random_state=42)) # sets higher penality strength (alpha) for more bias and less variance
    return