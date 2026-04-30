# visualization.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shap


# ==================================================
# GLOBAL STYLE
# ==================================================
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 11


# ==================================================
# 1. FEATURE IMPORTANCE
# ==================================================
def plot_feature_importance(
    model,
    features,
    top_features=20,
    figsize=(10, 7)
):
    """
    Plot feature importance for CatBoost / XGBoost / LightGBM
    """

    # Get importance
    if hasattr(model, "feature_importances_"):
        importance = model.feature_importances_

    elif hasattr(model, "get_feature_importance"):
        importance = model.get_feature_importance()

    else:
        raise ValueError("Model does not support feature importance.")

    imp_df = pd.DataFrame({
        "feature": features,
        "importance": importance
    })

    imp_df = (
        imp_df
        .sort_values("importance", ascending=False)
        .head(top_features)
        .iloc[::-1]
    )

    plt.figure(figsize=figsize)

    bars = plt.barh(
        imp_df["feature"],
        imp_df["importance"],
        alpha=0.9
    )

    for bar in bars:
        plt.text(
            bar.get_width(),
            bar.get_y() + bar.get_height()/2,
            f"{bar.get_width():.2f}",
            va="center",
            fontsize=9
        )

    plt.title("Top Feature Importance")
    plt.xlabel("Importance Score")
    plt.tight_layout()
    plt.show()


# ==================================================
# 2. SHAP SUMMARY
# ==================================================
def plot_shap_summary(
    model,
    df,
    features,
    top_features=20,
    sample_size=1000
):
    """
    SHAP Summary Plot
    """

    X = df[features].copy()

    if len(X) > sample_size:
        X = X.sample(sample_size, random_state=42)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    shap.summary_plot(
        shap_values,
        X,
        max_display=top_features,
        show=True
    )


# ==================================================
# 3. SHAP BAR IMPORTANCE
# ==================================================
def plot_shap_bar(
    model,
    df,
    features,
    top_features=20,
    sample_size=1000
):
    """
    Mean Absolute SHAP Importance
    """

    X = df[features].copy()

    if len(X) > sample_size:
        X = X.sample(sample_size, random_state=42)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    shap.summary_plot(
        shap_values,
        X,
        plot_type="bar",
        max_display=top_features,
        show=True
    )


# ==================================================
# 4. ACTUAL VS PREDICTION
# ==================================================
def plot_prediction_vs_actual(
    df,
    target,
    pred_col="prediction",
    date_col="date",
    figsize=(15, 6)
):
    """
    Compare actual vs prediction over time
    """

    plot_df = df.sort_values(date_col).copy()

    plt.figure(figsize=figsize)

    plt.plot(
        plot_df[date_col],
        plot_df[target],
        label="Actual",
        linewidth=2
    )

    plt.plot(
        plot_df[date_col],
        plot_df[pred_col],
        label="Prediction",
        linewidth=2
    )

    plt.title(f"Actual vs Prediction ({target})")
    plt.xlabel("Date")
    plt.ylabel(target)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# ==================================================
# 5. RESIDUAL PLOT
# ==================================================
def plot_residuals(
    df,
    target,
    pred_col="prediction",
    figsize=(10, 6)
):
    """
    Residual distribution
    """

    residuals = df[target] - df[pred_col]

    plt.figure(figsize=figsize)

    sns.histplot(
        residuals,
        bins=40,
        kde=True
    )

    plt.axvline(0, linestyle="--")
    plt.title("Residual Distribution")
    plt.xlabel("Actual - Prediction")
    plt.tight_layout()
    plt.show()


# ==================================================
# 6. QUICK REPORT
# ==================================================
def full_visual_report(
    model,
    df,
    target,
    features,
    top_features=20
):
    """
    Run full report
    """

    plot_feature_importance(
        model=model,
        features=features,
        top_features=top_features
    )

    plot_shap_summary(
        model=model,
        df=df,
        features=features,
        top_features=top_features
    )

    plot_prediction_vs_actual(
        df=df,
        target=target
    )

    plot_residuals(
        df=df,
        target=target
    )