

import forecastio


class Weather:

    def __init__(self, apiKey, latitude, longitude):
        self.apiKey = apiKey
        self.latitude = latitude
        self.longitude = longitude
        self.forecast = forecastio.load_forecast(self.apiKey, self.latitude, self.longitude, lang="fr", units="si")

    def getCurrent(self):
        """
        Get current weather
        :return: dict, current summary, icon, time, temp, % of precip. and pressure
        """
        currently = self.forecast.currently()
        current = {
            "time": currently.time,
            "summary": currently.summary,
            "temp": int(currently.temperature),
            "precip": currently.precipProbability * 100,
            "pressure": currently.pressure
        }
        return current

    def getNextHours(self):
        """
        Get next hours weather
        :param nbHours: int, number of hours to check
        :return: dict, time, summary, temp and % of precip. for next nbHours
        """
        hourly = self.forecast.hourly()
        hours = {}
        count = 0
        for element in hourly.data:
            hours[int(element.time.hour)] = [element.summary, int(element.temperature),
                                        int(element.precipProbability * 100)]
            count += 1
        return hours

    def getNextDays(self):
        """
        Get next days weather
        :param nbDays: int, number of days to check
        :return: dict, time, summary, tempLow, tempHigh and % of precip. for next nbDays
        """
        daily = self.forecast.daily()

        days = {}
        count = 0
        for element in daily.data:
            days.setdefault(element.time, [element.summary, int(element.temperatureLow),
                                           int(element.temperatureHigh), int(element.precipProbability * 100)])
            count += 1
        return days

    def createMessage(self):
        msg = ""
        current = self.getCurrent()
        hour = current["time"].hour
        nextHours = self.getNextHours()
        for element in range(13):
            # Time difference with Bordeaux's time: +1 accounts for it
            details = nextHours[(hour + element) % 24]
            msg += str((hour + element + 1) % 24) + ":00 " + str(details[0]) + " " + str(details[1]) + "°C\n"
        return msg


def writeTextFile(name, msg):
    name = str(name) + ".txt"
    weatherFile = open(name, "w")
    weatherFile.write(msg)
    weatherFile.close()


# CALL TO FUNCTION
# Bordeaux's longitude & latitude
BORDEAUX = [44.8333, -0.5667]
# Forecastio API key
APIKEY = "411930895b50ecc6dd4ebe6330eb9a2e"

# Fetch data for Bdx
weather = Weather(APIKEY, BORDEAUX[0], BORDEAUX[1])
msg = weather.createMessage()
# Display message in terminal
# print(msg)

# Write weather report to text file
name = "WeatherReport"
writeTextFile(name, msg)
