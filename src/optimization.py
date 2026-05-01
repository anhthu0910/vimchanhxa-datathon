# ==========================================================
# file 1: optuna_tuning.py
# ==========================================================

import numpy as np
import pandas as pd
import optuna
import warnings

from sklearn.metrics import mean_squared_error
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

warnings.filterwarnings("ignore")

SEED = 42


# ==========================================================
# COMMON
# ==========================================================
def prepare_date(df, date_col="date"):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).reset_index(drop=True)
    return df


def get_model(model_name, params):

    if model_name == "CatBoost":
        return CatBoostRegressor(
            **params,
            random_seed=SEED,
            loss_function="RMSE",
            allow_writing_files=False,
            verbose=0
        )

    elif model_name == "XGBoost":
        return XGBRegressor(
            **params,
            objective="reg:squarederror",
            random_state=SEED,
            n_jobs=-1
        )

    elif model_name == "LightGBM":
        return LGBMRegressor(
            **params,
            random_state=SEED,
            n_jobs=-1,
            verbose=-1
        )

    else:
        raise ValueError("Use CatBoost / XGBoost / LightGBM")


def get_search_space(trial, model_name):

    if model_name == "CatBoost":
        return {
            "iterations": trial.suggest_int("iterations", 500, 1800),
            "depth": trial.suggest_int("depth", 4, 10),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.08),
            "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1, 12),
            "subsample": trial.suggest_float("subsample", 0.7, 1.0)
        }

    elif model_name == "XGBoost":
        return {
            "n_estimators": trial.suggest_int("n_estimators", 500, 1800),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.08),
            "subsample": trial.suggest_float("subsample", 0.7, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.7, 1.0),
            "min_child_weight": trial.suggest_int("min_child_weight", 1, 10)
        }

    elif model_name == "LightGBM":
        return {
            "n_estimators": trial.suggest_int("n_estimators", 500, 1800),
            "num_leaves": trial.suggest_int("num_leaves", 20, 160),
            "max_depth": trial.suggest_int("max_depth", 3, 12),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.08),
            "subsample": trial.suggest_float("subsample", 0.7, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.7, 1.0)
        }


# ==========================================================
# MAIN OPTUNA
# ==========================================================
def tune_optuna_walkforward(
    model_name,
    df,
    target,
    features,
    categorical_features=None,
    n_trials=50,
    folds=(2019, 2020, 2021, 2022),
    weights=(0.10, 0.15, 0.25, 0.50),
    date_col="date"
):
    """
    For data from 2012-07 onward:
    Tune robust params using recent folds.

    Return:
        best_params
    """

    df = prepare_date(df, date_col)

    def objective(trial):

        params = get_search_space(trial, model_name)

        total_score = 0

        for year, weight in zip(folds, weights):

            train_df = df[df[date_col].dt.year < year].copy()
            valid_df = df[df[date_col].dt.year == year].copy()

            if len(train_df) == 0 or len(valid_df) == 0:
                continue

            X_train = train_df[features]
            y_train = train_df[target]

            X_valid = valid_df[features]
            y_valid = valid_df[target]

            cat_idx = None
            if categorical_features:
                cat_idx = [
                    X_train.columns.get_loc(col)
                    for col in categorical_features
                    if col in X_train.columns
                ]

            model = get_model(model_name, params)

            if model_name == "CatBoost":
                model.fit(
                    X_train,
                    y_train,
                    cat_features=cat_idx,
                    eval_set=(X_valid, y_valid),
                    early_stopping_rounds=100,
                    verbose=0
                )
            else:
                model.fit(X_train, y_train)

            preds = model.predict(X_valid)

            rmse = np.sqrt(mean_squared_error(y_valid, preds))

            total_score += rmse * weight

        return total_score

    study = optuna.create_study(
        direction="minimize",
        sampler=optuna.samplers.TPESampler(seed=SEED)
    )

    study.optimize(
        objective,
        n_trials=n_trials,
        show_progress_bar=True
    )

    print("=" * 60)
    print("MODEL:", model_name)
    print("BEST SCORE:", round(study.best_value, 4))
    print("BEST PARAMS:")
    print(study.best_params)
    print("=" * 60)

    return study.best_params