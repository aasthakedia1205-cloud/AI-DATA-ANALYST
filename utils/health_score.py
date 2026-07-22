import pandas as pd
import numpy as np


def calculate_health_score(df):

    score = 100
    report = {}

    # ----------------------------
    # Missing Values
    # ----------------------------
    missing = df.isnull().sum().sum()

    missing_percent = (
        missing / (df.shape[0] * df.shape[1])
    ) * 100

    report["Missing Values"] = missing
    report["Missing %"] = round(missing_percent, 2)

    if missing_percent > 10:
        score -= 20
    elif missing_percent > 5:
        score -= 10

    # ----------------------------
    # Duplicate Rows
    # ----------------------------
    duplicates = df.duplicated().sum()

    report["Duplicate Rows"] = duplicates

    if duplicates > 0:
        score -= 10

    # ----------------------------
    # Empty Columns
    # ----------------------------
    empty_columns = df.columns[df.isnull().all()].tolist()

    report["Empty Columns"] = len(empty_columns)

    if len(empty_columns) > 0:
        score -= 10

    # ----------------------------
    # Numeric Outliers
    # ----------------------------
    outliers = 0

    numeric_cols = df.select_dtypes(include=np.number)

    for col in numeric_cols.columns:

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers += df[
            (df[col] < lower) |
            (df[col] > upper)
        ].shape[0]

    report["Outliers"] = outliers

    if outliers > 20:
        score -= 15

    # ----------------------------
    # Memory Usage
    # ----------------------------
    memory = df.memory_usage(deep=True).sum() / 1024**2

    report["Memory Usage"] = round(memory, 2)

    score = max(score, 0)

    return score, report