def seconds_to_str(seconds, format_str="%H:%M:%S"):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)

    # Formatni almashtiramiz
    time_str = format_str.replace("%H", f"{hours:02}")
    time_str = time_str.replace("%M", f"{minutes:02}")
    time_str = time_str.replace("%S", f"{seconds:02}")

    return time_str


import requests
import json

def fetch_config_data():
    url = "https://masofaviy-monitoring.uz/api/CarWashDevice/Resources/12837192388a0sdua9hdsausdhas"
    auth = ('deviceuser', 'supersecret123')
    try:
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            config_data = response.json()
            for item in config_data:
                name = item['resourceName']
                price = item['resourceMinutePrice']
                relayPort = item['relayPort']
                relayOnTime = item['relayOnTime']
                relayOffTime = item['relayOfTime']
                print(f"Name: {name}, Price: {price}, Relay Port: {relayPort}, Relay On Time: {relayOnTime}, Relay Off Time: {relayOffTime}")
        else:
            print(f"Failed to fetch config data. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching config data: {e}")
        
if __name__ == "__main__":
    fetch_config_data()