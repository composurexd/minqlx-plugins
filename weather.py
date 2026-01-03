import minqlx
import requests

weatherdict = {
        "0": "Unknown",
        "1000": "Clear, Sunny",
        "1100": "Mostly Clear",
        "1101": "Partly Cloudy",
        "1102": "Mostly Cloudy",
        "1001": "Cloudy",
        "2000": "Fog",
        "2100": "Light Fog",
        "4000": "Drizzle",
        "4001": "Rain",
        "4200": "Light Rain",
        "4201": "Heavy Rain",
        "5000": "Snow",
        "5001": "Flurries",
        "5100": "Light Snow",
        "5101": "Heavy Snow",
        "6000": "Freezing Drizzle",
        "6001": "Freezing Rain",
        "6200": "Light Freezing Rain",
        "6201": "Heavy Freezing Rain",
        "7000": "Ice Pellets",
        "7101": "Heavy Ice Pellets",
        "7102": "Light Ice Pellets",
        "8000": "Thunderstorm"
}

class weather(minqlx.Plugin):

    def __init__(self):
        self.add_command("weather", self.cmd_weather, usage="<where?? spacing works (api.req limit 25/h~)>")
        self.add_command("weatherdemo", self.cmd_weatherdemo)
        self.set_cvar_once("qlx_weatherAPIkey", "**MY OWN HARDCODED KEY**")

    def cmd_weatherdemo(self, player, msg, channel):
        channel.reply("^1{} - ^3Temp: {}c, ^7Cloudiness: {}pct, ^4Condition: {}, ^5{} ({}) m/s^1|(c) compjke"
      	.format(minqlx.Game().map, -273.15 , 0 , "Ice Pellets", 0, 1 ))

    def cmd_weather(self, player, msg, channel):
        api_key = self.get_cvar("qlx_weatherAPIkey")

        if not api_key:
            self.msg("^3You need to set qlx_weatherAPIkey.")
            return minqlx.RET_STOP_ALL

        if(len(msg) == 1):
            return minqlx.RET_USAGE

        @minqlx.thread
        def get_weather():
            try:
                query_string = ""
                msglist = []
                #Concatenate all parameters called (!weather msg1 msg2..etc)
                for i in range(1, len(msg)):
                    msglist.append(str(msg[i]))
                query_string = ' '.join(msglist)
                query_string.replace(" ", "%20")
                res = requests.get("https://api.tomorrow.io/v4/weather/realtime?location=" + query_string + "&units=metric&apikey=" + api_key)
                res.raise_for_status()
                res = res.json()
                city = res["location"]["name"]
                temp = res["data"]["values"]["temperature"]
                weather = weatherdict[str(res["data"]["values"]["weatherCode"])]
                winds = res["data"]["values"]["windSpeed"]
                windg = res["data"]["values"]["windGust"]
                cloud = res["data"]["values"]["cloudCover"]
                channel.reply("^1{} | ^3Current Temp: {}c, ^4Condition: {}, ^7Cloudiness: {}pct, ^5{} ({}) m/s"
                .format(city, temp, weather, cloud, winds, windg))

            except requests.exceptions.RequestException as e:
                self.logger.info("ERROR: {}".format(e))

        get_weather()
