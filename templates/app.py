from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_weather(city, country):
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 100},
        timeout=10,
    ).json()
    results = geo.get("results", [])
    if country:
        results = [p for p in results
                   if p.get("country", "").lower() == country.lower()]
    if not results:
        return None
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
    return {"place": place, "now": weather["current"]}

@app.route("/")
def home():
    city = request.args.get("city", "").strip()
    country = request.args.get("country", "").strip()
    data = None
    error = None
    if city:
        try:
            data = get_weather(city, country)
            if data is None:
                error = "City not found"
        except requests.exceptions.RequestException:
            error = "Network problem. Check your internet."
    return render_template("index.html", data=data, error=error)

if __name__ == "__main__":
    app.run()