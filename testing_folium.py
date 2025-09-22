import folium
from geopy.geocoders import Nominatim

def draw_country_circle(country_name, distance_km, output_file="map.html"):
    # Get country center (lat, lon)
    geolocator = Nominatim(user_agent="country_center")
    location = geolocator.geocode(country_name)
    if not location:
        raise ValueError(f"Could not find country: {country_name}")

    lat, lon = location.latitude, location.longitude

    # Create map centered on country
    m = folium.Map(location=[lat, lon], zoom_start=4)

    # Add circle with given radius
    folium.Circle(
        location=[lat, lon],
        radius=distance_km * 1000,  # folium uses meters
        color="red",
        fill=True,
        fill_opacity=0.2,
    ).add_to(m)

    # Add marker for country center
    folium.Marker([lat, lon], popup=country_name).add_to(m)

    # Save to HTML
    m.save(output_file)
    print(f"Map saved to {output_file}")