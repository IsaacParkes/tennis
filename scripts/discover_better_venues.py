"""
Check a Better.org venue slug for tennis activities.

Usage:
    python scripts/discover_better_venues.py <slug>
    python scripts/discover_better_venues.py britannia-leisure-centre
    python scripts/discover_better_venues.py --all   # check a built-in list of London GLL venues
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from better_scraper import fetch_tennis_slugs

# Common GLL leisure centre slugs in London (not exhaustive)
CANDIDATE_SLUGS = [
    "britannia-leisure-centre",
    "hackney-parks",
    "islington-tennis-centre",
    "clissold-leisure-centre",
    "better-gym-finsbury-park",
    "archway-leisure-centre",
    "tottenham-green-leisure-centre",
    "park-road-leisure-centre",
    "walthamstow-leisure-centre",
    "leyton-leisure-centre",
    "poplar-baths-leisure-centre",
    "york-hall-leisure-centre",
    "mile-end-leisure-centre",
]


def check_venue(slug):
    parent, leafs = fetch_tennis_slugs(slug)
    if leafs:
        print(f"  \u2713 {slug}: parent={parent}, leafs={leafs}")
    else:
        print(f"  \u2717 {slug}: no tennis")
    return parent, leafs


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    if sys.argv[1] == "--all":
        print("Checking candidate Better.org venues for tennis...\n")
        for slug in CANDIDATE_SLUGS:
            check_venue(slug)
    else:
        slug = sys.argv[1]
        print(f"Checking {slug}...")
        parent, leafs = check_venue(slug)
        if leafs:
            print(f"\nAdd to BETTER_VENUES in courts.py:")
            print(f'    {{"name": "???", "slug": "{slug}", "booking_slug": "{parent}",')
            print(f'     "tennis_slugs": {leafs}, "borough": "???",')
            print(f'     "lat": 0.0, "lng": 0.0, "source": "better"}}')
