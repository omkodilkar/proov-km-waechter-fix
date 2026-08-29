# fleet_utils.py
KM_TO_MILES = 0.621371  # 1 km = 0.621371 mi (old value, 1.609, was inverted —
                         # that's km per mile, not miles per km)


def km_to_miles(km: float) -> float:
    """Used by the nightly run for the UK partner report. Do not remove."""
    return km * KM_TO_MILES


def format_number(value: float) -> str:
    return f"{value:.1f}"