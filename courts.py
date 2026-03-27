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
    # Finsbury Park: courts in SE corner near Seven Sisters Rd (globaltennisnetwork structured data)
    {"name": "Finsbury Park", "slug": "FinsburyPark", "borough": "Haringey", "lat": 51.5679, "lng": -0.1045},
    # Downhills Park: east side of park in Italian Gardens area (spintennisapp)
    {"name": "Downhills Park", "slug": "downhillsparktennisclub", "borough": "Haringey", "lat": 51.5895, "lng": -0.0933},
    # Down Lane Park: south of park (spintennisapp)
    {"name": "Down Lane Park", "slug": "DownLanePark", "borough": "Haringey", "lat": 51.5904, "lng": -0.0646},
    # Chestnuts Park: eastern half of park, St Ann's Road N15 (spintennisapp)
    {"name": "Chestnuts Park", "slug": "ChestnutsPark", "borough": "Haringey", "lat": 51.5818, "lng": -0.0887},
    # Stationers Park: Mayfield Road N8 (spintennisapp)
    {"name": "Stationers Park", "slug": "stationerspark", "borough": "Haringey", "lat": 51.5791, "lng": -0.1125},
    # Priory Park: Middle Lane N8, courts near Priory Road entrance (spintennisapp)
    {"name": "Priory Park", "slug": "PrioryPark2", "borough": "Haringey", "lat": 51.5852, "lng": -0.1252},
    # Chapmans Green: Perth Road N22 (not N17 — Wood Green area) (spintennisapp)
    {"name": "Chapmans Green", "slug": "chapmansgreen", "borough": "Haringey", "lat": 51.6013, "lng": -0.0983},
    # Bruce Castle Park: N17 (spintennisapp)
    {"name": "Bruce Castle Park", "slug": "BruceCastlePark", "borough": "Haringey", "lat": 51.5988, "lng": -0.0714},
    # OR Tambo Rec (Albert Rd): Durnsford Road N22 — NOT N15 (spintennisapp)
    {"name": "Albert Road Rec (OR Tambo)", "slug": "PavilionTennis", "borough": "Haringey", "lat": 51.6005, "lng": -0.1340},

    # Hackney
    # Clissold Park: courts by tennis pavilion, Queen Elizabeth's Walk N16 (OSM way 375067115 + spintennisapp)
    {"name": "Clissold Park", "slug": "ClissoldParkHackney", "borough": "Hackney", "lat": 51.5640, "lng": -0.0868},
    # Hackney Downs: Downs Park Road E5 (globaltennisnetwork structured data)
    {"name": "Hackney Downs", "slug": "HackneyDowns", "borough": "Hackney", "lat": 51.5530, "lng": -0.0603},
    # London Fields: Richmond Road opposite Navarino Road E8 (spintennisapp)
    {"name": "London Fields", "slug": "LondonFieldsPark", "borough": "Hackney", "lat": 51.5423, "lng": -0.0615},
    # Springfield Park: upper Clapton E5, near Springfield House (spintennisapp)
    {"name": "Springfield Park", "slug": "SpringfieldPark", "borough": "Hackney", "lat": 51.5709, "lng": -0.0595},
    # Spring Hill Rec: Spring Hill E5 (spintennisapp)
    {"name": "Spring Hill Rec", "slug": "SpringHillParkTennis", "borough": "Hackney", "lat": 51.5732, "lng": -0.0592},
    # Millfields Park: Chatsworth Road E5 (spintennisapp)
    {"name": "Millfields Park", "slug": "MillfieldsParkMiddlesex", "borough": "Hackney", "lat": 51.5599, "lng": -0.0476},

    # Enfield
    # Pymmes Park: Victoria Road N18 (spintennisapp)
    {"name": "Pymmes Park", "slug": "PymmesPark", "borough": "Enfield", "lat": 51.6171, "lng": -0.0667},
    # Broomfield Park: Aldermans Hill N13 (spintennisapp)
    {"name": "Broomfield Park", "slug": "BroomfieldPark", "borough": "Enfield", "lat": 51.6168, "lng": -0.1173},

    # Waltham Forest
    # Lloyd Park: Forest Road E17, courts to the right of main entrance (globaltennisnetwork)
    {"name": "Lloyd Park", "slug": "LloydPark", "borough": "Waltham Forest", "lat": 51.5923, "lng": -0.0201},

    # Tower Hamlets / East London
    # Victoria Park: E9, courts in western section (spintennisapp)
    {"name": "Victoria Park", "slug": "VictoriaParkTennis", "borough": "Tower Hamlets", "lat": 51.5407, "lng": -0.0391},

    # Southwark
    # Dulwich Park: College Road SE21, courts near Francis Peek Centre (spintennisapp)
    {"name": "Dulwich Park",               "slug": "DulwichPark",                       "borough": "Southwark",  "lat": 51.4454, "lng": -0.0776},
    # Burgess Park: near Addington Square, Camberwell SE5 (spintennisapp)
    {"name": "Burgess Park",               "slug": "BurgessParkSouthwark",              "borough": "Southwark",  "lat": 51.4815, "lng": -0.0924},
    # Southwark Park: west side near Jamaica Gate SE16 (spintennisapp)
    {"name": "Southwark Park",             "slug": "SouthwarkPark",                     "borough": "Southwark",  "lat": 51.4957, "lng": -0.0589},
    # Tanner Street Park: NE corner of park, SE1 (spintennisapp)
    {"name": "Tanner Street Park",         "slug": "TannerStPark",                      "borough": "Southwark",  "lat": 51.4999, "lng": -0.0812},
    # Geraldine Mary Harmsworth: St George's Road SE1 (spintennisapp)
    {"name": "Geraldine Mary Harmsworth",  "slug": "GeraldineMaryHarmsworth",           "borough": "Southwark",  "lat": 51.4960, "lng": -0.1084},

    # Lambeth
    # Brockwell Park: Herne Hill SE24, centre of park (spintennisapp)
    {"name": "Brockwell Park",             "slug": "BrockwellPark",                     "borough": "Lambeth",    "lat": 51.4528, "lng": -0.1032},
    # Clapham Common: Windmill Drive SW4, courts near bowling green (globaltennisnetwork)
    {"name": "Clapham Common",             "slug": "ClaphamCommon",                     "borough": "Lambeth",    "lat": 51.4541, "lng": -0.1510},
    # Kennington Park: Kennington Park Road SE11 (spintennisapp)
    {"name": "Kennington Park",            "slug": "KenningtonPark",                    "borough": "Lambeth",    "lat": 51.4843, "lng": -0.1106},
    # Archbishop's Park: Lambeth Palace Road SE1 (spintennisapp)
    {"name": "Archbishop's Park",          "slug": "archbishopsparklambethnorth",        "borough": "Lambeth",    "lat": 51.4955, "lng": -0.1164},
    # Streatham Common (The Rookery): Covington Way SW16 (spintennisapp)
    {"name": "Streatham Common",           "slug": "therookery",                        "borough": "Lambeth",    "lat": 51.4215, "lng": -0.1209},

    # Lewisham
    # Ladywell Fields: northern section, back of Lewisham Hospital SE13 (spintennisapp)
    {"name": "Ladywell Fields",            "slug": "LadywellFields",                    "borough": "Lewisham",   "lat": 51.4568, "lng": -0.0176},
    # Catford Bridge: SE6, Ladywell Fields South (spintennisapp slug: ladywell-fields-south-lewisham)
    {"name": "Catford Bridge",             "slug": "CatfordBridge",                     "borough": "Lewisham",   "lat": 51.4471, "lng": -0.0258},
    # Manor House Gardens: Manor Lane SE13 (spintennisapp)
    {"name": "Manor House Gardens",        "slug": "ManorHouseGds",                     "borough": "Lewisham",   "lat": 51.4579, "lng":  0.0040},
    # Chinbrook Meadows: Grove Park SE12 (spintennisapp — positive lng, east of meridian)
    {"name": "Chinbrook Meadows",          "slug": "ChinbrookPark",                     "borough": "Lewisham",   "lat": 51.4318, "lng":  0.0294},

    # Greenwich
    # Greenwich Park: near Rangers House, on/near meridian (OSM way 8879804 + spintennisapp)
    {"name": "Greenwich Park",             "slug": "GreenwichPark",                     "borough": "Greenwich",  "lat": 51.4746, "lng": -0.0007},
    # Blackheath: Chesterfield Walk SE10 (spintennisapp — near 0 longitude, not 0.0097)
    {"name": "Blackheath",                 "slug": "BlackheathPark",                    "borough": "Greenwich",  "lat": 51.4726, "lng": -0.0007},
    # Plumstead Common: Waverley Crescent SE18 (spintennisapp)
    {"name": "Plumstead Common",           "slug": "PlumsteadCommon",                   "borough": "Greenwich",  "lat": 51.4826, "lng":  0.0803},
    # Maryon Park: Cemetery Lane SE7 (spintennisapp)
    {"name": "Maryon Park",                "slug": "MarYonPark",                        "borough": "Greenwich",  "lat": 51.4897, "lng":  0.0432},
    # Eltham Park South: Glenesk Road SE9 (spintennisapp)
    {"name": "Eltham Park",                "slug": "ElthamPark",                        "borough": "Greenwich",  "lat": 51.4554, "lng":  0.0677},

    # Wandsworth
    # Battersea Park Millennium Arena: East Carriage Drive SW11 (spintennisapp)
    {"name": "Battersea Park",             "slug": "BatterseaParkTennisCourts",         "borough": "Wandsworth", "lat": 51.4818, "lng": -0.1534},
    # Wandsworth Common: Off Dorlcote Road SW18 (spintennisapp)
    {"name": "Wandsworth Common",          "slug": "AllWinWandsworthCommonTennisCentre","borough": "Wandsworth", "lat": 51.4527, "lng": -0.1701},
    # Tooting Bec Common: Dr Johnson Ave SW17 (spintennisapp)
    {"name": "Tooting Bec Common",         "slug": "AllWinTootingBecCommon",            "borough": "Wandsworth", "lat": 51.4341, "lng": -0.1488},
    # Spencer Park = Spencer Lawn Tennis Club: Fieldview/Burntwood Lane SW18 (spintennisapp)
    {"name": "Spencer Park",               "slug": "SpencerPark",                       "borough": "Wandsworth", "lat": 51.4414, "lng": -0.1775},

    # Merton
    # Wimbledon Park: Home Park Road SW19 (spintennisapp)
    {"name": "Wimbledon Park",             "slug": "WimbledonPark",                     "borough": "Merton",     "lat": 51.4359, "lng": -0.2027},
    # Morden Park: Links Avenue SM4, NE corner of park (spintennisapp)
    {"name": "Morden Park",                "slug": "MordenPark",                        "borough": "Merton",     "lat": 51.3982, "lng": -0.2014},
    # John Innes Park: Mostyn Road SW19 (spintennisapp)
    {"name": "John Innes Park",            "slug": "JohnInnesParkMorden",               "borough": "Merton",     "lat": 51.4093, "lng": -0.2065},
    # Tamworth Recreation Ground: London Road Mitcham CR4 (spintennisapp)
    {"name": "Tamworth Recreation Ground", "slug": "TamworthRecreationGround",          "borough": "Merton",     "lat": 51.4150, "lng": -0.1622},
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
