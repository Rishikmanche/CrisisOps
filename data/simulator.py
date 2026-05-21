import random
import datetime

CITY_LAT = 17.3850
CITY_LON = 78.4867

# Real-world scenarios (Some serious, some noise)
RAW_MESSAGES = [
    "URGENT: Massive fire broke out at the chemical factory in Industrial Area!",
    "Water levels rising rapidly near the Hussain Sagar lake, roads blocked.",
    "Terrible car crash on the Outer Ring Road, multiple injuries.",
    "Anyone want to buy a used bike? DM me.",
    "Just felt a huge tremor! Was that an earthquake?? Walls are cracking!",
    "My dog is barking nicely today.",
    "Medical emergency at the Metro Station, person collapsed!",
    "Heavy smog in the city today, visibility is low."
]

LOCATIONS = ["Industrial Area", "Lake Side", "Ring Road", "City Center", "Metro Station", "Old Market"]

def generate_fake_report():
    raw_text = random.choice(RAW_MESSAGES)
    location = random.choice(LOCATIONS)
    
    # Random coordinates
    lat = CITY_LAT + random.uniform(-0.05, 0.05)
    lon = CITY_LON + random.uniform(-0.05, 0.05)
    
    return {
        "id": random.randint(1000, 9999),
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "raw_text": raw_text,
        "location_name": location,
        "lat": lat,
        "lon": lon
    }