from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.prescription import Prescription
from app.schemas.prescription_stats import PrescriptionTimeStatsResponse, TimeSeriesDataPoint
from datetime import datetime

def get_prescription_time_stats(db: Session, interval: str = "month"):
    """
    Calculates prescription counts over time.
    interval: 'day', 'month', or 'year'
    """
    if interval == "day":
        format_str = "%Y-%m-%d"
        sqlite_format = "strftime('%Y-%m-%d', created_at)"
    elif interval == "month":
        format_str = "%Y-%m"
        sqlite_format = "strftime('%Y-%m', created_at)"
    elif interval == "year":
        format_str = "%Y"
        sqlite_format = "strftime('%Y', created_at)"
    else:
        raise ValueError("Invalid interval. Choose 'day', 'month', or 'year'.")

    # Query to count prescriptions grouped by date period
    results = db.query(
        func.strftime(sqlite_format, Prescription.created_at).label("period"),
        func.count(Prescription.id).label("count")
    ).group_by("period").order_by("period").all()

    stats = [TimeSeriesDataPoint(period=row[0], count=row[1]) for row in results]
    
    total_prescriptions = sum(point.count for point in stats)
    
    # Simple trend analysis
    trend = "stable"
    if len(stats) >= 2:
        first_half = sum(p.count for p in stats[:len(stats)//2])
        second_half = sum(p.count for p in stats[len(stats)//2:])
        if second_half > first_half * 1.1:
            trend = "increasing"
        elif second_half < first_half * 0.9:
            trend = "decreasing"

    return PrescriptionTimeStatsResponse(
        total_prescriptions=total_prescriptions,
        stats=stats,
        trend=trend
    )
