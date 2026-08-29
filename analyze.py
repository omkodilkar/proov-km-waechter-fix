# analyze.py
# Make KM-Waechter smarter — rank cars by breakdown risk instead of waiting
# for the 80% wear rule to catch them.

try:
    import pandas as pd  # type: ignore[import-not-found]
except ModuleNotFoundError as exc:
    raise SystemExit(
        "This script requires pandas. Install it with: pip install pandas"
    ) from exc

df = pd.read_csv("fleet_history.csv")

FEATURES = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]

broke = df[df["broke_down"] == 1]
ok = df[df["broke_down"] == 0]

print("Column-by-column comparison (broke-down vs healthy cars):")
print(f"{'column':<18}{'broke mean':>12}{'healthy mean':>15}{'separation':>13}")
separation = {}
for col in FEATURES:
    m_broke, m_ok = broke[col].mean(), ok[col].mean()
    spread = ok[col].std() or 1e-9
    gap = (m_broke - m_ok) / spread  # how many "healthy std devs" apart the means are
    separation[col] = gap
    print(f"{col:<18}{m_broke:>12.1f}{m_ok:>15.1f}{gap:>13.2f}")

# Keep only columns with a real gap between the two groups.
predictive = {c: g for c, g in separation.items() if abs(g) >= 0.5}
print("\nColumns that actually separate broke-down cars from healthy ones:", list(predictive))


def normalize(series):
    lo, hi = series.min(), series.max()
    return (series - lo) / (hi - lo) if hi != lo else series * 0


df["risk_score"] = 0.0
weight_total = sum(abs(g) for g in predictive.values()) or 1.0
for col, gap in predictive.items():
    norm = normalize(df[col])
    if gap < 0:
        norm = 1 - norm  # a LOWER value of this column means HIGHER risk
    df["risk_score"] += norm * (abs(gap) / weight_total)
df["risk_score"] = (df["risk_score"] * 100).round(1)

ranked = df.sort_values("risk_score", ascending=False)
print("\nCars ranked by breakdown risk (highest first):")
print(ranked[["car_id", "risk_score", "broke_down"] + FEATURES].to_string(index=False))