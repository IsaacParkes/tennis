"""
ClubSpark API client for fetching tennis court availability.
"""

import math
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://clubspark.lta.org.uk"
API_PREFIX = "/v0/VenueBooking"

# Default location: Tewkesbury Road, N15
DEFAULT_LAT = 51.5805
DEFAULT_LNG = -0.0760
DEFAULT_RADIUS_MILES = 3.0


def _minutes_to_time(minutes):
    """Convert minutes-from-midnight to 'HH:MM' string."""
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"


def _time_to_minutes(time_str):
    """Convert 'HH:MM' string to minutes-from-midnight."""
    h, m = map(int, time_str.split(":"))
    return h * 60 + m


def _haversine(lat1, lng1, lat2, lng2):
    """Return distance in miles between two lat/lng points."""
    R = 3958.8
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))


def fetch_sessions(slug, date_str):
    """
    Fetch court availability for a venue on a given date.

    Args:
        slug: ClubSpark venue slug (e.g. 'FinsburyPark')
        date_str: Date in 'YYYY-MM-DD' format

    Returns:
        dict with parsed API response, or None on error
    """
    url = f"{BASE_URL}{API_PREFIX}/{slug}/GetVenueSessions"
    params = {"startDate": date_str, "endDate": date_str}

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        return None


def parse_availability(api_data, start_time=None, end_time=None):
    """
    Parse the API response into a list of available slots.

    Args:
        api_data: Raw JSON response from GetVenueSessions
        start_time: Optional filter - earliest time as 'HH:MM'
        end_time: Optional filter - latest time as 'HH:MM'

    Returns:
        List of dicts with keys: court_name, start, end, cost, lighting
    """
    if not api_data or "Resources" not in api_data:
        return []

    start_min = _time_to_minutes(start_time) if start_time else 0
    end_min = _time_to_minutes(end_time) if end_time else 1440

    available = []

    for resource in api_data["Resources"]:
        court_name = resource.get("Name", "Unknown Court")
        lighting = resource.get("Lighting", 0) == 1

        for day in resource.get("Days", []):
            for session in day.get("Sessions", []):
                session_start = session.get("StartTime", 0)
                session_end = session.get("EndTime", 0)
                capacity = session.get("Capacity", 0)
                name = session.get("Name", "")

                # Skip booked or closed slots
                if capacity == 0 or name in ("Booking", "Closed"):
                    continue

                cost = session.get("GuestPrice") or session.get("CourtCost") or session.get("CostFrom") or 0

                # Split into 1-hour slots
                slot_start = session_start
                while slot_start + 60 <= session_end:
                    slot_end = slot_start + 60

                    # Apply time filter per hour slot
                    if slot_start >= start_min and slot_end <= end_min:
                        available.append({
                            "court_name": court_name,
                            "start": _minutes_to_time(slot_start),
                            "end": _minutes_to_time(slot_end),
                            "cost": cost,
                            "lighting": lighting,
                        })

                    slot_start = slot_end

    return available


def get_availability(venues, date_str, start_time=None, end_time=None,
                     user_lat=None, user_lng=None, radius_miles=None):
    """
    Fetch availability across venues within radius of user location.

    Args:
        venues: List of venue dicts from courts.py
        date_str: Date in 'YYYY-MM-DD' format
        start_time: Optional earliest time as 'HH:MM'
        end_time: Optional latest time as 'HH:MM'
        user_lat: User's latitude (defaults to Tewkesbury Road N15)
        user_lng: User's longitude (defaults to Tewkesbury Road N15)
        radius_miles: Max distance in miles (defaults to 3.0)

    Returns:
        List of dicts: {venue, slots} for each venue within radius, sorted by distance
    """
    lat = user_lat if user_lat is not None else DEFAULT_LAT
    lng = user_lng if user_lng is not None else DEFAULT_LNG
    radius = radius_miles if radius_miles is not None else DEFAULT_RADIUS_MILES

    # Filter venues by radius and attach computed distance
    nearby = []
    for v in venues:
        dist = _haversine(lat, lng, v["lat"], v["lng"])
        if dist <= radius:
            nearby.append({**v, "distance_miles": round(dist, 1)})

    results = []

    def _fetch_one(venue):
        api_data = fetch_sessions(venue["slug"], date_str)
        slots = parse_availability(api_data, start_time, end_time)
        return venue, slots

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(_fetch_one, v): v for v in nearby}
        for future in as_completed(futures):
            venue, slots = future.result()
            results.append({
                "venue": venue,
                "slots": sorted(slots, key=lambda s: (s["court_name"], s["start"])),
            })

    results.sort(key=lambda r: r["venue"]["distance_miles"])
    return results
