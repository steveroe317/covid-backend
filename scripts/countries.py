#!/usr/bin/env python3

alternate_country_names_to_country = {
    'Bahamas, The': 'Bahamas',
    'Gambia, The': 'Gambia',
    'Hong Kong SAR': 'Hong Kong',
    'Iran (Islamic Republic of)': 'Iran',
    'Macao SAR': 'Macau',
    'Mainland China': 'China',
    'Taiwan*': 'Taiwan',
    'The Bahamas': 'Bahamas',
    'The Gambia': 'Gambia',
    'Viet Nam': 'Vietnam',
}


def standard_country_name(name):
    name = name.strip()
    if name in alternate_country_names_to_country:
        return alternate_country_names_to_country[name]
    return name
