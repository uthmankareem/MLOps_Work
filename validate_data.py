import pandas as pd

df = pd.read_csv("data/housing.csv")

results = []

def check(name, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    results.append(status)
    print(f"[{status}] {name} {detail}")

check("row count == 20640", len(df) == 20640)
check("all 9 columns present", list(df.columns) == [
    "MedInc", "HouseAge", "AveRooms", "AveBedrms",
    "Population", "AveOccup", "Latitude", "Longitude", "target",
])
check("no missing values", df.isna().sum().sum() == 0)
check("no duplicate rows", df.duplicated().sum() == 0)
check("target within known range", df["target"].between(0.1, 5.1).all())
check("MedInc positive", (df["MedInc"] > 0).all())
check("AveOccup positive", (df["AveOccup"] > 0).all())
check("all columns numeric", all(df[col].dtype.kind in "fi" for col in df.columns))

passed = results.count("PASS")
print("-" * 40)
print(f"VALIDATION RESULT: {passed}/{len(results)} checks passed")

if passed != len(results):
    print("Data has problems. Fix before training.")
else:
    print("Data ready for training.")