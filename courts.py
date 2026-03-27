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

    # Enfield
    {"name": "Pymmes Park", "slug": "PymmesPark", "borough": "Enfield", "lat": 51.6155, "lng": -0.0791},
    {"name": "Broomfield Park", "slug": "BroomfieldPark", "borough": "Enfield", "lat": 51.6097, "lng": -0.1125},

    # Waltham Forest
    {"name": "Lloyd Park", "slug": "LloydPark", "borough": "Waltham Forest", "lat": 51.5845, "lng": -0.0135},

    # Tower Hamlets / East London
    {"name": "Victoria Park", "slug": "VictoriaParkTennis", "borough": "Tower Hamlets", "lat": 51.5363, "lng": -0.0396},

    # Southwark
    {"name": "Dulwich Park",               "slug": "DulwichPark",                       "borough": "Southwark",  "lat": 51.4510, "lng": -0.0852},
    {"name": "Burgess Park",               "slug": "BurgessParkSouthwark",              "borough": "Southwark",  "lat": 51.4816, "lng": -0.0899},
    {"name": "Southwark Park",             "slug": "SouthwarkPark",                     "borough": "Southwark",  "lat": 51.4922, "lng": -0.0648},
    {"name": "Tanner Street Park",         "slug": "TannerStPark",                      "borough": "Southwark",  "lat": 51.4993, "lng": -0.0811},
    {"name": "Geraldine Mary Harmsworth",  "slug": "GeraldineMaryHarmsworth",           "borough": "Southwark",  "lat": 51.4969, "lng": -0.1071},

    # Lambeth
    {"name": "Brockwell Park",             "slug": "BrockwellPark",                     "borough": "Lambeth",    "lat": 51.4464, "lng": -0.1068},
    {"name": "Clapham Common",             "slug": "ClaphamCommon",                     "borough": "Lambeth",    "lat": 51.4614, "lng": -0.1412},
    {"name": "Kennington Park",            "slug": "KenningtonPark",                    "borough": "Lambeth",    "lat": 51.4851, "lng": -0.1109},
    {"name": "Archbishop's Park",          "slug": "archbishopsparklambethnorth",        "borough": "Lambeth",    "lat": 51.4983, "lng": -0.1136},
    {"name": "Streatham Common",           "slug": "therookery",                        "borough": "Lambeth",    "lat": 51.4244, "lng": -0.1337},

    # Lewisham
    {"name": "Ladywell Fields",            "slug": "LadywellFields",                    "borough": "Lewisham",   "lat": 51.4562, "lng": -0.0189},
    {"name": "Catford Bridge",             "slug": "CatfordBridge",                     "borough": "Lewisham",   "lat": 51.4449, "lng": -0.0197},
    {"name": "Manor House Gardens",        "slug": "ManorHouseGds",                     "borough": "Lewisham",   "lat": 51.4516, "lng": -0.0108},
    {"name": "Chinbrook Meadows",          "slug": "ChinbrookPark",                     "borough": "Lewisham",   "lat": 51.4285, "lng": -0.0122},

    # Greenwich
    {"name": "Greenwich Park",             "slug": "GreenwichPark",                     "borough": "Greenwich",  "lat": 51.4769, "lng":  0.0000},
    {"name": "Blackheath",                 "slug": "BlackheathPark",                    "borough": "Greenwich",  "lat": 51.4659, "lng":  0.0097},
    {"name": "Plumstead Common",           "slug": "PlumsteadCommon",                   "borough": "Greenwich",  "lat": 51.4817, "lng":  0.0842},
    {"name": "Maryon Park",                "slug": "MarYonPark",                        "borough": "Greenwich",  "lat": 51.4875, "lng":  0.0288},
    {"name": "Eltham Park",                "slug": "ElthamPark",                        "borough": "Greenwich",  "lat": 51.4561, "lng":  0.0601},

    # Wandsworth
    {"name": "Battersea Park",             "slug": "BatterseaParkTennisCourts",         "borough": "Wandsworth", "lat": 51.4812, "lng": -0.1547},
    {"name": "Wandsworth Common",          "slug": "AllWinWandsworthCommonTennisCentre","borough": "Wandsworth", "lat": 51.4444, "lng": -0.1712},
    {"name": "Tooting Bec Common",         "slug": "AllWinTootingBecCommon",            "borough": "Wandsworth", "lat": 51.4350, "lng": -0.1561},
    {"name": "Spencer Park",               "slug": "SpencerPark",                       "borough": "Wandsworth", "lat": 51.4607, "lng": -0.1900},

    # Merton
    {"name": "Wimbledon Park",             "slug": "WimbledonPark",                     "borough": "Merton",     "lat": 51.4355, "lng": -0.2076},
    {"name": "Morden Park",                "slug": "MordenPark",                        "borough": "Merton",     "lat": 51.3939, "lng": -0.1987},
    {"name": "John Innes Park",            "slug": "JohnInnesParkMorden",               "borough": "Merton",     "lat": 51.4055, "lng": -0.1947},
    {"name": "Tamworth Recreation Ground", "slug": "TamworthRecreationGround",          "borough": "Merton",     "lat": 51.4003, "lng": -0.1710},
]

# Better.org (GLL) tennis venues.
# Confirmed via live API checks March 2026. tennis_slugs are the leaf-level
# activity slugs for the /times endpoint; booking_slug is the parent category
# used in the booking URL.
BETTER_VENUES = [
    # Hackney — confirmed has tennis-activities with outdoor courts
    {
        "name": "Britannia Leisure Centre",
        "slug": "britannia-leisure-centre",
        "booking_slug": "tennis-activities",
        "tennis_slugs": ["tennis-court-outdoor"],
        "borough": "Hackney",
        "lat": 51.5342,
        "lng": -0.0830,
        "source": "better",
    },
    # Hackney — GLL-managed outdoor parks courts (Haggerston Park and others), £8/hr
    {
        "name": "Hackney Parks (GLL)",
        "slug": "hackney-parks",
        "booking_slug": "tennis-activities",
        "tennis_slugs": ["tennis-court-outdoor"],
        "borough": "Hackney",
        "lat": 51.5338,
        "lng": -0.0771,
        "source": "better",
    },
    # Islington — confirmed has outdoor + indoor courts
    {
        "name": "Islington Tennis Centre",
        "slug": "islington-tennis-centre",
        "booking_slug": "tennis-activities",
        "tennis_slugs": ["tennis-court-outdoor", "tennis-court-indoor"],
        "borough": "Islington",
        "lat": 51.5505,
        "lng": -0.0973,
        "source": "better",
    },
]
