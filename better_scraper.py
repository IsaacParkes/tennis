"""
Better.org (GLL) API client for fetching tennis court availability.

Venues are discovered from the OpenActive FacilityUse RPDE feed:
  https://better-admin.org.uk/api/openactive/better/facility-uses

Availability is fetched from the internal slots API:
  https://better-admin.org.uk/api/activities/location/{slug}/{activity}/slots?date=YYYY-MM-DD
"""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

BETTER_BASE = "https://better-admin.org.uk"
OPENACTIVE_FACILITY_USES = f"{BETTER_BASE}/api/openactive/better/facility-uses"
SLOTS_API = f"{BETTER_BASE}/api/activities/location/{{slug}}/{{activity}}/slots"
BOOKING_URL = "https://bookings.better.org.uk/location/{slug}/{activity}/{date}/by-time"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; TennisCourtsBot/1.0)",
    "Accept": "application/json",
}


def _time_to_minutes(time_str):
    h, m = map(int, time_str.split(":"))
    return h * 60 + m


def discover_london_tennis_venues():
    """
    Paginate the Better OpenActive FacilityUse RPDE feed and return all
    London tennis court venues with lat/lng and booking slugs.

    Returns:
        List of dicts with keys: name, slug, activity_slug, borough, lat, lng, source
    """
    venues = []
    url = OPENACTIVE_FACILITY_USES

    while url:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            break

        items = data.get("items", [])
        next_url = data.get("next", "")

        for item in items:
            if item.get("state") != "updated":
                continue
            d = item.get("data", {})

            # Filter for tennis
            activities = [a.get("prefLabel", "") for a in d.get("activity", [])]
            facility_types = [f.get("prefLabel", "") for f in d.get("facilityType", [])]
            name = d.get("name", "")
            is_tennis = (
                any("tennis" in a.lower() for a in activities)
                or any("tennis" in f.lower() for f in facility_types)
                or "tennis" in name.lower()
            )
            if not is_tennis:
                continue

            loc = d.get("location", {})
            geo = loc.get("geo", {})
            lat = geo.get("latitude")
            lng = geo.get("longitude")

            # Filter for London (rough lat/lng bounding box)
            if lat is None or lng is None:
                continue
            if not (51.28 <= lat <= 51.70 and -0.55 <= lng <= 0.30):
                continue

            booking_url = d.get("url", "")
            # Extract venue slug and activity slug from URL
            # Format: https://bookings.better.org.uk/location/{slug}/{activity}/...
            slug = ""
            activity_slug = "tennis-pay-and-play"
            if "bookings.better.org.uk/location/" in booking_url:
                parts = booking_url.split("/location/")[1].split("/")
                if len(parts) >= 2:
                    slug = parts[0]
                    activity_slug = parts[1] if parts[1] else activity_slug

            if not slug:
                continue

            venue_name = loc.get("name") or name
            address = loc.get("address", {})
            borough = address.get("addressLocality", "")

            venues.append({
                "name": venue_name,
                "slug": slug,
                "activity_slug": activity_slug,
                "borough": borough,
                "lat": round(lat, 6),
                "lng": round(lng, 6),
                "source": "better",
            })

        # Stop if next URL didn't change (end of feed)
        if not next_url or next_url == url:
            break
        url = next_url

    # Deduplicate by slug
    seen = set()
    unique = []
    for v in venues:
        if v["slug"] not in seen:
            seen.add(v["slug"])
            unique.append(v)
    return unique


def fetch_better_slots(slug, activity_slug, date_str):
    """
    Fetch available slots for a Better venue on a given date.

    Returns:
        List of slot dicts, or None on error
    """
    url = SLOTS_API.format(slug=slug, activity=activity_slug)
    try:
        resp = requests.get(url, params={"date": date_str}, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        return None


def parse_better_slots(slots_data, start_time=None, end_time=None):
    """
    Parse Better slots API response into the same format as ClubSpark slots.

    Returns:
        List of dicts with keys: court_name, start, end, cost, lighting
    """
    if not slots_data:
        return []

    start_min = _time_to_minutes(start_time) if start_time else 0
    end_min = _time_to_minutes(end_time) if end_time else 1440

    available = []

    # Handle both list and dict ({"slots": [...]}) response formats
    items = slots_data if isinstance(slots_data, list) else slots_data.get("slots", [])

    for slot in items:
        # Check availability
        spaces = slot.get("spaces_remaining") or slot.get("remainingUses") or 0
        if spaces == 0:
            continue
        if not slot.get("available", True):
            continue

        # Parse start/end time — could be ISO string or OpenActive format
        raw_start = slot.get("start_date") or slot.get("startDate") or ""
        raw_end = slot.get("end_date") or slot.get("endDate") or ""

        try:
            dt_start = datetime.fromisoformat(raw_start.replace("Z", "+00:00"))
            dt_end = datetime.fromisoformat(raw_end.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            continue

        s_min = dt_start.hour * 60 + dt_start.minute
        e_min = dt_end.hour * 60 + dt_end.minute

        if s_min < start_min or e_min > end_min:
            continue

        # Price — check multiple field names
        offers = slot.get("offers") or slot.get("prices") or []
        cost = 0
        if offers:
            if isinstance(offers[0], dict):
                cost = (offers[0].get("price") or offers[0].get("cost") or
                        offers[0].get("Price") or 0)
        else:
            cost = slot.get("price") or slot.get("cost") or 0

        court_name = slot.get("court_name") or slot.get("resource_name") or "Court"

        available.append({
            "court_name": court_name,
            "start": dt_start.strftime("%H:%M"),
            "end": dt_end.strftime("%H:%M"),
            "cost": float(cost),
            "lighting": False,
        })

    return available


def get_better_availability(venues, date_str, start_time=None, end_time=None):
    """
    Fetch availability for Better venues concurrently.

    Args:
        venues: List of Better venue dicts (with slug, activity_slug)
        date_str: Date in 'YYYY-MM-DD' format
        start_time: Optional earliest time as 'HH:MM'
        end_time: Optional latest time as 'HH:MM'

    Returns:
        List of dicts: {venue, slots} — same format as ClubSpark results
    """
    results = []

    def _fetch_one(venue):
        slots_data = fetch_better_slots(venue["slug"], venue["activity_slug"], date_str)
        slots = parse_better_slots(slots_data, start_time, end_time)
        return venue, slots

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(_fetch_one, v): v for v in venues}
        for future in as_completed(futures):
            venue, slots = future.result()
            results.append({
                "venue": venue,
                "slots": sorted(slots, key=lambda s: (s["court_name"], s["start"])),
            })

    results.sort(key=lambda r: r["venue"].get("distance_miles", 999))
    return results
