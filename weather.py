# Python Weather App

Shows live temperature, wind speed and humidity for any city.

## Features
- Search by city and optional country
- Check multiple cities in a loop
- Handles unknown cities and network errors

## How to run
    pip install requests
    python weather.py

Weather data by [Open-Meteo](https://open-meteo.com/)


import requests

while True:
    city = input("Enter city (or q to quit): ").strip()

    if city.lower() == "q":
        print("Goodbye!")
        break

    country = input("Enter country (Enter to skip): ").strip()

    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 100},
            timeout=10,
        ).json()

        results = geo.get("results", [])

        if country:
            results = [
                p for p in results
                if p.get("country", "").lower() == country.lower()
            ]

        if not results:
            print("City not found")
            continue

        place = results[0]

        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,wind_speed_10m,relative_humidity_2m",
            },
            timeout=10,
        ).json()

        now = weather["current"]
        print(place["name"], "-", place.get("country", ""))
        print("Temperature:", now["temperature_2m"], "°C")
        print("Wind:", now["wind_speed_10m"], "km/h")
        print("Humidity:", now["relative_humidity_2m"], "%")

    except requests.exceptions.RequestException:
        print("Network problem. Check your internet.")   