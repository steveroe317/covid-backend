#!/usr/bin/env python3

alternate_country_names_to_country = {
    'Bahamas, The': 'Bahamas',
    'Congo (Brazzaville)': 'Republic of the Congo',
    'Czech Republic': 'Czechia',
    'Gambia, The': 'Gambia',
    'Holy See': 'Vatican City',
    'Hong Kong SAR': 'Hong Kong',
    'Iran (Islamic Republic of)': 'Iran',
    'Ivory Coast': "Cote d'Ivoire",
    'Korea, South': 'South Korea',
    'Macao': 'China',
    'Macao SAR': 'China',
    'Mainland China': 'China',
    'Republic of Ireland': 'Ireland',
    'Republic of Korea': 'South Korea',
    'Taipei and environs': 'Taiwan',
    'Taiwan*': 'Taiwan',
    'The Bahamas': 'Bahamas',
    'The Gambia': 'Gambia',
    'UK': 'United Kingdom',
    'Viet Nam': 'Vietnam',
}


def standard_country_name(name):
    name = name.strip()
    if name in alternate_country_names_to_country:
        return alternate_country_names_to_country[name]
    return name
