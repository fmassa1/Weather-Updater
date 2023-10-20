import schedule
import time

#retrieves the weather using the given lat and long
def get_weather(lat, long):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m,windspeed_10m&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    response = requests.get(url)
    data = response.json()
    return data

#sends the message through the use of a twilio account
def send_message(text):
    account_sid = "twilio_sid"
    auth_token = "twilio_token"
    from_phone_number = "from_phone_number"
    to_phone_number = "to_phone_number"

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=text,
        from_=from_phone_number,
        to=to_phone_number
    )
    print("Text has been sent!")

def send_update():
    #Chicago latitude and longitude
    lat = 41.85
    long = -87.65

    weather_data = get_weather(lat, long)
    temp_in_celsius = weather_data["hourly"]["temperature_2m"][0]
    humidity = weather_data["hourly"]["relativehumidy_2m"][0]
    wind_speeds = weather_data["hourly"]["windspeed_10m"][0]
    temp_in_fahrenheit = (temp_in_celsius * 9/5) + 32

    weather_info = (
        f"Good morning!\n"
        f"Current weather this morning:\n"
        f"Temperature: {temp_in_fahrenheit:.2f}F\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speeds: {wind_speeds} m\s"
        f"Have a wonderful day!"
    )
    send_message(weather_info)

def main():
    schedule.every(day).at("08:00").do(send_update)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
