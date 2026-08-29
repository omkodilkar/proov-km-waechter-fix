# test_fleet_report.py
from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars():
    assert fleet_summary(SAMPLE)["due"] == 1


def test_summary_survives_missing_reading():
    """A car with no last-service reading (like VOS-7788) must not crash
    the nightly report."""
    fleet = SAMPLE + [{"id": "VOS-7788", "odometer": 92000}]
    summary = fleet_summary(fleet)
    assert "average_wear" in summary
    assert summary["due"] == 1