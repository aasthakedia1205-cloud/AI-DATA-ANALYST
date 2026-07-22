import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.metrics import r2_score


def compare_models(df, target):

    data = df.copy()

    data = data.dropna()

    # Convert categorical columns
    data = pd.get_dummies(data)

    target_cols = [c for c in data.columns if c.startswith(target)]

    if len(target_cols) == 0:
        return None

    target = target_cols[0]

    X = data.drop(columns=[target])
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=42),
        "Random Forest": RandomForestRegressor(
            random_state=42,
            n_estimators=200
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            random_state=42
        )
    }

    results = []

    for name, model in models.items():

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        score = r2_score(y_test, predictions)

        results.append({
            "Model": name,
            "R² Score": round(score, 3)
        })

    comparison = pd.DataFrame(results)

    comparison = comparison.sort_values(
        by="R² Score",
        ascending=False
    )

    return comparison