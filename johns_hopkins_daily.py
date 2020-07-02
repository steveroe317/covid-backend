#!/usr/bin/env python3

import csv

from countries import standard_country_name
from us_state_locations import (convert_us_location_to_state,
                                us_states_to_state_names)


class JohnsHopkinsDaily:
    def __init__(self, filename):
        self.data_dicts = self._read_csv_data_dicts(filename)

    def _read_csv_data_dicts(self, filename):
        with open(filename, encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            rows = []
            for row in csvreader:
                rows.append(row)
            header_row = rows[0]
            data_dicts = []
            for row_num in range(1, len(rows)):
                data_dict = {}
                data_row = rows[row_num]
                for col_num in range(len(header_row)):
                    data_dict[header_row[col_num]] = data_row[col_num]
                data_dicts.append(data_dict)
        return data_dicts

    def keys(self):
        if self.data_dicts:
            return self.data_dicts[0].keys()
        else:
            return []

    def countries(self):
        if not self.data_dicts:
            return set()

        for key in self.data_dicts[0].keys():
            if 'Country' in key:
                country_key = key

        countries = set()
        for data_dict in self.data_dicts:
            country = standard_country_name(data_dict[country_key])
            countries.add(country)

        return countries

    def country_state_locations(self, country):
        if not self.data_dicts:
            return set()

        for key in self.data_dicts[0].keys():
            if 'State' in key:
                state_key = key
            if 'Country' in key:
                country_key = key

        states = set()
        for data_dict in self.data_dicts:
            data_country = standard_country_name(data_dict[country_key])
            if data_country == country:
                states.add(data_dict[state_key])

        return states

    def sum(self, sum_key):
        sum = 0

        if not self.data_dicts:
            return sum

        for data_dict in self.data_dicts:
            if sum_key in data_dict:
                row_val = data_dict[sum_key]
                sum += int(row_val) if row_val else 0

        return sum

    def sum_by_country(self, sum_key, country):
        sum = 0

        if not self.data_dicts:
            return sum

        for key in self.data_dicts[0].keys():
            if 'Country' in key:
                country_key = key

        for data_dict in self.data_dicts:
            if standard_country_name(data_dict[country_key]) == country:
                if sum_key in data_dict:
                    row_val = data_dict[sum_key]
                    sum += int(row_val) if row_val else 0

        return sum

    def sum_by_country_state(self, sum_key, state, country):
        sum = 0

        if not self.data_dicts:
            return sum

        for key in self.data_dicts[0].keys():
            if 'State' in key:
                state_key = key
            if 'Country' in key:
                country_key = key

        for data_dict in self.data_dicts:
            if data_dict[country_key] == country:
                if convert_us_location_to_state(data_dict[state_key]) == state:
                    if standard_country_name(data_dict[country_key]) == country:
                        if sum_key in data_dict:
                            row_val = data_dict[sum_key]
                            sum += int(row_val) if row_val else 0

        return sum

    def sum_by_country_state_county(self, sum_key, county, state, country):
        sum = 0

        if not self.data_dicts:
            return sum

        admin2_key = None

        for key in self.data_dicts[0].keys():
            if 'State' in key:
                state_key = key
            if 'Country' in key:
                country_key = key
            if 'Admin2' in key:
                admin2_key = key

        if not admin2_key:
            return 0

        for data_dict in self.data_dicts:
            if data_dict[country_key] == country:
                if convert_us_location_to_state(data_dict[state_key]) == state:
                    if standard_country_name(data_dict[country_key]) == country:
                        if data_dict[admin2_key] == county:
                            if sum_key in data_dict:
                                row_val = data_dict[sum_key]
                                sum += int(row_val) if row_val else 0

        return sum
