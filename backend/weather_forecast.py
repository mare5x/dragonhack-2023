import python_weather
import os
import asyncio

def classify_rainfall(mmph):
   #Slight rain: Less than 0.5 mm per hour. Moderate rain: Greater than 0.5 mm per hour, but less than 4.0 mm per hour. 
   #Heavy rain: Greater than 4 mm per hour, but less than 8 mm per hour. Very heavy rain: Greater than 8 mm per hour.
    if mmph < 0.05:
        return "No rain"
    if mmph < 0.5:
        return "Slight rain"
    if mmph < 4:
        return "Moderate rain"
    if mmph < 8:
        return "Heavy rain"
    return "Very heavy rain"
   

async def getweather(city):
    # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        # fetch a weather forecast from specified location
        weather = await client.get(city)

        # returns the current day's forecast temperature (int)
        print(str(weather.current.temperature)+"°C" + " (feels like " + str(weather.current.feels_like)+"°C)")
        print(classify_rainfall(weather.current.precipitation))
        print(weather.current.kind)
    
        


if __name__ == '__main__':
  # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather("Dolenje pri Ajdovščini"))
