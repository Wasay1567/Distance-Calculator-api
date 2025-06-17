from fastapi import FastAPI, Query
from math import radians, cos, sin, sqrt, atan2

app = FastAPI()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers

    φ1, φ2 = radians(lat1), radians(lat2)
    Δφ = radians(lat2 - lat1)
    Δλ = radians(lon2 - lon1)

    a = sin(Δφ / 2) ** 2 + cos(φ1) * cos(φ2) * sin(Δλ / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

@app.get("/distance")
def get_distance(
    lat1: float = Query(..., description="Latitude of point A"),
    lon1: float = Query(..., description="Longitude of point A"),
    lat2: float = Query(..., description="Latitude of point B"),
    lon2: float = Query(..., description="Longitude of point B"),
    unit: str = Query("km", description="Unit: km or miles")
):
    distance_km = haversine(lat1, lon1, lat2, lon2)
    if unit == "miles":
        distance = distance_km * 0.621371
    else:
        distance = distance_km

    return {
        "point_A": {"lat": lat1, "lon": lon1},
        "point_B": {"lat": lat2, "lon": lon2},
        "distance": round(distance, 2),
        "unit": unit
    }
