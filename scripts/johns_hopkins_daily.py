#!/usr/bin/env python3

import csv
from itertools import count

from countries import standard_country_name
from us_state_locations import (convert_us_location_to_state,
                                us_state_names_to_state,
                                us_states_to_state_names)


class JohnsHopkinsAreaNode:
    def __init__(self, country, state, admin2):
        self.country = country
        self.state = state
        self.admin2 = admin2
        self.children = {}
        self.confirmed = 0
        self.deaths = 0
        self.incident_rate = 0
        self.population = 0

    def __str__(self):
        return (f'country: "{self.country}", state: "{self.state}", '
                f'admin2: "{self.admin2}"')

    def roll_up_metrics(self):
        self._roll_up_confirmed()
        self._roll_up_deaths()
        self._roll_up_population()

    def lookup(self, name):
        if name == 'Confirmed':
            return self.confirmed
        elif name == 'Deaths':
            return self.deaths
        elif name == 'Population':
            return self.population
        else:
            raise ValueError(f'unsupported lookup key {name}')

    def _roll_up_confirmed(self):
        for child in self.children.values():
            self.confirmed += child._roll_up_confirmed()
        return self.confirmed

    def _roll_up_deaths(self):
        for child in self.children.values():
            self.deaths += child._roll_up_deaths()
        return self.deaths

    def _roll_up_population(self):
        population = 0
        for child in self.children.values():
            population += child._roll_up_population()
        if not self.incident_rate:
            self.population = population
        else:
            self.population = int(
                100000 * self.confirmed / self.incident_rate)

        return self.population


