import json
import matplotlib.pyplot as plt
from PIL import Image
import requests
import datetime

API_key = "b45e1d6b581f6c2d99e5e432d21b2a2d"


def classify_rainfall(mm_per_hour):
    """ classifies rain from the mm per hour """
    if mm_per_hour < 0.1:
        return "No rain"
    if mm_per_hour < 0.5:
        return "Slight rain"
    if mm_per_hour < 4:
        return "Moderate rain"
    if mm_per_hour < 8:
        return "Heavy rain"
    return "Very heavy rain"
   

def WMO_code(num):
    code = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Fog",
        56: "Freezing drizzle",
        57: "Freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Freezing rain",
        67: "Freezing rain",
        68: "Freezing rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain shower",
        81: "Moderate rain shower",
        82: "Heavy rain shower",
        83: "Slight snow shower",
        85: "Moderate snow shower",
        86: "Heavy snow shower",
        95: "Thunderstorm",
        96: "Thunderstorm",
        99: "Thunderstorm"
    }
    return code.get(num, "unknown")


def weather_visualization(coordinates, city):
    
    lat, lon = coordinates
    forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}" \
                   f"&hourly=temperature_2m,precipitation,weathercode"
    
    report_forecast = (requests.get(forecast_url)).json()

    now = datetime.datetime.now()
    time_interval = now.hour if now.minute < 30 else (now.hour + 1)%24

    # weather forecast by hours for today
    hourly_temperatures = report_forecast["hourly"]["temperature_2m"][time_interval:time_interval+25]
    hourly_precipitation = report_forecast["hourly"]["precipitation"][time_interval:time_interval+25]
    hourly_weathercode = report_forecast["hourly"]["weathercode"][time_interval:time_interval+25]
    time_range = list(range(time_interval, time_interval+25,3))

    # visualize the current forecast with matplotlib
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Precipitation')
    ax2.set_ylabel('Temperatures')

    ax1.bar(range(0, 25), hourly_precipitation, color="blue", width=1)
    ax2.plot(range(0, 25), hourly_temperatures, color="red")
    
    ax1.set_xticks(range(0, 25, 3))
    ax1.set_xticklabels(list(map(lambda x: str(x%24)+":00", time_range)))

    ax1.set_xlim([0, 24])
    
    ax1.set_ylim([min(min(hourly_precipitation), 0), max(max(hourly_precipitation)+1, 10)])
    ax2.set_ylim([min(min(hourly_temperatures)-2, 0), max(max(hourly_temperatures)+2, 25)])

    # describe the current weather
    rainfall = classify_rainfall(hourly_precipitation[time_interval])
    temperature = str(hourly_temperatures[time_interval]) + " °C"
    description = WMO_code(hourly_weathercode[time_interval])
    current_description = f"{rainfall}\n{temperature}\n{description}"
    
    ax1.text(0.5, 9.7, current_description, fontsize=14, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='blue', alpha=0.25))
    
    plt.title(f"Forecast for {city}")
    plt.savefig("weather_forecast.jpg")
    image = Image.open("weather_forecast.jpg")
    return image
