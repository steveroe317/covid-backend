#!/usr/bin/env python3

import datetime
import os
import re
from functools import reduce

from johns_hopkins_daily import JohnsHopkinsDaily


class JohnsHopkinsJournal:
    def __init__(self, dir_path):
        self.dailies = self._load_dailies(dir_path)

    def _find_csv_files(self, dir_path):
        date_files = {}
        for name in os.listdir(dir_path):
            path = os.path.join(dir_path, name)
            if os.path.isfile(path):
                match = re.match(r'^(?P<MM>\d\d)-(?P<DD>\d\d)-(?P<YYYY>\d\d\d\d)\.csv$',
                                 name)
                if match:
                    # Increment timestamp from file name date by one day to
                    # adjust for Johns Hopkins github data update schedule.
                    file_name_date = datetime.datetime(int(match.group(
                        'YYYY')), int(match.group('MM')), int(match.group('DD')))
                    sample_date = file_name_date + \
                        datetime.timedelta(days=1)
                    sample_date_string = sample_date.strftime('%Y-%m-%d')
                    date_files[sample_date_string] = path
        return date_files

    def _load_dailies(self, dir_path):
        date_files = self._find_csv_files(dir_path)
        dailies = {}
        for date in date_files:
            dailies[date] = JohnsHopkinsDaily(date_files[date])
        return dailies

    def daily_keys_reduce(self, func):
        keys = reduce(func, [set(daily.keys())
                             for daily in self.dailies.values()])
        return keys

    def daily_keys_by_date(self):
        date_to_keys = {}
        for date in self.dailies.keys():
            date_to_keys[date] = self.dailies[date].keys()
        return date_to_keys

    def countries(self):
        countries = set()
        for daily in self.dailies.values():
            countries |= daily.countries()
        return countries

    def country_locations(self, country):
        locations = set()
        for daily in self.dailies.values():
            locations |= daily.country_state_locations(country)
        return locations

    def country_state_locations(self, country):
        state_labels = set()
        for daily in self.dailies.values():
            state_labels |= daily.country_state_locations(country)
        return state_labels

    def country_state_admin2_locations(self, country, state):
        admin2_labels = set()
        for daily in self.dailies.values():
            admin2_labels |= daily.country_state_admin2_locations(
                country, state)
        return admin2_labels

    def get_world_data(self, data_keys):
        data = {}
        for date in self.dailies.keys():
            daily = self.dailies[date]
            daily_data = {}
            for data_key in data_keys:
                daily_data[data_key] = daily.sum(data_key)
            data[date] = daily_data
        return data

    def get_country_data(self, country, data_keys):
        data = {}
        for date in self.dailies.keys():
            daily = self.dailies[date]
            daily_data = {}
            for data_key in data_keys:
                daily_data[data_key] = daily.sum_by_country(data_key, country)
            data[date] = daily_data
        return data

    def get_state_data(self, state, country, data_keys):
        data = {}
        for date in self.dailies.keys():
            daily = self.dailies[date]
            daily_data = {}
            for data_key in data_keys:
                daily_data[data_key] = daily.sum_by_country_state(data_key, state,
                                                                  country)
            data[date] = daily_data
        return data

    def get_county_data(self, county, state, country, data_keys):
        data = {}
        for date in self.dailies.keys():
            daily = self.dailies[date]
            daily_data = {}
            for data_key in data_keys:
                daily_data[data_key] = daily.sum_by_country_state_county(
                    data_key, county, state, country)
            data[date] = daily_data
        return data
