"""
Better.org (GLL) API client for fetching tennis court availability.

API discovery via browser DevTools (March 2026):
  - Requires headers: Origin/Referer from bookings.better.org.uk
  - Categories: GET /api/activities/venue/{slug}/categories
  - Tennis children: GET /api/activities/venue/{slug}/categories/{parent-slug}
  - Times: GET /api/activities/venue/{slug}/activity/{leaf-slug}/times?date=YYYY-MM-DD
  - Booking URL: https://bookings.better.org.uk/location/{slug}/{parent-slug}/{date}/by-time

Response format for /times:
  {data: [{starts_at: {format_24_hour: "07:00"}, ends_at: {format_24_hour: "08:00"},
           price: {formatted_amount: "£14.85"}, spaces: 2,
           action_to_show: {status: "BOOK"|"SOLD_OUT"|"LOGIN"}, name: "...", ...}]}
"""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BETTER_ADMIN = "https://better-admin.org.uk"
BOOKING_BASE = "https://bookings.better.org.uk"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Origin": BOOKING_BASE,
    "Referer": f"{BOOKING_BASE}/",
}


def _time_to_minutes(time_str):
    h, m = map(int, time_str.split(":"))
    return h * 60 + m


def fetch_tennis_slugs(venue_slug):
    """
    Discover the tennis activity slugs for a venue.
    Returns (parent_slug, [leaf_slug, ...]) or (None, []) if no tennis.
    """
    try:
        resp = requests.get(
            f"{BETTER_ADMIN}/api/activities/venue/{venue_slug}/categories",
            headers=HEADERS, timeout=10)
        resp.raise_for_status()
        cats = resp.json().get("data", [])
    except Exception:
        return None, []

    tennis_cat = next(
        (c for c in cats if "tennis" in c.get("slug", "") or
         "tennis" in c.get("name", "").lower()), None)
    if not tennis_cat:
        return None, []

    parent_slug = tennis_cat["slug"]

    if tennis_cat.get("has_children"):
        try:
            resp2 = requests.get(
                f"{BETTER_ADMIN}/api/activities/venue/{venue_slug}/categories/{parent_slug}",
                headers=HEADERS, timeout=10)
            resp2.raise_for_status()
            children = resp2.json().get("data", {}).get("children", [])
            # Exclude add-on activities (e.g. "additional-players")
            leaf_slugs = [
                c["slug"] for c in children
                if not c.get("has_children") and "additional" not in c["slug"]
            ]
        except Exception:
            leaf_slugs = [parent_slug]
    else:
        leaf_slugs = [parent_slug]

    return parent_slug, leaf_slugs


def fetch_better_times(venue_slug, activity_slug, date_str):
    """
    Fetch available time slots for one leaf tennis activity.
    Returns list of raw slot dicts, or [] on error.

    Note: the API returns data as a list for future dates but as a dict
    (keyed by index string "0", "1", ...) for today's date. We normalise both.
    """
    url = f"{BETTER_ADMIN}/api/activities/venue/{venue_slug}/activity/{activity_slug}/times"
    try:
        resp = requests.get(url, params={"date": date_str}, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        if isinstance(data, dict):
            data = list(data.values())
        return data
    except Exception:
        return []


def parse_better_times(times_data, court_name, start_time=None, end_time=None):
    """
    Parse Better /times response into our standard slot format.
    Filters by time window and only includes slots with available spaces.
    """
    start_min = _time_to_minutes(start_time) if start_time else 0
    end_min = _time_to_minutes(end_time) if end_time else 1440

    slots = []
    for t in times_data:
        if t.get("spaces", 0) == 0:
            continue
        status = (t.get("action_to_show") or {}).get("status", "")
        if status == "SOLD_OUT":
            continue

        start = t.get("starts_at", {}).get("format_24_hour", "")
        end = t.get("ends_at", {}).get("format_24_hour", "")
        if not start or not end:
            continue

        s_min = _time_to_minutes(start)
        e_min = _time_to_minutes(end)
        if s_min < start_min or e_min > end_min:
            continue

        price_str = t.get("price", {}).get("formatted_amount", "")
        try:
            cost = float(price_str.replace("£", "").replace(",", "").strip())
        except (ValueError, AttributeError):
            cost = 0.0

        name = t.get("name", court_name)
        lighting = "floodlit" in name.lower() or "flood" in name.lower()

        slots.append({
            "court_name": name,
            "start": start,
            "end": end,
            "cost": cost,
            "lighting": lighting,
        })

    return slots


def get_better_availability(venues, date_str, start_time=None, end_time=None):
    """
    Fetch availability for a list of Better.org venues concurrently.

    Each venue dict must have: slug, booking_slug, tennis_slugs (list), name, borough,
    distance_miles, source="better".

    For venues without pre-seeded tennis_slugs, auto-discovers them first.

    Returns: list of {venue, slots} dicts, same format as ClubSpark results.
    """
    results = []

    def _fetch_one(venue):
        slug = venue["slug"]
        tennis_slugs = venue.get("tennis_slugs") or []
        booking_slug = venue.get("booking_slug") or "tennis-activities"

        # Auto-discover if not pre-seeded
        if not tennis_slugs:
            booking_slug, tennis_slugs = fetch_tennis_slugs(slug)
            if not tennis_slugs:
                return venue, []

        all_slots = []
        for activity_slug in tennis_slugs:
            times = fetch_better_times(slug, activity_slug, date_str)
            all_slots.extend(parse_better_times(times, activity_slug, start_time, end_time))

        return venue, sorted(all_slots, key=lambda s: (s["court_name"], s["start"]))

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(_fetch_one, v): v for v in venues}
        for future in as_completed(futures):
            venue, slots = future.result()
            # Build booking URL
            booking_slug = venue.get("booking_slug", "tennis-activities")
            booking_url = f"{BOOKING_BASE}/location/{venue['slug']}/{booking_slug}/{date_str}/by-time"
            results.append({
                "venue": {**venue, "booking_url": booking_url},
                "slots": slots,
            })

    results.sort(key=lambda r: r["venue"].get("distance_miles", 999))
    return results
