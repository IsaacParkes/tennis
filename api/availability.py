"""Vercel serverless function for tennis court availability."""

import json
import sys
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Allow imports from project root
sys.path.insert(0, os.getcwd())

from courts import VENUES, BETTER_VENUES
from scraper import get_availability, filter_by_radius
from better_scraper import get_better_availability

DEFAULT_LAT = 51.5805
DEFAULT_LNG = -0.0760
DEFAULT_RADIUS = 3.0


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        date_str = params.get("date", [None])[0]
        start_time = params.get("start_time", [None])[0]
        end_time = params.get("end_time", [None])[0]
        lat = params.get("lat", [None])[0]
        lng = params.get("lng", [None])[0]
        radius = params.get("radius", [None])[0]

        if not date_str:
            self._respond(400, {"error": "date is required"})
            return

        user_lat = float(lat) if lat else None
        user_lng = float(lng) if lng else None
        radius_miles = float(radius) if radius else None

        # ClubSpark venues
        clubspark_results = get_availability(
            VENUES, date_str, start_time, end_time,
            user_lat=user_lat, user_lng=user_lng, radius_miles=radius_miles,
        )

        # Better.org venues — filter by radius then fetch concurrently
        resolved_lat = user_lat if user_lat is not None else DEFAULT_LAT
        resolved_lng = user_lng if user_lng is not None else DEFAULT_LNG
        resolved_radius = radius_miles if radius_miles is not None else DEFAULT_RADIUS

        nearby_better = filter_by_radius(BETTER_VENUES, resolved_lat, resolved_lng, resolved_radius)
        better_results = get_better_availability(nearby_better, date_str, start_time, end_time)

        # Merge and re-sort by distance
        all_results = clubspark_results + better_results
        all_results.sort(key=lambda r: r["venue"].get("distance_miles", 999))

        self._respond(200, all_results)

    def _respond(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
