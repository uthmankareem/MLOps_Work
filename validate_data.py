import pandas as pd

BASELINE_ROWS = 20640
ROW_TOLERANCE = 0.1

df = pd.read_csv("data/housing.csv")

failed = 0
warnings = 0

def invariant(name, passed, detail=""):
    global failed
    status = "PASS" if passed else "FAIL"
    if not passed:
        failed += 1
    print(f"[{status}] {name} {detail}")

def expectation(name, passed, detail=""):
    global warnings
    status = "PASS" if passed else "WARN"
    if not passed:
        warnings += 1
    print(f"[{status}] {name} {detail}")

print("--- INVARIANTS (hard fail) ---")
invariant("all 9 columns present", list(df.columns) == [
    "MedInc", "HouseAge", "AveRooms", "AveBedrms",
    "Population", "AveOccup", "Latitude", "Longitude", "target",
])
invariant("no missing values", df.isna().sum().sum() == 0)
invariant("MedInc positive", (df["MedInc"] > 0).all())
invariant("AveOccup positive", (df["AveOccup"] > 0).all())
invariant("all columns numeric", all(df[col].dtype.kind in "fi" for col in df.columns))

print("--- EXPECTATIONS (warn on drift) ---")
rows = len(df)
deviation = abs(rows - BASELINE_ROWS) / BASELINE_ROWS
expectation(
    f"row count within {int(ROW_TOLERANCE * 100)}% of baseline ({BASELINE_ROWS})",
    deviation <= ROW_TOLERANCE,
    f"({rows} rows, deviation {deviation:.1%})",
)
expectation("no duplicate rows", df.duplicated().sum() == 0)
expectation("target within known range", df["target"].between(0.1, 5.1).all())

print("-" * 40)
print(f"RESULT: {failed} invariant(s) failed, {warnings} expectation(s) warned")

if failed:
    print("BLOCKED: data has structural problems. Do not train.")
elif warnings:
    print("ALLOWED with review: data passed invariants but drifted from baseline.")
else:
    print("ALLOWED: data ready for training.")