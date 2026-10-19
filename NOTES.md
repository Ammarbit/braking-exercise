# Notes
Grid: first 0.1 s step at/after the first timestamp to the last step at/before the last (0.2 to 29.9), built from integer steps to avoid float drift.
Speed: linear interpolation over time using only non-NaN rows, no extrapolation. This also fills the dropout at 14.0-14.5 s.
Brake: last raw value at or before each grid time, so it stays 0/1.
Event = run of brake=1 grid rows. end_s is the last pressed row, so duration_s = end_s - start_s.
Presses shorter than min_duration_s (0.5 s) are ignored, e.g. the blip at ~12.1 s.
speed_drop_kmh = speed at start_s minus speed at end_s, rounded to 2 decimals.
drive.csv is not in this repo. Put it next to solution.py and run `python solution.py`.
Tests: short press ignored, NaN gap with different endpoints (the gap in drive.csv is 50 to 50), empty result keeps its columns.
Improve: validate input columns, handle duplicate timestamps, flag a press still active at the end of the data, test unsorted input.