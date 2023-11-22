from requests import get
# from get_time import get_time
from os import environ
import discord
# from transliterate import translit, get_available_language_codes

def get_weather(ctx, city_name):
    api_key = "4b9f9afe7c15fc0372530c7ad011104c"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = get(complete_url)
    x = response.json()
    status = x["cod"]
    if status != "404":
        y = x["main"]
        w = x["wind"]
        sys = x["sys"]
        current_temperature = y["temp"]
        temperature_in_celsius = round(current_temperature - 273.15, 1)
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        original_city_name = x["name"]
        country = sys["country"]
        # languages: ['bg', 'el', 'hy', 'ka', 'l1', 'mk', 'mn', 'ru', 'sr', 'uk']
        '''
        if country == "RU":
          home_city_name = translit(original_city_name, 'ru')
          original_city_name = f"{original_city_name} ({home_city_name})"
        if country == "RS":
          home_city_name = translit(original_city_name, 'sr')
          original_city_name = f"{original_city_name} ({home_city_name})"
        '''
        feels_like = y["feels_like"]
        feels_like = round(feels_like - 273.15, 1)
        min = y["temp_min"]
        min = round(min - 273.15, 1)
        max = y["temp_max"]
        max = round(max - 273.15, 1)
        wind_speed = w["speed"]
        wind_speed = int(wind_speed)
        wind_speed = round(wind_speed * 3.837, 1)
        weather_description = z[0]["description"]
        if temperature_in_celsius > 25:
          warning=discord.Color.red()
        elif temperature_in_celsius > 15.0:
          warning=discord.Color.orange()
        elif temperature_in_celsius < -5.0:
          warning=0xeeffee
        else:
          warning=discord.Color.blue()
        embed = discord.Embed(title=f"Weather forecast for {original_city_name} :flag_{country.lower()}:", color=warning, 
        # timestamp=ctx.message.created_at
        )
        embed.set_thumbnail(url="https://cdn.dribbble.com/users/2120934/screenshots/6193524/media/0e653e48615e57898805fd78918e697d.gif")
        embed.add_field(name="Temperature", value=f"{str(temperature_in_celsius)}°C", inline=True)
        embed.add_field(name="Atmospheric Pressure", value=f"{str(current_pressure)}mbar", inline=True)
        embed.add_field(name="Humidity", value=f"{str(current_humidity)}%", inline=True)
        embed.add_field(name="Feels Like", value=f"{str(feels_like)}°C", inline=True)
        embed.add_field(name="Min / Max °C", value=f"{str(min)}°C / {str(max)}°C", inline=True)
        embed.add_field(name="Wind Speed", value=f"{str(wind_speed)}km/h", inline=True)
        embed.add_field(name="Description", value=weather_description, inline=True)
        # embed.set_footer(text=f'Requested by - {ctx.author}', icon_url=ctx.author.avatar_url)
        return embed, original_city_name, country
    elif status == "404":
        embed = discord.Embed(title=f"{city_name} Not Found", color=discord.Color.red())
        embed.add_field(name="Errorcode", value=f"404")
        return embed, "404"
    else:
        embed = discord.Embed(title=f"Error occured. Please try again!", color=discord.Color.red())
        embed.add_field(name="Errorcode", value=status)
        return embed, status

def tell_weather(city_name):
    api_key = "4b9f9afe7c15fc0372530c7ad011104c"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = get(complete_url)
    x = response.json()
    status = x["cod"]
    if status != "404":
        y = x["main"]
        current_temperature = y["temp"]
        original_city_name = x["name"]
        temperature_in_celsius = round(current_temperature - 273.15, 1)
        z = x["weather"]
        weather_description = z[0]["description"]
        return f"Currently are {temperature_in_celsius}° in {original_city_name} with {weather_description}."
    elif status == "404":
        return f"{city_name} not found. Please check your spelling."
    else:
        return "Error occured. Please try again!"