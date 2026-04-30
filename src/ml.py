# ml.py
# ============================================================
# Benchmark models for revenue forecasting (tabular features)
# ============================================================

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

# ============================================================
# LINEAR MODELS
# ============================================================

from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    Lasso,
    ElasticNet,
    BayesianRidge,
    HuberRegressor
)

# ============================================================
# TREE / ENSEMBLE MODELS
# ============================================================

from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    HistGradientBoostingRegressor,
    AdaBoostRegressor
)

from sklearn.tree import DecisionTreeRegressor

# ============================================================
# EXTERNAL BOOSTING MODELS
# ============================================================

from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor


# ============================================================
# GLOBAL CONFIG
# ============================================================

RANDOM_STATE   = 42
TRAIN_END_DATE = "2021-12-31"
VAL_START_DATE = "2022-01-01"
VAL_END_DATE   = "2022-12-31"


# ============================================================
# DATA PREP
# ============================================================

def prepare_data(df, feature_cols, target_col="revenue"):
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # remove rows containing NaN (common from lag features)
    use_cols = ["date", target_col] + feature_cols
    df = df[use_cols].dropna().reset_index(drop=True)

    train = df[df["date"] <= TRAIN_END_DATE].copy()
    val = df[
        (df["date"] >= VAL_START_DATE) &
        (df["date"] <= VAL_END_DATE)
    ].copy()

    X_train = train[feature_cols]
    y_train = train[target_col]

    X_val = val[feature_cols]
    y_val = val[target_col]

    return train, val, X_train, y_train, X_val, y_val


# ============================================================
# METRICS
# ============================================================

def evaluate_metrics(y_true, y_pred):
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "MAPE": mean_absolute_percentage_error(y_true, y_pred) * 100,
        "R-squared": r2_score(y_true, y_pred)
    }


# ============================================================
# CORE RUNNER
# ============================================================

def run_model(model, df, feature_cols, target_col="revenue"):
    train, val, X_train, y_train, X_val, y_val = prepare_data(
        df, feature_cols, target_col
    )

    model.fit(X_train, y_train)

    val_result = val.copy()
    val_result["prediction"] = model.predict(X_val)

    # revenue cannot be negative
    val_result["prediction"] = np.maximum(val_result["prediction"], 0)

    metrics = evaluate_metrics(y_val, val_result["prediction"])

    return val_result, model, metrics


# ============================================================
# LINEAR FAMILY
# ============================================================

def linear_regression_model(df, feature_cols, target_col="revenue", params=None):
    basic = {}
    if params:
        basic.update(params)

    model = LinearRegression(**basic)
    return run_model(model, df, feature_cols, target_col)


def ridge_model(df, feature_cols, target_col="revenue", params=None):
    basic = {
        "alpha": 1.0
    }
    if params:
        basic.update(params)

    model = Ridge(**basic)
    return run_model(model, df, feature_cols, target_col)


def lasso_model(df, feature_cols, target_col="revenue", params=None):
    basic = {
        "alpha": 1.0,
        "max_iter": 5000,
        "random_state": RANDOM_STATE
    }
    if params:
        basic.update(params)

    model = Lasso(**basic)
    return run_model(model, df, feature_cols, target_col)


def elasticnet_model(df, feature_cols, target_col="revenue", params=None):
    basic = {
        "alpha": 1.0,
        "l1_ratio": 0.5,
        "max_iter": 5000,
        "random_state": RANDOM_STATE
    }
    if params:
        basic.update(params)

    model = ElasticNet(**basic)
    return run_model(model, df, feature_cols, target_col)


def bayesian_ridge_model(df, feature_cols, target_col="revenue", params=None):
    basic = {}
    if params:
        basic.update(params)

    model = BayesianRidge(**basic)
    return run_model(model, df, feature_cols, target_col)


def huber_model(df, feature_cols, target_col="revenue", params=None):
    basic = {
        "epsilon": 1.35,
        "max_iter": 500
    }
    if params:
        basic.update(params)

    model = HuberRegressor(**basic)
    return run_model(model, df, feature_cols, target_col)


# ============================================================
# TREE MODELS
# ============================================================

def decision_tree_model(df, feature_cols, target_col="revenue", params=None):
    basic = {
        "random_state": RANDOM_STATE
    }
    if params:
        basic.update(params)

    model = DecisionTreeRegressor(**basic)
    return run_model(model, df, feature_cols, target_col)


def random_forest_model(df, feature_cols, target_col="revenue", params=None):
    basic = {
        "n_estimators": 300,
        "random_state": RANDOM_STATE,
        "n_jobs": -1
    }
    if params:
        basic.update(params)

    model = RandomForestRegressor(**basic)
    return run_model(model, df, feature_cols, target_col)


def extra_trees_model(df, feature_cols, target_col="revenue", params=None):
    basic = {
        "n_estimators": 300,
        "random_state": RANDOM_STATE,
        "n_jobs": -1
    }
    if params:
        basic.update(params)

    model = ExtraTreesRegressor(**basic)
    return run_model(model, df, feature_cols, target_col)


