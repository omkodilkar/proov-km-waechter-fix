# fleet_report.py
from km_wachter import wear_percent, needs_service, SERVICE_INTERVAL_KM
from config_loader import load_settings, get_setting
from log_util import log, flush_log
import fleet_utils


def car_wear(car: dict) -> float:
    """Wear percent for one car. A car with no last-service reading
    contributes 0 — we don't know its wear, so we don't guess or crash."""
    last = car.get("last_service_km")
    if last is None:
        return 0.0
    return wear_percent(car["odometer"] - last, SERVICE_INTERVAL_KM)


def fleet_summary(fleet: list) -> dict:
    total = 0.0
    due = 0
    for car in fleet:
        total += car_wear(car)
        if needs_service(car):
            due += 1
    average = total / len(fleet)
    return {"count": len(fleet), "due": due, "average_wear": average}


def print_report(fleet: list) -> None:
    settings = load_settings()
    log(get_setting(settings, "report_title", "Nightly fleet report"))
    s = fleet_summary(fleet)
    print(f"Fleet: {s['count']} cars")
    print(f"Due for service: {s['due']}")
    print(f"Average wear: {s['average_wear']:.0f}%")

    total_km = sum(car["odometer"] for car in fleet)
    # The UK partner garage wants distance in miles (since 2015).
    miles = fleet_utils.km_to_miles(total_km)
    print(f"Fleet distance: {fleet_utils.format_number(miles)} miles")

    flush_log(get_setting(settings, "log_file", "km_wachter.log"))