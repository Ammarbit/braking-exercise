import pandas as pd
import pytest
from solution import find_braking_events, resample_signals


def make_grid(speeds, brakes):
    index = [round(0.1 * (i + 1), 1) for i in range(len(speeds))]
    return pd.DataFrame({"speed_kmh": speeds, "brake_pressed": brakes}, index=index)


def test_short_press_is_ignored():
    df = make_grid([50] * 10, [0, 0, 1, 1, 0, 0, 0, 0, 0, 0])
    assert find_braking_events(df).empty


def test_nan_gap_is_interpolated_linearly():
    raw = pd.DataFrame({
        "timestamp_s": [0.1, 0.2, 0.3, 0.4, 0.5],
        "speed_kmh": [50.0, float("nan"), float("nan"), 20.0, 20.0],
        "brake_pressed": [0, 0, 0, 0, 0],
    })
    out = resample_signals(raw)
    assert out.loc[0.2, "speed_kmh"] == pytest.approx(40.0)
    assert out.loc[0.3, "speed_kmh"] == pytest.approx(30.0)
    assert out["speed_kmh"].notna().all()


def test_no_events_keeps_columns():
    df = make_grid([50] * 5, [0] * 5)
    result = find_braking_events(df)
    assert list(result.columns) == ["start_s", "end_s", "duration_s", "speed_drop_kmh"]
    assert result.empty