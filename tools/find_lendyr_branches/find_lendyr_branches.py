from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Optional
from pydantic import BaseModel

BRANCHES = [
    {"name": "San Francisco - Main", "address": "124 2nd St", "city": "San Francisco", "state": "CA", "zip": "94105", "lat": 37.7879, "lng": -122.3974},
    {"name": "San Francisco - Sunset", "address": "1405 Noriega St", "city": "San Francisco", "state": "CA", "zip": "94122", "lat": 37.7534, "lng": -122.4871},
    {"name": "Daly City", "address": "362 Gellert Blvd", "city": "Daly City", "state": "CA", "zip": "94015", "lat": 37.6879, "lng": -122.4702},
    {"name": "Berkeley", "address": "2033 Kala Bagai Way", "city": "Berkeley", "state": "CA", "zip": "94704", "lat": 37.8716, "lng": -122.2727},
    {"name": "Oakland", "address": "360 22nd St", "city": "Oakland", "state": "CA", "zip": "94612", "lat": 37.8126, "lng": -122.2644},
    {"name": "Oakland City Center", "address": "1200 Clay St, Suite 130", "city": "Oakland", "state": "CA", "zip": "94612", "lat": 37.8044, "lng": -122.2712},
    {"name": "San Bruno", "address": "1050 Admiral Ct, Suite F", "city": "San Bruno", "state": "CA", "zip": "94066", "lat": 37.6305, "lng": -122.4111},
    {"name": "Hayward", "address": "24703 Amador St", "city": "Hayward", "state": "CA", "zip": "94545", "lat": 37.6688, "lng": -122.0808},
    {"name": "Lafayette", "address": "3498 Mount Diablo Blvd, Suite A", "city": "Lafayette", "state": "CA", "zip": "94549", "lat": 37.8858, "lng": -122.1180},
    {"name": "Fremont", "address": "5166 Mowry Ave", "city": "Fremont", "state": "CA", "zip": "94538", "lat": 37.5485, "lng": -121.9886},
    {"name": "Walnut Creek", "address": "1790 N Broadway", "city": "Walnut Creek", "state": "CA", "zip": "94596", "lat": 37.9101, "lng": -122.0652},
    {"name": "Concord", "address": "1390 Willow Pass Rd, Suite 100", "city": "Concord", "state": "CA", "zip": "94520", "lat": 37.9780, "lng": -122.0311},
    {"name": "San Mateo", "address": "51 Bovet Rd", "city": "San Mateo", "state": "CA", "zip": "94402", "lat": 37.5630, "lng": -122.3255},
    {"name": "Livermore", "address": "2245 Las Positas Rd", "city": "Livermore", "state": "CA", "zip": "94551", "lat": 37.6819, "lng": -121.7680},
    {"name": "Brentwood", "address": "5601 Lone Tree Way, Suite T-110", "city": "Brentwood", "state": "CA", "zip": "94513", "lat": 37.9318, "lng": -121.6957},
    {"name": "Sacramento", "address": "2425 Fair Oaks Blvd, Suite 6", "city": "Sacramento", "state": "CA", "zip": "95825", "lat": 38.5816, "lng": -121.4944},
    {"name": "Castro Valley", "address": "4055 E Castro Valley Blvd", "city": "Castro Valley", "state": "CA", "zip": "94552", "lat": 37.6941, "lng": -122.0858},
    {"name": "Redwood City", "address": "1105 Veterans Blvd", "city": "Redwood City", "state": "CA", "zip": "94063", "lat": 37.4852, "lng": -122.2364},
    {"name": "Milpitas", "address": "1351 McCandless Dr", "city": "Milpitas", "state": "CA", "zip": "95035", "lat": 37.4323, "lng": -121.8996},
    {"name": "Novato", "address": "112 Vintage Way, Suite C1", "city": "Novato", "state": "CA", "zip": "94945", "lat": 38.1074, "lng": -122.5697},
    {"name": "Sunnyvale", "address": "332 W El Camino Real", "city": "Sunnyvale", "state": "CA", "zip": "94087", "lat": 37.3688, "lng": -122.0363},
    {"name": "Pleasanton", "address": "4515 Rosewood Dr, Suite 800", "city": "Pleasanton", "state": "CA", "zip": "94588", "lat": 37.6624, "lng": -121.8747},
    {"name": "Dublin", "address": "3 Park Pl", "city": "Dublin", "state": "CA", "zip": "94588", "lat": 37.7022, "lng": -121.9358},
    {"name": "San Ramon", "address": "6000 Bollinger Canyon Rd, Suite 1612", "city": "San Ramon", "state": "CA", "zip": "94583", "lat": 37.7799, "lng": -121.9780},
    {"name": "Danville", "address": "310 Hartz Ave", "city": "Danville", "state": "CA", "zip": "94526", "lat": 37.8219, "lng": -121.9999},
    {"name": "Campbell", "address": "1790 S Bascom Ave, Suite 110", "city": "Campbell", "state": "CA", "zip": "95008", "lat": 37.2872, "lng": -121.9400},
    {"name": "Santa Rosa", "address": "1965 Cleveland Ave", "city": "Santa Rosa", "state": "CA", "zip": "95401", "lat": 38.4405, "lng": -122.7144},
    {"name": "Rohnert Park", "address": "985 Golf Course Dr", "city": "Rohnert Park", "state": "CA", "zip": "94928", "lat": 38.3396, "lng": -122.7011},
    {"name": "Roseville", "address": "5040 Foothills Blvd", "city": "Roseville", "state": "CA", "zip": "95747", "lat": 38.7521, "lng": -121.2880},
    {"name": "Citrus Heights", "address": "6100 Birdcage St, Suite 125", "city": "Citrus Heights", "state": "CA", "zip": "95610", "lat": 38.7071, "lng": -121.2810},
    {"name": "Elk Grove", "address": "9121 E Stockton Blvd", "city": "Elk Grove", "state": "CA", "zip": "95624", "lat": 38.4088, "lng": -121.3716},
    {"name": "Folsom", "address": "1300 E Bidwell St, Suite 155", "city": "Folsom", "state": "CA", "zip": "95630", "lat": 38.6779, "lng": -121.1761},
    {"name": "San Leandro", "address": "15100 Hesperian Blvd", "city": "San Leandro", "state": "CA", "zip": "94578", "lat": 37.7249, "lng": -122.1561},
    {"name": "San Jose - Almaden", "address": "5185 Cherry Ave, Suite 50", "city": "San Jose", "state": "CA", "zip": "95118", "lat": 37.2358, "lng": -121.8963},
    {"name": "Fairfield", "address": "3101 Travis Blvd, Suite A", "city": "Fairfield", "state": "CA", "zip": "94534", "lat": 38.2494, "lng": -122.0400},
    {"name": "Santa Clara", "address": "2654 El Camino Real", "city": "Santa Clara", "state": "CA", "zip": "95051", "lat": 37.3541, "lng": -121.9552},
]


