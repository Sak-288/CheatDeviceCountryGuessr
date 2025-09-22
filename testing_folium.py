def add_country_circle(country_name, distance_km):
    import folium
    import json
    from geopy.geocoders import Nominatim
    from pathlib import Path
    import random as rd

    geolocator = Nominatim(user_agent="country_center")
    STATE_FILE = Path("circles.json")

    # Load previous state
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            circles = json.load(f)
    else:
        circles = []

    # Append new circle
    circles.append({"country": country_name, "distance": distance_km})

    # Save state back
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(circles, f, indent=2)

    # Rebuild map
    m = folium.Map(location=[20, 0], zoom_start=2)

    for c in circles:
        location = geolocator.geocode(c["country"])
        if not location:
            continue
        folium.Circle(
            location=[location.latitude, location.longitude],
            radius=c["distance"] * 1000,
            color=f"rgb({rd.randint(0, 255)}, {rd.randint(0, 255)}, {rd.randint(0, 255)})",
            fill=True,
            fill_opacity=0.2,
        ).add_to(m)
        folium.Marker([location.latitude, location.longitude], popup=c["country"]).add_to(m)

    m.save("map.html")
    print(f"✅ Added {country_name} ({distance_km} km). Map updated.")

