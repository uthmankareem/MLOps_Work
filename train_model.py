import joblib
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, RobustScaler


def make_features(df):
    df = df.copy()
    df["MedInc_log"] = np.log1p(df["MedInc"])
    df["rooms_per_bedroom"] = df["AveRooms"] / df["AveBedrms"]
    df["people_per_household"] = df["Population"] / df["AveOccup"]
    bay_lat, bay_lon = 37.5, -122.0
    df["dist_to_bay"] = np.sqrt(
        (df["Latitude"] - bay_lat) ** 2 + (df["Longitude"] - bay_lon) ** 2
    )
    return df


df = pd.read_csv("data/housing.csv")
X = df.drop(columns=["target"])
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pipeline = Pipeline([
    ("features", FunctionTransformer(make_features)),
    ("scale", RobustScaler()),
    ("model", RandomForestRegressor(n_estimators=100, random_state=42)),
])

scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="r2")
print("Cross-val R2 per fold:", [round(s, 3) for s in scores])
print("Mean cross-val R2:", round(scores.mean(), 3))

pipeline.fit(X_train, y_train)

from sklearn.metrics import mean_absolute_error, r2_score

y_pred = pipeline.predict(X_test)
print("Test R2:", round(r2_score(y_test, y_pred), 3))
print("Test MAE (thousands $):", round(mean_absolute_error(y_test, y_pred), 3))

models_dir = Path("models")
models_dir.mkdir(exist_ok=True)
joblib.dump(pipeline, models_dir / "housing_pipeline.joblib")
print("Pipeline saved to models/housing_pipeline.joblib")