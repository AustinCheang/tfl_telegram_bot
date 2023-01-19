import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


class Stations:

    def __init__(self):
        self.stations_df = pd.read_csv("data/Stations.csv")
        self.base_url = f"https://tfl.gov.uk/hub/stop/"
        self.end_url = f"-underground-station/"
        self.stations_dict = self.get_stations_dict()
        self.origin_station_names = self.stations_df["Name"].tolist()

    def check_valid_station_name(self, input_station):
        return input_station in self.origin_station_names

    def clean_station_name(self):
        names = self.stations_df["Name"]
        cleaned_names = ([
            station.lower().replace(" ", "-")
            for station in names.values.tolist()
        ])
        return cleaned_names

    def get_stations_dict(self):
        cleaned_names = self.clean_station_name()
        unique_ids = self.stations_df["UniqueId"]
        return dict(zip(cleaned_names, unique_ids))

    def clean_name(self, station_name):
        if station_name.startswith(" "):
            station_name = station_name[1:]
        station_name = station_name.replace("-", " ")
        return station_name

    def get_station_url(self, station_name):
        if self.check_valid_station_name(station_name.title()):
            station_name = (station_name.lower().replace(" ", "-"))
            url = (
                f"{self.base_url}{self.stations_dict[station_name]}/{station_name}{self.end_url}"
            )
            return url
        else:
            return

    def get_station_info(self, station, station_url):
        response = requests.get(station_url)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Issues
        try:
            issue = soup.find(
                'div',
                id=lambda x: x and x.startswith('reported-issues-'
                                                ) and x.endswith('content'))
            msg = issue.text.replace("\n", "")
        except:
            msg = f"{station.title()} Station operates as usual."

        return f"[{station.title()}]\n{msg}"

    def get_current_update(self, station_name):
        url = self.get_station_url(station_name)
        if url is None:
            return
        issues = self.get_station_info(station_name, url)
        print(f"url: {url}, issues: {issues}")
        return issues

    def print_message(self, interested_stations):
        print(f"interested_stops: {interested_stations}")
        issues = [
            self.get_current_update(self.clean_name(station))
            for station in interested_stations
        ]
        current = datetime.now().strftime("%Y-%-m-%-d %H:%M:%S")
        message = []

        message.append(f"{current}\n\n")
        for issue in issues:
            message.append(f"{issue}\n\n")

        return "".join(message)
