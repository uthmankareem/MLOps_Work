from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

# ---- Load the trained pipeline once, at startup ------------------------------
# Path is computed from THIS script's location, so it works no matter which
# folder the server is launched from.
PIPELINE_PATH = Path(__file__).resolve().parent / "models" / "housing_pipeline.joblib"
pipeline = joblib.load(PIPELINE_PATH)


# ---- Input schema (what a client must send as JSON) --------------------------
# Field names come from the dataset columns; Field(gt=0) rejects any value <= 0
# with a clear 422 error instead of letting garbage reach the model.
class HouseFeatures(BaseModel):
    MedInc: float = Field(gt=0, description="Median income, in tens of thousands of $")
    HouseAge: float = Field(gt=0, description="Median house age, in years")
    AveRooms: float = Field(gt=0, description="Average rooms per household")
    AveBedrms: float = Field(gt=0, description="Average bedrooms per household")
    Population: float = Field(gt=0, description="Block population")
    AveOccup: float = Field(gt=0, description="Average household size")
    Latitude: float = Field(ge=-90, le=90, description="Block latitude, degrees")
    Longitude: float = Field(ge=-180, le=180, description="Block longitude, degrees")


# ---- The app ----------------------------------------------------------------
app = FastAPI(
    title="California Housing Price Predictor",
    description="Serves the trained RandomForest pipeline built in Stages 4-5.",
    version="1.0.0",
)


@app.get("/")
def health():
    """Liveness check — confirms the server is up and the model is loaded."""
    return {
        "status": "ok",
        "model_loaded": pipeline is not None,
        "try_docs": "/docs",
    }


@app.post("/predict")
def predict(house: HouseFeatures):
    """Given one house's raw features, return the predicted median price.

    The pipeline (features -> scaling -> RandomForest) does all the work.
    """
    # Pydantic validated the JSON; build the exact DataFrame shape the pipeline
    # was trained on. model_dump() keeps the order of the fields defined above.
    X_raw = pd.DataFrame([house.model_dump()])

    # pipeline.predict feeds the raw 8 columns into make_features, which adds the
    # 4 engineered ones, RobustScaler normalizes, then the forest votes.
    prediction = float(pipeline.predict(X_raw)[0])

    # Price is in units of $100k (e.g. 2.7 = $270,000); round to 3 decimals.
    return {"price_100k": round(prediction, 3)}


@app.get("/predict")
def predict_get():
    """Friendly hint if someone opens the URL instead of POSTing to it."""
    return {
        "message": "Use POST /predict with a JSON body. Example body:",
        "example": {
            "MedInc": 8.5,
            "HouseAge": 30,
            "AveRooms": 6.2,
            "AveBedrms": 1.1,
            "Population": 800,
            "AveOccup": 2.9,
            "Latitude": 37.7,
            "Longitude": -122.2,
        },
    }