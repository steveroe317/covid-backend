#!/usr/bin/env python3

import csv

from countries import standard_country_name
from us_state_locations import (convert_us_location_to_state,
                                us_state_names_to_state,
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

    def country_state_admin2_locations(self, country, state):
        if not self.data_dicts:
            return set()

        admin2_key = None
        state_key = None
        country_key = None
        for key in self.data_dicts[0].keys():
            if 'Admin2' in key:
                admin2_key = key
            if 'State' in key:
                state_key = key
            if 'Country' in key:
                country_key = key

        if not country_key or not state_key or not admin2_key:
            return set()

        locations = set()
        for data_dict in self.data_dicts:
            data_country = standard_country_name(data_dict[country_key])
            if data_country == country:
                if _match_state(data_dict[state_key], state):
                    locations.add(data_dict[admin2_key])

        return locations

    def numeric_value(self, text):
        return int(float(text)) if text else 0

    def sum(self, sum_key):
        sum = 0

        if not self.data_dicts:
            return sum

        for data_dict in self.data_dicts:
            if sum_key in data_dict:
                row_val = data_dict[sum_key]
                sum += self.numeric_value(row_val)

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
                    sum += self.numeric_value(row_val)

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
            if standard_country_name(data_dict[country_key]) == country:
                if _match_state(data_dict[state_key], state):
                    if sum_key in data_dict:
                        row_val = data_dict[sum_key]
                        sum += self.numeric_value(row_val)

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
                if _match_state(data_dict[state_key], state):
                    if standard_country_name(data_dict[country_key]) == country:
                        if data_dict[admin2_key] == county:
                            if sum_key in data_dict:
                                row_val = data_dict[sum_key]
                                sum += self.numeric_value(row_val)

        return sum


def _match_state(state_text, state_label):
    """ Check if Johns Hopkins state key text matches state name or USPS code.

    The state key text has different formats for different daily data sets.

    For example, Washington State might be "Seattle, WA" or "Washington".

    Args:
        state_text: Johns Hopkins state key text.
        state_label: State name or USPS code.

    Returns True if there is a state match, or False if not.
    """

    state_code = convert_us_location_to_state(state_text)
    if state_code == state_label:
        return True
    if state_code in us_states_to_state_names:
        if us_states_to_state_names[state_code] == state_label:
            return True
    if state_text == state_label:
        return True
    return False
