# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: float) -> float:
    """Percent of the service interval used up. True division, not floor —
    a car at 14,900 of 15,000 km is ~99.3% worn, not 0%."""
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """True once wear crosses WARN_AT_PERCENT. A car with no last-service
    reading has unknown wear, so it is NOT flagged."""
    last = car.get("last_service_km")
    if last is None:
        return False
    km_since = car["odometer"] - last
    return wear_percent(km_since, SERVICE_INTERVAL_KM) >= WARN_AT_PERCENT


def check_fleet(fleet: list) -> list:
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged