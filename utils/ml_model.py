import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    root_mean_squared_error
)
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from sklearn.preprocessing import LabelEncoder

def detect_problem_type(df, target):

    data = df[target].dropna()

    # Check for identifier columns
    id_keywords = ["id", "number", "employee", "customer", "order", "invoice"]

    if any(word in target.lower() for word in id_keywords):
        return "Identifier"

    # Text columns
    if pd.api.types.is_object_dtype(data):
        return "Classification"

    # Numeric columns
    if pd.api.types.is_numeric_dtype(data):

        if data.nunique() <= 10:
            return "Classification"

        return "Regression"

    return "Unknown"

def get_valid_target_columns(df):

    valid_columns = []

    ignore_keywords = [
        "id",
        "number",
        "employee",
        "customer",
        "order",
        "invoice",
        "phone",
        "address",
        "postal",
        "city",
        "state",
        "country",
        "name",
        "email"
    ]

    for col in df.columns:

        col_lower = col.lower()

        # Skip identifier columns
        if any(word in col_lower for word in ignore_keywords):
            continue

        # Skip columns with all missing values
        if df[col].dropna().empty:
            continue

        valid_columns.append(col)

    return valid_columns

def train_regression_model(df, target):

    # Copy dataset
    data = df.copy()

    # Remove missing values
    data = data.dropna()

    # Convert categorical columns into numbers
    data = pd.get_dummies(data)

    # Target column after encoding
    target_columns = [col for col in data.columns if col.startswith(target)]

    if len(target_columns) == 0:
        return None

    target = target_columns[0]

    X = data.drop(columns=[target])

    y = data[target]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Train model
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    # Metrics
    results = {
        "R2": round(r2_score(y_test, predictions), 3),
        "MAE": round(mean_absolute_error(y_test, predictions), 3),
        "RMSE": round(root_mean_squared_error(y_test, predictions), 3),
        "Actual": y_test,
        "Predicted": predictions,
        "Importance": pd.DataFrame({
            "Feature": X.columns,
            "Importance": model.feature_importances_
        }).sort_values(
            by="Importance",
            ascending=False
        )
    }
    fig, ax = plt.subplots(figsize=(4, 3))

    ax.scatter(y_test, predictions)

    ax.plot(
        [y_test.min(), y_test.max()],
        [y_test.min(), y_test.max()],
        linestyle="--"
    )

    ax.set_xlabel("Actual Values")
    ax.set_ylabel("Predicted Values")
    ax.set_title("Actual vs Predicted")

    results["Plot"] = fig

    return results

def train_classification_model(df, target):

    data = df.copy()

    data = data.dropna()

    # Encode categorical columns
    for col in data.select_dtypes(include="object").columns:
        encoder = LabelEncoder()
        data[col] = encoder.fit_transform(data[col])

    X = data.drop(columns=[target])

    y = data[target]

    # Encode target if needed
    if y.dtype == "object":
        encoder = LabelEncoder()
        y = encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    results = {

        "Accuracy": round(
            accuracy_score(y_test, predictions),3
        ),

        "Precision": round(
            precision_score(
                y_test,
                predictions,
                average="weighted"
            ),3
        ),

        "Recall": round(
            recall_score(
                y_test,
                predictions,
                average="weighted"
            ),3
        ),

        "F1": round(
            f1_score(
                y_test,
                predictions,
                average="weighted"
            ),3
        ),

        "Confusion": confusion_matrix(
            y_test,
            predictions
        ),

        "Importance": pd.DataFrame({
            "Feature": X.columns,
            "Importance": model.feature_importances_
        }).sort_values(
            by="Importance",
            ascending=False
        )
    }

    return results