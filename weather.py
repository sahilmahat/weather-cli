import requests
from dotenv import load_dotenv
import argparse
import os

load_dotenv()

API_KEY=os.getenv("API_KEY")
BASE_URL= "https://api.openweathermap.org/data/2.5"

def get_current_weather(city):
    url = f"{BASE_URL}/weather"
    params ={
        "q": city,
        "appid":API_KEY,
        "units":"metric"
    }
    response= requests.get(url, params=params)
    if response.status_code == 404:
        print (f"City '{city}' not found. Check the spelling and try again.")
        exit (1)
    response.raise_for_status()
    return response.json()

def get_forecast(city):
    url=f"{BASE_URL}/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "cnt":9
    }
    response=requests.get(url, params=params)
    if response.status_code == 404:
        print (f"City '{city}' not found. Check the spelling and try again.")
        exit (1)
    response.raise_for_status()
    return response.json()

def display_current(data):
    name = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels= data["main"]["feels_like"]
    humidity= data["main"]["humidity"]
    wind= data["wind"]["speed"]
    desc= data["weather"][0]["description"].capitalize()

    print(f"\n{'='*40}")
    print(f"  {name}, {country}")
    print(f"{'='*40}")
    print(f"  Condition : {desc}")
    print(f"  Temp      : {temp}°C  (feels like {feels}°C)")
    print(f"  Humidity  : {humidity}%")
    print(f"  Wind      : {wind} m/s")
    print(f"{'='*40}")

def display_forecast(data):
    print("\n Next 24hr forecast")
    print(f" {'-'*36}")
    for item in data["list"]:
        time = item["dt_txt"][11:16]
        temp = item["main"]["temp"]
        desc = item["weather"][0]["description"]
        print(f"  {time}  -  {temp}°C  -  {desc}")
    print()



def main():
    parser= argparse.ArgumentParser(description="Weather CLI Dashboard")
    parser.add_argument("city", help="City name e.g. Delhi, Mumbai, London")
    args= parser.parse_args()

    city= args.city

    print(f"\nFetching weather for: {city}...")

    current=get_current_weather(city)
    forecast=get_forecast(city)

    display_current(current)
    display_forecast(forecast)

if __name__ == "__main__":
    main()