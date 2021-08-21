#!/usr/bin/env python3


import argparse
import csv


from collections import defaultdict
from glob import glob
from re import sub


us_state_names_to_state = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Cruise Ship': 'SS',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'CP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'U.S. Virgin Islands': 'VI',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

state_name_adjustments = {
    'United States Virgin Islands': 'U.S. Virgin Islands',
}


def read_counties_from_wikidata_file():
    county_rows = []
    with open('state_counties_wikidata.csv') as counties_csv:
        county_reader = csv.reader(counties_csv, delimiter='\t')
        county_rows = [row for row in county_reader]
    return county_rows


def get_state_counties_from_wikidata_file():
    county_rows = read_counties_from_wikidata_file()
    normalize_state_names(county_rows)

    state_counties = defaultdict(set)
    for row in county_rows:
        (county, state_name) = (row[0], row[1])
        if state_name in us_state_names_to_state:
            state = us_state_names_to_state[state_name]
            county = filter_wiki_county_name(state, county)
            if (county):
                state_counties[state].add(county)

    return state_counties


def get_state_counties_from_johns_hopkins_files():
    admin2_files = glob('*.admin2')
    state_admin2s = defaultdict(set)
    for filename in admin2_files:
        state = filename.split('.')[0]
        with open(filename) as state_file:
            for admin2 in state_file:
                admin2 = filter_johns_admin2_name(state, admin2)
                if admin2:
                    state_admin2s[state].add(admin2)
    return state_admin2s


def normalize_state_names(county_rows):
    for row in county_rows:
        if row[1] in state_name_adjustments:
            row[1] = state_name_adjustments[row[1]]


def filter_wiki_county_name(state, county):
    county = sub(r' County$', '', county)
    return county


def filter_johns_admin2_name(state, admin2):
    admin2 = admin2.strip()
    admin2 = sub(r' County$', '', admin2)
    if admin2 in ['Unassigned', 'unassigned', 'Unknown', 'Out-of-state']:
        admin2 = ''
    if admin2.startswith('Out of '):
        admin2 = ''
    return admin2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['check', 'generate'])
    args = parser.parse_args()

    state_counties_wiki = get_state_counties_from_wikidata_file()
    state_counties_johns = get_state_counties_from_johns_hopkins_files()

    if args.operation == 'check':
        states_wiki = set(state_counties_wiki.keys())
        states_johns = set(state_counties_johns.keys())
        states_common = states_wiki & states_johns

        for state in sorted(states_common):
            counties_wiki = state_counties_wiki[state]
            counties_johns = state_counties_johns[state]
            counties_wiki_only = counties_wiki - counties_johns
            counties_johns_only = counties_johns - counties_wiki
            if counties_johns_only or counties_wiki_only:
                print(state)
                print('johns_only', sorted(counties_johns_only))
                print('wiki_only', sorted(counties_wiki_only))
    elif args.operation == 'generate':
        county_file_name = 'state_counties.py'
        print(f'Writing state county lists to {county_file_name}')
        with open(county_file_name, 'w') as county_file:
            def print_to_file(line):
                print(line, file=county_file)
            print_to_file('#!/usr/bin/env python3')
            print_to_file('')
            print_to_file('import itertools')
            print_to_file('')

            list_names = []
            for state in sorted(state_counties_johns.keys()):
                list_name = f'US_{state}_COUNTIES'
                list_names.append(list_name)
                print_to_file(f'{list_name} = [')
                for county in sorted(state_counties_johns[state]):
                    print_to_file(f'    "World:US:{state}:{county}",')
                print_to_file(']')
                print_to_file('')

            print_to_file('US_STATE_COUNTIES = list(itertools.chain(')
            for name in sorted(list_names):
                print_to_file(f'    {name},')
            print_to_file('))')
            print_to_file('')


if __name__ == '__main__':
    main()
