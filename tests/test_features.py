"""Unit tests for features.make_features.

These run anywhere Python runs - no server, no model, no network. That is
exactly what makes them suitable for CI: fast, deterministic, no side effects.

Run locally:  .\\.venv\\Scripts\\python.exe -m unittest discover -s tests -t . -v
"""
import unittest

import pandas as pd

from features import make_features

RAW_ROW = {
    "MedInc": 8.5,
    "HouseAge": 30,
    "AveRooms": 6.2,
    "AveBedrms": 1.1,
    "Population": 800,
    "AveOccup": 2.9,
    "Latitude": 37.7,
    "Longitude": -122.2,
}

ENGINEERED = ["MedInc_log", "rooms_per_bedroom", "people_per_household", "dist_to_bay"]


class TestMakeFeatures(unittest.TestCase):
    def setUp(self):
        self.raw = pd.DataFrame([RAW_ROW])

    def test_adds_all_four_engineered_columns(self):
        out = make_features(self.raw)
        for col in ENGINEERED:
            self.assertIn(col, out.columns)

    def test_does_not_mutate_the_caller_frame(self):
        make_features(self.raw)
        for col in ENGINEERED:
            self.assertNotIn(col, self.raw.columns)

    def test_medinc_log_uses_log1p(self):
        out = make_features(self.raw)
        self.assertAlmostEqual(out["MedInc_log"].iloc[0], 2.251291799, places=6)

    def test_rooms_per_bedroom_is_a_ratio(self):
        out = make_features(self.raw)
        self.assertAlmostEqual(out["rooms_per_bedroom"].iloc[0], 6.2 / 1.1, places=6)

    def test_dist_to_bay_matches_expected_geometry(self):
        out = make_features(self.raw)
        self.assertAlmostEqual(out["dist_to_bay"].iloc[0], 0.2828427125, places=6)


if __name__ == "__main__":
    unittest.main()