# ============================================================
# BOOSTING MODELS (SKLEARN)
# ============================================================

def hist_gbm_model(df, feature_cols, target_col="revenue", params=None):
    basic = {
        "max_iter": 300,
        "random_state": RANDOM_STATE
    }
    if params:
        basic.update(params)

    model = HistGradientBoostingRegressor(**basic)
    return run_model(model, df, feature_cols, target_col)


def adaboost_model(df, feature_cols, target_col="revenue", params=None):
    basic = {
        "n_estimators": 300,
        "random_state": RANDOM_STATE
    }
    if params:
        basic.update(params)

    model = AdaBoostRegressor(**basic)
    return run_model(model, df, feature_cols, target_col)


# ============================================================
# LIGHTGBM
# ============================================================

def lightgbm_model(df, feature_cols, target_col="revenue", params=None):
    basic = {
        "n_estimators": 500,
        "learning_rate": 0.05,
        "random_state": RANDOM_STATE,
        "n_jobs": -1,
        "verbose": -1
    }
    if params:
        basic.update(params)

    model = LGBMRegressor(**basic)
    return run_model(model, df, feature_cols, target_col)


def lightgbm_dart_model(df, feature_cols, target_col="revenue", params=None):
    basic = {
        "boosting_type": "dart",
        "n_estimators": 500,
        "learning_rate": 0.05,
        "random_state": RANDOM_STATE,
        "n_jobs": -1,
        "verbose": -1
    }
    if params:
        basic.update(params)

    model = LGBMRegressor(**basic)
    return run_model(model, df, feature_cols, target_col)


# ============================================================
# XGBOOST
# ============================================================

def xgboost_model(df, feature_cols, target_col="revenue", params=None):
    basic = {
        "n_estimators": 500,
        "learning_rate": 0.05,
        "random_state": RANDOM_STATE,
        "n_jobs": -1,
        "verbosity": 0
    }
    if params:
        basic.update(params)

    model = XGBRegressor(**basic)
    return run_model(model, df, feature_cols, target_col)


# ============================================================
# CATBOOST
# ============================================================

def catboost_model(df, feature_cols, target_col="revenue", params=None):
    basic = {
        "iterations": 500,
        "learning_rate": 0.05,
        "random_seed": RANDOM_STATE,
        "verbose": 0,
        "allow_writing_files": False
    }
    if params:
        basic.update(params)

    model = CatBoostRegressor(**basic)
    return run_model(model, df, feature_cols, target_col)


# ============================================================
# MODEL ZOO
# ============================================================

MODEL_ZOO = {
    # Linear
    "LinearRegression": linear_regression_model,
    "Ridge": ridge_model,
    "Lasso": lasso_model,
    "ElasticNet": elasticnet_model,
    "BayesianRidge": bayesian_ridge_model,
    "HuberRegressor": huber_model,

    # Tree
    "DecisionTree": decision_tree_model,
    "RandomForest": random_forest_model,
    "ExtraTrees": extra_trees_model,

    # Boosting sklearn
    "HistGradientBoosting": hist_gbm_model,
    "AdaBoost": adaboost_model,

    # External Boosting
    "LightGBM": lightgbm_model,
    "LightGBM_DART": lightgbm_dart_model,
    "XGBoost": xgboost_model,
    "CatBoost": catboost_model,
}


# ============================================================
# BENCHMARK ALL MODELS
# ============================================================

def run_all_models(
    df,
    features,
    target="revenue",
    sort_by="RMSE"
):
    """
    Returns ranking dataframe.
    """

    results = []

    for model_name, model_func in MODEL_ZOO.items():
        try:
            _, _, metric = model_func(
                df=df,
                feature_cols=features,
                target_col=target
            )

            row = {
                "Model": model_name,
                "MAE": metric["MAE"],
                "RMSE": metric["RMSE"],
                "MAPE": metric["MAPE"],
                "R-squared": metric["R-squared"]
            }

            results.append(row)

            print(f"Done: {model_name}")

        except Exception as e:
            print(f"Failed: {model_name} --> {e}")

    result_df = pd.DataFrame(results)

    if sort_by in result_df.columns:
        ascending = True
        if sort_by == "R-squared":
            ascending = False

        result_df = result_df.sort_values(
            sort_by,
            ascending=ascending
        ).reset_index(drop=True)

    return result_df


# ============================================================
# RUN ONE MODEL WITH CUSTOM PARAMS
# ============================================================

def run_single_model(
    model_name,
    df,
    features,
    target="revenue",
    params=None
):
    """
    Example:
    run_single_model(
        "LightGBM",
        df,
        features,
        params={"num_leaves":31}
    )
    """

    if model_name not in MODEL_ZOO:
        raise ValueError(f"{model_name} not found in MODEL_ZOO")

    return MODEL_ZOO[model_name](
        df=df,
        feature_cols=features,
        target_col=target,
        params=params
    )