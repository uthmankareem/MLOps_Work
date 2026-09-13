from pathlib import Path

import joblib
import pandas as pd
import requests

# The live server started in another terminal (uvicorn on port 8000).
BASE_URL = "http://127.0.0.1:8000"

# Load the same model the server is using, so we can compare answers 1:1.
model = joblib.load(
    Path(__file__).resolve().parent / "models" / "housing_pipeline.joblib"
)

# Health check first: is the server alive and is the model loaded?
r = requests.get(f"{BASE_URL}/")
print("GET / ->", r.status_code, r.json())

# Now test the real deal: send 5 REAL rows from the dataset to the API.
df = pd.read_csv("data/housing.csv")  # raw features only — no target needed
for i in range(5):
    raw = df.drop(columns=["target"]).iloc[i].to_dict()  # as a real client sends it

    # Ground truth: what the model says when run directly on this machine...
    local_price = float(model.predict(pd.DataFrame([raw]))[0])

    # ...vs what the live API answers over HTTP.
    resp = requests.post(f"{BASE_URL}/predict", json=raw)
    api_price = resp.json()["price_100k"]

    match = "MATCH" if round(local_price, 3) == api_price else "DIFF!"
    print(f"row {i}: local={local_price:.4f}  api={api_price}  ->  {match}")