"""
Tennis court venues in London that use the ClubSpark (LTA) booking system.
Each venue has lat/lng for dynamic distance calculation from any user location.
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
