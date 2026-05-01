# ==========================================================
# models.py
# Final Production Version
# Revenue Forecasting / Benchmark / Rolling Forecast
# ==========================================================
"""
HƯỚNG DẪN SỬ DỤNG NHANH
==========================================================

1) Benchmark toàn bộ model:

result = run_all_models(
    df=df,
    feature_cols=features,
    target_col="revenue"
)

2) Chạy 1 model backtest:

val_result, model, metrics = run_single_model(
    model_name="CatBoost",
    df=df,
    feature_cols=features,
    target_col="revenue",
    params=best_params
)

3) Forecast direct:

future_df, model = run_final_forecast(
    model_name="CatBoost",
    df=df,
    feature_cols=features,
    target_col="revenue",
    params=best_params
)

4) Rolling monthly forecast:

future_df, model = run_rolling_forecast(
    model_name="CatBoost",
    df=df,
    feature_cols=features,
    target_col="revenue",
    params=best_params
)

5) Compare tuned boosting:

compare_boosting_models(
    df=df,
    feature_cols=features,
    target_col="revenue",
    params_dict={
        "CatBoost": cat_params,
        "XGBoost": xgb_params,
        "LightGBM": lgb_params
    }
)
"""

# ==========================================================
# IMPORTS
# ==========================================================
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
    r2_score
)

from sklearn.linear_model import LinearRegression

from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    HistGradientBoostingRegressor,
    AdaBoostRegressor
)

from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

SEED = 42


# ==========================================================
# HELPERS
# ==========================================================
def prepare_data(df, date_col="date"):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).reset_index(drop=True)
    return df


def evaluate_metrics(y_true, y_pred):
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "MAPE": mean_absolute_percentage_error(y_true, y_pred) * 100,
        "R-squared": r2_score(y_true, y_pred)
    }


def get_cat_idx(X, categorical_features=None):
    if not categorical_features:
        return None

    cols = []
    for c in categorical_features:
        if c in X.columns:
            cols.append(X.columns.get_loc(c))
    return cols


# ==========================================================
# MODEL FACTORY
# ==========================================================
def get_model(model_name, params=None):

    if params is None:
        params = {}

    # LINEAR
    if model_name == "LinearRegression":
        basic = {}
        basic.update(params)
        return LinearRegression(**basic)

    # TREE
    elif model_name == "DecisionTree":
        basic = {"random_state": SEED}
        basic.update(params)
        return DecisionTreeRegressor(**basic)

    elif model_name == "RandomForest":
        basic = {
            "n_estimators": 300,
            "random_state": SEED,
            "n_jobs": -1
        }
        basic.update(params)
        return RandomForestRegressor(**basic)

    elif model_name == "ExtraTrees":
        basic = {
            "n_estimators": 300,
            "random_state": SEED,
            "n_jobs": -1
        }
        basic.update(params)
        return ExtraTreesRegressor(**basic)

    # BOOSTING SKLEARN
    elif model_name == "HistGradientBoosting":
        basic = {
            "max_iter": 300,
            "random_state": SEED
        }
        basic.update(params)
        return HistGradientBoostingRegressor(**basic)

    elif model_name == "AdaBoost":
        basic = {
            "n_estimators": 300,
            "random_state": SEED
        }
        basic.update(params)
        return AdaBoostRegressor(**basic)

    # LIGHTGBM
    elif model_name == "LightGBM":
        basic = {
            "n_estimators": 500,
            "learning_rate": 0.05,
            "random_state": SEED,
            "n_jobs": -1,
            "verbose": -1
        }
        basic.update(params)
        return LGBMRegressor(**basic)

    # XGB
    elif model_name == "XGBoost":
        basic = {
            "n_estimators": 500,
            "learning_rate": 0.05,
            "random_state": SEED,
            "n_jobs": -1,
            "verbosity": 0,
            "objective": "reg:squarederror"
        }
        basic.update(params)
        return XGBRegressor(**basic)

    # CATBOOST
    elif model_name == "CatBoost":
        basic = {
            "iterations": 500,
            "learning_rate": 0.05,
            "random_seed": SEED,
            "verbose": 0,
            "allow_writing_files": False,
            "loss_function": "RMSE"
        }
        basic.update(params)
        return CatBoostRegressor(**basic)

    else:
        raise ValueError("Unknown model_name")


# ==========================================================
# BACKTEST
# ==========================================================
def run_single_model(
    model_name,
    df,
    feature_cols,
    target_col="revenue",
    params=None,
    categorical_features=None,
    test_year=2022,
    date_col="date"
):

    df = prepare_data(df, date_col)

    use_cols = [date_col, target_col] + feature_cols
    df = df[use_cols].dropna().reset_index(drop=True)

    train = df[df[date_col].dt.year < test_year].copy()
    test = df[df[date_col].dt.year == test_year].copy()

    X_train = train[feature_cols]
    y_train = train[target_col]

    X_test = test[feature_cols]
    y_test = test[target_col]

    model = get_model(model_name, params)

    if model_name == "CatBoost":
        cat_idx = get_cat_idx(X_train, categorical_features)
        model.fit(X_train, y_train, cat_features=cat_idx, verbose=0)
    else:
        model.fit(X_train, y_train)

    preds = model.predict(X_test)
    preds = np.maximum(preds, 0)

    result = test.copy()
    result["prediction"] = preds

    metrics = evaluate_metrics(y_test, preds)

    return result, model, metrics


