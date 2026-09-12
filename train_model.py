import joblib
from pathlib import Path

import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, RobustScaler

from features import make_features


# ---- Load data -------------------------------------------------------------
df = pd.read_csv("data/housing.csv")        # the versioned dataset (DVC-tracked)
X = df.drop(columns=["target"])             # all input features, minus the price column
y = df["target"]                            # the thing we predict: median house value

# Split BEFORE any transform so the test set genuinely never touches the model.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42    # 20% held out; same split every run (reproducible)
)

# ---- Build the trainable pipeline ------------------------------------------
# One object = features -> scaling -> model. Same belt runs at train AND deploy time.
pipeline = Pipeline([
    ("features", FunctionTransformer(make_features)),   # step 1: build the 4 engineered columns
    ("scale",    RobustScaler()),                        # step 2: median/IQR scaling (outlier-resistant)
    ("model",    RandomForestRegressor(n_estimators=100, random_state=42)),  # step 3: 100 trees
])

# ---- Experiment tracking with MLflow ----------------------------------------
mlflow.set_experiment("california-housing")   # the "bucket" this run gets filed under

with mlflow.start_run():                      # open a run — everything inside is recorded
    # Log the INPUTS (parameters) so we know exactly what produced this result.
    params = {
        "n_estimators": 100,
        "random_state": 42,
        "test_size": 0.2,
        "model": "RandomForestRegressor",
    }
    mlflow.log_params(params)

    # Honest estimate: train 5 folds, each tested on data it never trained on.
    scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="r2")
    print("Cross-val R2 per fold:", [round(s, 3) for s in scores])
    print("Mean cross-val R2:", round(scores.mean(), 3))

    # Real fit on ALL training data, then check on the locked-away test set.
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    test_r2 = r2_score(y_test, y_pred)
    test_mae = mean_absolute_error(y_test, y_pred)
    print("Test R2:", round(test_r2, 3))
    print("Test MAE (thousands $):", round(test_mae, 3))

    # Log the OUTPUTS (metrics) and the trained artifact itself.
    mlflow.log_metrics({"test_r2": test_r2, "test_mae": test_mae, "cv_r2_mean": scores.mean()})
    mlflow.sklearn.log_model(pipeline, name="model", serialization_format="cloudpickle")

    # ALSO save a plain joblib copy into models/ (what Stage 4 used).
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    joblib.dump(pipeline, models_dir / "housing_pipeline.joblib")
    print(f"Pipeline saved to {models_dir / 'housing_pipeline.joblib'}")

run = mlflow.last_active_run()   # peek at the most recent run (works AFTER the with-block closes)
print("MLflow run:", run.info.run_id)
print("See it at: mlflow ui")