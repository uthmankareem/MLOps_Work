import numpy as np
import pandas as pd

df = pd.read_csv("data/housing.csv")

print("Features before engineering:", df.shape)

log_skew_before = df["MedInc"].skew()

df["MedInc_log"] = np.log1p(df["MedInc"])
df["rooms_per_bedroom"] = df["AveRooms"] / df["AveBedrms"]
df["people_per_household"] = df["Population"] / df["AveOccup"]

bay_lat, bay_lon = 37.5, -122.0
df["dist_to_bay"] = np.sqrt(
    (df["Latitude"] - bay_lat) ** 2 + (df["Longitude"] - bay_lon) ** 2
)

print("Features after engineering:", df.shape)
print("-" * 40)
print(f"MedInc skew BEFORE log:  {log_skew_before:.2f}")
print(f"MedInc_log skew AFTER:   {df['MedInc_log'].skew():.2f}")
print("-" * 40)
print(df[["MedInc_log", "rooms_per_bedroom", "people_per_household", "dist_to_bay"]].describe())