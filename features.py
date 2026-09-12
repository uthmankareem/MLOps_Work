import numpy as np


def make_features(df):
    """Turn raw California Housing columns into engineered feature columns."""
    df = df.copy()  # work on a copy so we never mutate the caller's DataFrame
    df["MedInc_log"] = np.log1p(df["MedInc"])  # == log(1 + MedInc): pulls right-skew tail toward normal
    df["rooms_per_bedroom"] = df["AveRooms"] / df["AveBedrms"]  # ratio: house size per bedroom pool
    df["people_per_household"] = df["Population"] / df["AveOccup"]  # ratio: how crowded households are
    bay_lat, bay_lon = 37.5, -122.0  # reference point near the SF Bay area
    df["dist_to_bay"] = np.sqrt(  # Euclidean distance from (lat, lon) to the bay anchor
        (df["Latitude"] - bay_lat) ** 2 + (df["Longitude"] - bay_lon) ** 2
    )
    return df