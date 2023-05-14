import python_weather
import os
import asyncio
import matplotlib.pyplot as plt
from PIL import Image


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
   

async def weather_visualization(city):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        # fetch a weather forecast from specified location
        weather = await client.get(city, locale="sl_SI")

        forecast_today = list(weather.forecasts)[0]
        hourly_temperatures = []
        hourly_precipitation = []
        hourly_kind = []
        for hourly in forecast_today.hourly:
            hourly_temperatures.append(hourly.temperature)
            hourly_precipitation.append(hourly.precipitation)
            hourly_kind.append(hourly.kind)

        # visualize the current forecast with matplotlib
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        ax1.set_xlabel('Time')
        ax1.set_ylabel('Temperatures')
        ax2.set_ylabel('Precipitation')
        ax1.plot(range(0, 22, 3), hourly_temperatures, color="red")
        ax2.bar(range(0, 22, 3), hourly_precipitation, color="blue", width=2)
        
        ax1.set_xticks(range(0, 22, 3))
        ax1.set_xticklabels(list(map(lambda x: str(x)+":00", list(range(0, 22, 3)))))

        ax1.set_xlim([0, 21])
        ax1.set_ylim([min(min(hourly_temperatures), 0), max(max(hourly_temperatures), 25)])
        ax2.set_ylim([min(min(hourly_precipitation), 0), max(max(hourly_precipitation), 10)])

        rainfall = classify_rainfall(weather.current.precipitation)
        temperature = f"{weather.current.temperature} °C (feels like " \
                      f"{weather.current.feels_like} °C)"
        current_description = f"Current conditions:\n{rainfall}\n{temperature}"
       
        ax1.text(0.5, 24, current_description, fontsize=14, verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='blue', alpha=0.25))
        plt.title(f"Forecast for {city}")
        plt.savefig("weather_forecast.jpg")
        image = Image.open("weather_forecast.jpg")
        return image
    
        
def visualize_forecast(city):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    coroutine = weather_visualization(city)
    return loop.run_until_complete(coroutine)


if __name__ == '__main__':
    visualize_forecast("Nanos")
  