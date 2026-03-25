"""
Discover Better.org (GLL) tennis venues in London from the OpenActive RPDE feed.
Run this script to refresh the BETTER_VENUES list in courts.py.

Usage:
    python scripts/discover_better_venues.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from better_scraper import discover_london_tennis_venues

if __name__ == "__main__":
    print("Fetching Better.org OpenActive FacilityUse feed...")
    venues = discover_london_tennis_venues()

    if not venues:
        print("No venues found (feed may be down). Try again later.")
        sys.exit(1)

    print(f"\nFound {len(venues)} London tennis venues on Better.org:\n")
    print("BETTER_VENUES = [")
    for v in venues:
        print(f"    # {v['borough']}")
        print(f"    {{")
        print(f'        "name": "{v["name"]}",')
        print(f'        "slug": "{v["slug"]}",')
        print(f'        "activity_slug": "{v["activity_slug"]}",')
        print(f'        "borough": "{v["borough"]}",')
        print(f'        "lat": {v["lat"]},')
        print(f'        "lng": {v["lng"]},')
        print(f'        "source": "better",')
        print(f"    }},")
    print("]")