class Branch(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zip: str
    lat: float
    lng: float


class BranchSearchResult(BaseModel):
    branches: list[Branch]
    total: int
    query: str


@tool(
    name="find_lendyr_branches",
    display_name="Find Lendyr Branches",
    description="Search for Lendyr Bank branch locations by city, ZIP code, or region. Returns branch names, addresses, and GPS coordinates suitable for map display. Pass 'all' to retrieve every branch.",
)
def find_lendyr_branches(location: str) -> BranchSearchResult:
    """Search for Lendyr Bank branches by city, ZIP code, or region.

    Args:
        location (str): The city name, ZIP code, or region to search for (e.g. 'Oakland',
            '94612', 'East Bay'). Pass 'all' to return all branches.

    Returns:
        BranchSearchResult: A list of matching branches with name, address, and GPS coordinates.
    """
    query = location.strip().lower()

    if query == "all":
        matches = BRANCHES
    else:
        east_bay = {"oakland", "berkeley", "hayward", "fremont", "san leandro",
                    "castro valley", "livermore", "pleasanton", "dublin",
                    "san ramon", "danville", "walnut creek", "concord", "lafayette"}
        south_bay = {"san jose", "campbell", "santa clara", "sunnyvale", "milpitas"}
        north_bay = {"novato", "santa rosa", "rohnert park"}
        sacramento_area = {"sacramento", "roseville", "citrus heights", "elk grove",
                           "folsom", "brentwood", "fairfield"}

        region_map = {
            "east bay": east_bay,
            "south bay": south_bay,
            "north bay": north_bay,
            "sacramento": sacramento_area,
            "bay area": east_bay | south_bay | north_bay | {"san francisco", "daly city",
                                                             "san bruno", "san mateo",
                                                             "redwood city"},
        }

        if query in region_map:
            target_cities = region_map[query]
            matches = [b for b in BRANCHES if b["city"].lower() in target_cities]
        else:
            matches = [
                b for b in BRANCHES
                if query in b["city"].lower()
                or query in b["zip"]
                or query in b["name"].lower()
            ]

    return BranchSearchResult(
        branches=[Branch(**b) for b in matches],
        total=len(matches),
        query=location,
    )
