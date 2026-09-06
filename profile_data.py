import pandas as pd
from pathlib import Path
from ydata_profiling import ProfileReport

df = pd.read_csv("data/housing.csv")

print("Shape:", df.shape)
print("Missing values per column:")
print(df.isna().sum())

reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)

report = ProfileReport(df, title="California Housing — Data Profile")
report.to_file(reports_dir / "housing_profile.html")

print("Report saved to reports/housing_profile.html")