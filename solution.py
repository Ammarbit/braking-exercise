import numpy as np
import pandas as pd

STEP_S = 0.1  # grid spacing: 10 Hz


def resample_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Return df on a regular 10 Hz grid (see exercise.md)."""
    df = df.sort_values("timestamp_s")
    t = df["timestamp_s"].to_numpy()

    first_step = int(np.ceil(round(t[0] / STEP_S, 6)))
    last_step = int(np.floor(round(t[-1] / STEP_S, 6)))
    grid = np.round(np.arange(first_step, last_step + 1) * STEP_S, 1)

    known = df.dropna(subset=["speed_kmh"])
    speed = np.interp(grid, known["timestamp_s"], known["speed_kmh"])

    pos = np.searchsorted(t, grid, side="right") - 1
    brake = df["brake_pressed"].to_numpy()[pos]

    return pd.DataFrame({"speed_kmh": speed, "brake_pressed": brake}, index=grid)


def find_braking_events(df: pd.DataFrame, min_duration_s: float = 0.5) -> pd.DataFrame:
    """Return one row per braking event (see exercise.md)."""
    columns = ["start_s", "end_s", "duration_s", "speed_drop_kmh"]
    pressed = df["brake_pressed"].to_numpy() == 1

    padded = np.concatenate(([False], pressed, [False]))
    changes = np.flatnonzero(padded[1:] != padded[:-1])
    starts, ends = changes[::2], changes[1::2] - 1

    rows = []
    for s, e in zip(starts, ends):
        start_s, end_s = df.index[s], df.index[e]
        duration_s = round(end_s - start_s, 3)
        if duration_s < min_duration_s:
            continue
        drop = df["speed_kmh"].iloc[s] - df["speed_kmh"].iloc[e]
        rows.append([start_s, end_s, duration_s, round(drop, 2)])

    return pd.DataFrame(rows, columns=columns)


if __name__ == "__main__":
    raw = pd.read_csv("drive.csv")
    print(find_braking_events(resample_signals(raw)))