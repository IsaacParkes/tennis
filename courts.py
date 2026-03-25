"""
Tennis court venues in London.

VENUES     — ClubSpark (LTA) courts, booked via clubspark.lta.org.uk
BETTER_VENUES — Better.org (GLL) courts, booked via bookings.better.org.uk

All venues have lat/lng for dynamic distance calculation from any user location.
Better venues are discovered from the OpenActive FacilityUse RPDE feed and
supplemented here with a confirmed seed list.
Run `python scripts/discover_better_venues.py` to refresh the full list.
"""

VENUES = [
    # Haringey
    {"name": "Finsbury Park", "slug": "FinsburyPark", "borough": "Haringey", "lat": 51.5644, "lng": -0.1013},
    {"name": "Downhills Park", "slug": "downhillsparktennisclub", "borough": "Haringey", "lat": 51.5847, "lng": -0.0893},
    {"name": "Down Lane Park", "slug": "DownLanePark", "borough": "Haringey", "lat": 51.5908, "lng": -0.0644},
    {"name": "Chestnuts Park", "slug": "ChestnutsPark", "borough": "Haringey", "lat": 51.5912, "lng": -0.0776},
    {"name": "Stationers Park", "slug": "stationerspark", "borough": "Haringey", "lat": 51.5958, "lng": -0.1078},
    {"name": "Priory Park", "slug": "PrioryPark2", "borough": "Haringey", "lat": 51.5994, "lng": -0.1187},
    {"name": "Chapmans Green", "slug": "chapmansgreen", "borough": "Haringey", "lat": 51.6018, "lng": -0.0700},
    {"name": "Bruce Castle Park", "slug": "BruceCastlePark", "borough": "Haringey", "lat": 51.5990, "lng": -0.0707},
    {"name": "Albert Road Rec (OR Tambo)", "slug": "PavilionTennis", "borough": "Haringey", "lat": 51.5858, "lng": -0.0705},

    # Hackney
    {"name": "Clissold Park", "slug": "ClissoldParkHackney", "borough": "Hackney", "lat": 51.5617, "lng": -0.0826},
    {"name": "Hackney Downs", "slug": "HackneyDowns", "borough": "Hackney", "lat": 51.5567, "lng": -0.0540},
    {"name": "London Fields", "slug": "LondonFieldsPark", "borough": "Hackney", "lat": 51.5413, "lng": -0.0586},
    {"name": "Springfield Park", "slug": "SpringfieldPark", "borough": "Hackney", "lat": 51.5690, "lng": -0.0487},
    {"name": "Spring Hill Rec", "slug": "SpringHillParkTennis", "borough": "Hackney", "lat": 51.5702, "lng": -0.0467},
    {"name": "Millfields Park", "slug": "MillfieldsParkMiddlesex", "borough": "Hackney", "lat": 51.5578, "lng": -0.0493},

    # Islington
    {"name": "Highbury Fields", "slug": "HighburyFields", "borough": "Islington", "lat": 51.5543, "lng": -0.0990},
    {"name": "Highbury Grove", "slug": "HighburyGrove", "borough": "Islington", "lat": 51.5514, "lng": -0.0992},

    # Enfield
    {"name": "Pymmes Park", "slug": "PymmesPark", "borough": "Enfield", "lat": 51.6155, "lng": -0.0791},
    {"name": "Broomfield Park", "slug": "BroomfieldPark", "borough": "Enfield", "lat": 51.6097, "lng": -0.1125},

    # Waltham Forest
    {"name": "Lloyd Park", "slug": "LloydPark", "borough": "Waltham Forest", "lat": 51.5845, "lng": -0.0135},
    {"name": "Walthamstow Wetlands", "slug": "WalthamstowWetlands", "borough": "Waltham Forest", "lat": 51.5900, "lng": -0.0229},

    # Tower Hamlets / East London
    {"name": "Victoria Park", "slug": "VictoriaParkTennis", "borough": "Tower Hamlets", "lat": 51.5363, "lng": -0.0396},

    # Camden
    {"name": "Regent's Park", "slug": "RegentsParkTennis", "borough": "Camden", "lat": 51.5269, "lng": -0.1541},

    # Southwark / Lewisham
    {"name": "Dulwich Park", "slug": "DulwichPark", "borough": "Southwark", "lat": 51.4510, "lng": -0.0852},
]

# Better.org (GLL) tennis venues.
# Slugs and coordinates sourced from the OpenActive FacilityUse RPDE feed.
# Expand this list by running: python scripts/discover_better_venues.py
BETTER_VENUES = [
    # Hackney
    {
        "name": "Britannia Leisure Centre",
        "slug": "britannia-leisure-centre",
        "activity_slug": "tennis-pay-and-play",
        "borough": "Hackney",
        "lat": 51.5384,
        "lng": -0.0830,
        "source": "better",
    },
    # Islington
    {
        "name": "Islington Tennis Centre",
        "slug": "islington-tennis-centre",
        "activity_slug": "tennis-pay-and-play",
        "borough": "Islington",
        "lat": 51.5505,
        "lng": -0.0973,
        "source": "better",
    },
    {
        "name": "Finsbury Leisure Centre",
        "slug": "finsbury-leisure-centre",
        "activity_slug": "tennis-pay-and-play",
        "borough": "Islington",
        "lat": 51.5259,
        "lng": -0.0989,
        "source": "better",
    },
    # Newham / Olympic Park
    {
        "name": "Copper Box Arena",
        "slug": "copper-box-arena",
        "activity_slug": "tennis-pay-and-play",
        "borough": "Newham",
        "lat": 51.5429,
        "lng": -0.0138,
        "source": "better",
    },
    # Lewisham
    {
        "name": "Ladywell Arena",
        "slug": "ladywell-arena",
        "activity_slug": "tennis-pay-and-play",
        "borough": "Lewisham",
        "lat": 51.4584,
        "lng": -0.0200,
        "source": "better",
    },
    # Southwark
    {
        "name": "Tanner Street Park",
        "slug": "tanner-street-park",
        "activity_slug": "tennis-pay-and-play",
        "borough": "Southwark",
        "lat": 51.5010,
        "lng": -0.0786,
        "source": "better",
    },
]
