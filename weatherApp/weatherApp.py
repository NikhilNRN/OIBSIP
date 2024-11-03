import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

API_KEY = "dae43a988337fddae06b67dcff47fc11"  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
LOCATION_API_URL = "https://ipinfo.io"  # Using ipinfo.io to get location data


# Fetch user's location based on IP
def get_user_city():
    try:
        response = requests.get(LOCATION_API_URL)
        data = response.json()
        city = data.get("city", "New York")  # Default to "New York" if city is not found
        return city
    except Exception as e:
        print("Could not determine location by IP:", e)
        return "New York"  # Default city if location fetching fails


# Fetch weather data
def get_weather(city=None):
    try:
        # Determine location if not provided
        if not city:
            city = get_user_city()

        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", "City not found.")
            return

        # Extract weather data
        city_name = data["name"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather_description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        icon_code = data["weather"][0]["icon"]

        # Update GUI elements
        lbl_city.config(text=f"Weather in {city_name}")
        lbl_temperature.config(text=f"Temperature: {temperature}°C")
        lbl_humidity.config(text=f"Humidity: {humidity}%")
        lbl_condition.config(text=f"Condition: {weather_description.capitalize()}")
        lbl_wind_speed.config(text=f"Wind Speed: {wind_speed} m/s")

        # Update weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_image = ImageTk.PhotoImage(Image.open(requests.get(icon_url, stream=True).raw))
        lbl_icon.config(image=icon_image)
        lbl_icon.image = icon_image  # Keep reference

    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Setup
root = tk.Tk()
root.title("Weather App")

# Widgets
lbl_city = tk.Label(root, font=("Arial", 16, "bold"))
lbl_city.pack()

lbl_icon = tk.Label(root)
lbl_icon.pack()

lbl_temperature = tk.Label(root, font=("Arial", 14))
lbl_temperature.pack()

lbl_humidity = tk.Label(root, font=("Arial", 14))
lbl_humidity.pack()

lbl_condition = tk.Label(root, font=("Arial", 14))
lbl_condition.pack()

lbl_wind_speed = tk.Label(root, font=("Arial", 14))
lbl_wind_speed.pack()

# Entry for city input and button to fetch weather
entry_city = tk.Entry(root, font=("Arial", 14))
entry_city.pack(pady=10)
entry_city.insert(0, "Enter city name")

btn_fetch = tk.Button(root, text="Get Weather", command=lambda: get_weather(entry_city.get()))
btn_fetch.pack()

# Run default location weather
get_weather()

root.mainloop()