# ==========================================================
# DIRECT FORECAST
# ==========================================================
def run_final_forecast(
    model_name,
    df,
    feature_cols,
    target_col="revenue",
    params=None,
    categorical_features=None,
    forecast_start="2023-01-01",
    date_col="date"
):

    df = prepare_data(df, date_col)

    train = df[df[date_col] < forecast_start].copy()
    future = df[df[date_col] >= forecast_start].copy()

    train = train.dropna(subset=[target_col])

    X_train = train[feature_cols]
    y_train = train[target_col]

    X_future = future[feature_cols]

    model = get_model(model_name, params)

    if model_name == "CatBoost":
        cat_idx = get_cat_idx(X_train, categorical_features)
        model.fit(X_train, y_train, cat_features=cat_idx, verbose=0)
    else:
        model.fit(X_train, y_train)

    preds = model.predict(X_future)
    preds = np.maximum(preds, 0)

    result = future.copy()
    result["prediction"] = preds

    mask = result[target_col].isna()
    result.loc[mask, target_col] = result.loc[mask, "prediction"]

    return result, model


# ==========================================================
# ROLLING MONTHLY FORECAST
# ==========================================================
def run_rolling_forecast(
    model_name,
    df,
    feature_cols,
    target_col="revenue",
    params=None,
    categorical_features=None,
    forecast_start="2023-01-01",
    date_col="date"
):

    df = prepare_data(df, date_col)
    work_df = df.copy()

    future_dates = work_df[
        work_df[date_col] >= forecast_start
    ][date_col].dt.to_period("M").unique()

    model = None

    for month in future_dates:

        month_mask = (
            work_df[date_col].dt.to_period("M") == month
        )

        predict_df = work_df[month_mask].copy()

        train_df = work_df[
            work_df[date_col] < predict_df[date_col].min()
        ].copy()

        train_df = train_df.dropna(subset=[target_col])

        X_train = train_df[feature_cols]
        y_train = train_df[target_col]

        X_pred = predict_df[feature_cols]

        model = get_model(model_name, params)

        if model_name == "CatBoost":
            cat_idx = get_cat_idx(X_train, categorical_features)
            model.fit(X_train, y_train, cat_features=cat_idx, verbose=0)
        else:
            model.fit(X_train, y_train)

        preds = model.predict(X_pred)
        preds = np.maximum(preds, 0)

        work_df.loc[month_mask, "prediction"] = preds

        nan_mask = month_mask & work_df[target_col].isna()
        work_df.loc[nan_mask, target_col] = work_df.loc[nan_mask, "prediction"]

    # Xóa cột "prediction"
    result = work_df.drop(columns=["prediction"]).copy()

    return result, model


# ==========================================================
# BENCHMARK ALL MODELS
# ==========================================================
def run_all_models(
    df,
    feature_cols,
    target_col="revenue",
    sort_by="RMSE"
):

    model_list = [
        "LinearRegression",
        "DecisionTree",
        "RandomForest",
        "ExtraTrees",
        "HistGradientBoosting",
        "AdaBoost",
        "LightGBM",
        "XGBoost",
        "CatBoost"
    ]

    rows = []

    for name in model_list:

        try:
            _, _, metric = run_single_model(
                model_name=name,
                df=df,
                feature_cols=feature_cols,
                target_col=target_col
            )

            row = {"Model": name}
            row.update(metric)
            rows.append(row)

            print(f"Done: {name}")

        except Exception as e:
            print(f"Failed: {name} -> {e}")

    result = pd.DataFrame(rows)

    if sort_by in result.columns:
        asc = sort_by != "R-squared"
        result = result.sort_values(
            sort_by,
            ascending=asc
        ).reset_index(drop=True)

    return result


# ==========================================================
# COMPARE BOOSTING ONLY
# ==========================================================
def compare_boosting_models(
    df,
    feature_cols,
    target_col,
    params_dict
):

    rows = []

    for model_name in ["CatBoost", "XGBoost", "LightGBM"]:

        params = params_dict.get(model_name, {})

        _, _, metric = run_single_model(
            model_name=model_name,
            df=df,
            feature_cols=feature_cols,
            target_col=target_col,
            params=params
        )

        row = {"Model": model_name}
        row.update(metric)

        rows.append(row)

    return pd.DataFrame(rows).sort_values("RMSE").reset_index(drop=True)