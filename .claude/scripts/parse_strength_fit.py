#!/usr/bin/env python3
"""
Parse a COROS strength-training .fit file and print per-set weight/reps.

Usage: python3 parse_strength_fit.py /path/to/file.fit

Notes:
- COROS's strength FIT files trip up `fitparse` (malformed field size in a
  later definition message) — use `fitdecode` instead, which tolerates it
  with a warning.
- Weight is stored in kg; this script converts to lb.
- The `category` field is a generic COROS movement category (squat,
  deadlift, lunge, hip_raise, pull_up, row, plank, ...) — map it to the
  actual named exercise from the day's plan by hand, since COROS doesn't
  know "goblet squat" vs "back squat", or "barbell row" vs "single-arm DB
  row".
- Weight is whatever total load was entered on the watch. For two-dumbbell
  exercises, confirm with the athlete whether that's per-hand or combined —
  COROS doesn't distinguish, and it isn't always obvious from the number.
"""
import sys
import fitdecode


def main(path):
    sets = []
    with fitdecode.FitReader(path) as fit:
        for frame in fit:
            if isinstance(frame, fitdecode.FitDataMessage) and frame.name == "set":
                sets.append({f.name: f.value for f in frame.fields})

    active = [s for s in sets if s.get("set_type") == "active"]

    print(f"{'Category':12s} | {'Reps':>4s} | {'Weight':>10s} | Timestamp")
    print("-" * 60)
    for s in active:
        w_kg = s.get("weight")
        w_lb = f"{w_kg * 2.20462:.1f} lb" if w_kg else "bodyweight"
        reps = s.get("repetitions")
        reps_str = str(reps) if reps is not None else f"{s.get('duration', 0):.0f}s hold"
        ts = s.get("timestamp")
        print(f"{s.get('category', '?'):12s} | {reps_str:>4s} | {w_lb:>10s} | {ts}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} /path/to/file.fit")
        sys.exit(1)
    main(sys.argv[1])
