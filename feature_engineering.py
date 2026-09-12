import numpy as np
import pandas as pd

from features import make_features


# ---- Demo script: show what feature engineering does to the data ------------
df = pd.read_csv("data/housing.csv")

print("Features before engineering:", df.shape)

log_skew_before = df["MedInc"].skew()   # skewness of raw median income (1.65 = right-skewed)

df = make_features(df)                  # apply the shared feature builder from features.py

print("Features after engineering:", df.shape)
print("-" * 40)
print(f"MedInc skew BEFORE log:  {log_skew_before:.2f}")
print(f"MedInc_log skew AFTER:   {df['MedInc_log'].skew():.2f}")  # |skew|<0.5 approx normal
print("-" * 40)
print(df[["MedInc_log", "rooms_per_bedroom", "people_per_household", "dist_to_bay"]].describe())