class JohnsHopkinsDaily:
    def __init__(self, filename):
        self.filename = filename
        self.data_dicts = self._read_csv_data_dicts(filename)
        self.area_root = self.build_area_tree(self.data_dicts)
        self.check_lookup = False

    def __str__(self):
        return f'filename: {self.filename}'

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

    def build_area_tree(self, data_dicts):

        # Find data dictionary keys.
        # TODO: Refactor finding data dictionary keys into separate method.
        admin2_key = None
        state_key = None
        country_key = None
        incident_rate_key = None
        confirmed_key = None
        deaths_key = None
        for key in data_dicts[0].keys():
            if 'Country' in key:
                country_key = key
            if 'State' in key:
                state_key = key
            if 'Admin2' in key:
                admin2_key = key
            if 'Incident_Rate' in key:
                incident_rate_key = key
            if 'Confirmed' in key:
                confirmed_key = key
            if 'Deaths' in key:
                deaths_key = key

        if not country_key:
            raise ValueError('no country key')
        if state_key and not country_key:
            raise ValueError('state key without country key')
        if admin2_key and not (state_key or country_key):
            raise ValueError('admin2 key with missing state or country key')
        if not confirmed_key:
            raise ValueError('incident rate key without confirmed key')

        # Build tree from data_dicts.
        root = JohnsHopkinsAreaNode(None, None, None)
        for dict in data_dicts:

            # Create tree node.
            # TODO: Refactor adding tree node into separate method.
            node = None
            state = None
            admin2 = None
            country = standard_country_name(dict[country_key])
            if state_key:
                state = dict[state_key]
            if admin2_key:
                admin2 = dict[admin2_key]
            if not country:
                raise ValueError('Empty country value')
            if state and not country:
                raise Exception(f'state {state} without country')
            if admin2 and not (state and country):
                raise Exception(
                    f'admin2 {admin2} and not state {state} '
                    f'or country {country}')
            if country == 'US' or country == 'United States':
                state = convert_us_location_to_state(state)
            if country not in root.children:
                node = JohnsHopkinsAreaNode(country, None, None)
                root.children[country] = node
            node = root.children[country]
            if state:
                if country == 'United States':
                    state_code = convert_us_location_to_state(state)
                    state = us_states_to_state_names(state_code)
                if state not in root.children[country].children:
                    node = JohnsHopkinsAreaNode(country, state, None)
                    root.children[country].children[state] = node
                node = root.children[country].children[state]
            if admin2:
                if admin2 not in root.children[country].children[state].children:
                    node = JohnsHopkinsAreaNode(country, state, admin2)
                    root.children[country].children[state].children[admin2] = node
                node = root.children[country].children[state].children[admin2]

            # Load tree nodes from data_dict
            if dict[confirmed_key]:
                node.confirmed += int(dict[confirmed_key])
            if dict[deaths_key]:
                node.deaths += int(dict[deaths_key])
            if incident_rate_key in dict and dict[incident_rate_key]:
                node.incident_rate = float(dict[incident_rate_key])
            else:
                node.incident_rate = 0.0

        root.roll_up_metrics()

        return root

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
                if _match_state(data_country, data_dict[state_key], state):
                    locations.add(data_dict[admin2_key])

        return locations

    def numeric_value(self, text):
        return round(float(text)) if text else 0

    def sum(self, sum_key):
        if sum_key == 'Population':
            return self._lookup_root(sum_key)
        elif sum_key in ['Confirmed', 'Deaths']:
            lookup_value = self._lookup_root(sum_key)
            if self.check_lookup:
                sum_value = self._sum_data(sum_key)
                if lookup_value != sum_value:
                    raise Exception(f'file {self.filename} key {sum_key} '
                                    f'loopkup value {lookup_value} not equal '
                                    f'sum value {sum_value}')
            return lookup_value
        else:
            return self._sum_data(sum_key)

    def sum_by_country(self, sum_key, country):
        if sum_key == 'Population':
            return self._lookup_country(sum_key, country)
        elif sum_key in ['Confirmed', 'Deaths']:
            lookup_value = self._lookup_country(sum_key, country)
            if self.check_lookup:
                sum_value = self._sum_data_by_country(sum_key, country)
                if lookup_value != sum_value:
                    raise Exception(f'loopkup value {lookup_value} not equal '
                                    f'sum value {sum_value}')
            return lookup_value
        else:
            return self._sum_data_by_country(sum_key, country)

    def sum_by_country_state(self, sum_key, state, country):
        if sum_key == 'Population':
            return self._lookup_country_state(sum_key, state, country)
        elif sum_key in ['Confirmed', 'Deaths']:
            lookup_value = self._lookup_country_state(sum_key, state, country)
            if self.check_lookup:
                sum_value = self._sum_data_by_country_state(sum_key, state,
                                                            country)
                if lookup_value != sum_value:
                    raise Exception(f'file {self.filename} country {country} '
                                    f'state {state} '
                                    f'lookup value {lookup_value} not equal '
                                    f'sum value {sum_value}')
            return lookup_value
        else:
            return self._sum_data_by_country_state(sum_key, state, country)

    def sum_by_country_state_county(self, sum_key, county, state, country):
        if sum_key == 'Population':
            return self._lookup_country_state_county(sum_key, county, state,
                                                     country)
        elif sum_key in ['Confirmed', 'Deaths']:
            lookup_value = self._lookup_country_state_county(sum_key, county,
                                                             state, country)
            if self.check_lookup:
                sum_value = self._sum_data_by_country_state_county(
                    sum_key, county, state, country)
                if lookup_value != sum_value:
                    raise Exception(f'loopkup value {lookup_value} not equal '
                                    f'sum value {sum_value}')
            return lookup_value
        else:
            return self._sum_data_by_country_state_county(sum_key, county,
                                                          state, country)

    def _lookup_root(self, sum_key):
        return self.area_root.lookup(sum_key)

    def _lookup_country(self, sum_key, country):
        if country not in self.area_root.children:
            return 0
        return self.area_root.children[country].lookup(sum_key)

    def _lookup_country_state(self, sum_key, state, country):
        if country == 'US' or country == 'United States':
            state = convert_us_location_to_state(state)

        if country not in self.area_root.children:
            return 0
        if state not in self.area_root.children[country].children:
            return 0
        return self.area_root.children[country].children[state].lookup(sum_key)

    def _lookup_country_state_county(self, sum_key, county, state, country):
        if country == 'US' or country == 'United States':
            state = convert_us_location_to_state(state)

        if country not in self.area_root.children:
            return 0
        if state not in self.area_root.children[country].children:
            return 0
        if county not in self.area_root.children[country].children[state].children.keys():
            return 0
        return self.area_root.children[country].children[state].children[county].lookup(sum_key)

    def _sum_data(self, sum_key):
        sum = 0

        if not self.data_dicts:
            return sum

        for data_dict in self.data_dicts:
            if sum_key in data_dict:
                row_val = data_dict[sum_key]
                sum += self.numeric_value(row_val)

        return sum

    def _sum_data_by_country(self, sum_key, country):
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

    def _sum_data_by_country_state(self, sum_key, state, country):
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
                if _match_state(country, data_dict[state_key], state):
                    if sum_key in data_dict:
                        row_val = data_dict[sum_key]
                        sum += self.numeric_value(row_val)

        return sum

    def _sum_data_by_country_state_county(self, sum_key, county, state, country):
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
                if _match_state(country, data_dict[state_key], state):
                    if standard_country_name(data_dict[country_key]) == country:
                        if data_dict[admin2_key] == county:
                            if sum_key in data_dict:
                                row_val = data_dict[sum_key]
                                sum += self.numeric_value(row_val)

        return sum


def _match_state(country, state_text, state_label):
    """ Check if Johns Hopkins state key text matches US state name or USPS code.

    The state key text has different formats for different daily data sets.

    For example, Washington State might be "Seattle, WA" or "Washington".

    Args:
        state_text: Johns Hopkins state key text.
        state_label: State name or USPS code.

    Returns True if there is a state match, or False if not.
    """

    if country != 'US' and country != 'United States':
        return state_text == state_label

    state_code = convert_us_location_to_state(state_text)
    if state_code == state_label:
        return True
    if state_code in us_states_to_state_names:
        if us_states_to_state_names[state_code] == state_label:
            return True
    if state_text == state_label:
        return True
    return False
