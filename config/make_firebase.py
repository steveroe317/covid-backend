#!/usr/bin/env python3

import itertools
import re
import os
import sys


ROOT_COLLECTION = 'time-series'
SUB_COLLECTION = 'entities'

WORLD = [
    "World",
]

COUNTRIES = [
    'World:Afghanistan',
    'World:Albania',
    'World:Algeria',
    'World:Andorra',
    'World:Angola',
    'World:Antigua and Barbuda',
    'World:Argentina',
    'World:Armenia',
    'World:Australia',
    'World:Austria',
    'World:Azerbaijan',
    'World:Bahamas',
    'World:Bahrain',
    'World:Bangladesh',
    'World:Barbados',
    'World:Belarus',
    'World:Belgium',
    'World:Belize',
    'World:Benin',
    'World:Bhutan',
    'World:Bolivia',
    'World:Bosnia and Herzegovina',
    'World:Botswana',
    'World:Brazil',
    'World:Brunei',
    'World:Bulgaria',
    'World:Burkina Faso',
    'World:Burma',
    'World:Burundi',
    'World:Cabo Verde',
    'World:Cambodia',
    'World:Cameroon',
    'World:Canada',
    'World:Central African Republic',
    'World:Chad',
    'World:Chile',
    'World:China',
    'World:Colombia',
    'World:Comoros',
    'World:Congo (Kinshasa)',
    'World:Costa Rica',
    "World:Cote d'Ivoire",
    'World:Croatia',
    'World:Cuba',
    'World:Cyprus',
    'World:Czechia',
    'World:Denmark',
    'World:Dominican Republic',
    'World:Ecuador',
    'World:Egypt',
    'World:El Salvador',
    'World:Equatorial Guinea',
    'World:Eritrea',
    'World:Estonia',
    'World:Eswatini',
    'World:Ethiopia',
    'World:Fiji',
    'World:Finland',
    'World:France',
    'World:Gabon',
    'World:Gambia',
    'World:Georgia',
    'World:Germany',
    'World:Ghana',
    'World:Greece',
    'World:Grenada',
    'World:Guatemala',
    'World:Guinea',
    'World:Guinea-Bissau',
    'World:Guyana',
    'World:Haiti',
    'World:Honduras',
    'World:Hungary',
    'World:Iceland',
    'World:India',
    'World:Indonesia',
    'World:Iran',
    'World:Iraq',
    'World:Ireland',
    'World:Israel',
    'World:Italy',
    'World:Jamaica',
    'World:Japan',
    'World:Jordan',
    'World:Kazakhstan',
    'World:Kenya',
    'World:Kosovo',
    'World:Kuwait',
    'World:Kyrgyzstan',
    'World:Laos',
    'World:Latvia',
    'World:Lebanon',
    'World:Lesotho',
    'World:Liberia',
    'World:Libya',
    'World:Liechtenstein',
    'World:Lithuania',
    'World:Luxembourg',
    'World:Madagascar',
    'World:Malawi',
    'World:Malaysia',
    'World:Maldives',
    'World:Mali',
    'World:Malta',
    'World:Mauritania',
    'World:Mauritius',
    'World:Mexico',
    'World:Moldova',
    'World:Monaco',
    'World:Mongolia',
    'World:Montenegro',
    'World:Morocco',
    'World:Mozambique',
    'World:Namibia',
    'World:Nepal',
    'World:Netherlands',
    'World:New Zealand',
    'World:Nicaragua',
    'World:Niger',
    'World:Nigeria',
    'World:North Macedonia',
    'World:Norway',
    'World:Oman',
    'World:Pakistan',
    'World:Panama',
    'World:Papua New Guinea',
    'World:Paraguay',
    'World:Peru',
    'World:Philippines',
    'World:Poland',
    'World:Portugal',
    'World:Qatar',
    'World:Republic of the Congo',
    'World:Romania',
    'World:Russia',
    'World:Rwanda',
    'World:Saint Kitts and Nevis',
    'World:Saint Lucia',
    'World:Saint Vincent and the Grenadines',
    'World:Samoa',
    'World:San Marino',
    'World:Sao Tome and Principe',
    'World:Saudi Arabia',
    'World:Senegal',
    'World:Serbia',
    'World:Seychelles',
    'World:Sierra Leone',
    'World:Singapore',
    'World:Slovakia',
    'World:Slovenia',
    'World:Solomon Islands',
    'World:Somalia',
    'World:South Africa',
    'World:South Korea',
    'World:South Sudan',
    'World:Spain',
    'World:Sri Lanka',
    'World:Sudan',
    'World:Suriname',
    'World:Sweden',
    'World:Switzerland',
    'World:Syria',
    'World:Taiwan',
    'World:Tajikistan',
    'World:Tanzania',
    'World:Thailand',
    'World:Timor-Leste',
    'World:Togo',
    'World:Trinidad and Tobago',
    'World:Tunisia',
    'World:Turkey',
    'World:US',
    'World:Uganda',
    'World:Ukraine',
    'World:United Arab Emirates',
    'World:United Kingdom',
    'World:Uruguay',
    'World:Uzbekistan',
    'World:Vanuatu',
    'World:Vatican City',
    'World:Venezuela',
    'World:Vietnam',
    'World:West Bank and Gaza',
    'World:Yemen',
    'World:Zambia',
    'World:Zimbabwe',
]

CANADA_PROVINCES = [
    'World:Canada:Alberta',
    'World:Canada:British Columbia',
    'World:Canada:Manitoba',
    'World:Canada:New Brunswick',
    'World:Canada:Newfoundland and Labrador',
    'World:Canada:Northwest Territories',
    'World:Canada:Nova Scotia',
    'World:Canada:Nunavut',
    'World:Canada:Ontario',
    'World:Canada:Prince Edward Island',
    'World:Canada:Quebec',
    'World:Canada:Saskatchewan',
    'World:Canada:Yukon',
]

US_STATES = [
    'World:US:AK',
    'World:US:AL',
    'World:US:AR',
    'World:US:AS',
    'World:US:AZ',
    'World:US:CA',
    'World:US:CO',
    'World:US:CP',
    'World:US:CT',
    'World:US:DC',
    'World:US:DE',
    'World:US:FL',
    'World:US:GA',
    'World:US:GU',
    'World:US:HI',
    'World:US:IA',
    'World:US:ID',
    'World:US:IL',
    'World:US:IN',
    'World:US:KS',
    'World:US:KY',
    'World:US:LA',
    'World:US:MA',
    'World:US:MD',
    'World:US:ME',
    'World:US:MI',
    'World:US:MN',
    'World:US:MO',
    'World:US:MS',
    'World:US:MT',
    'World:US:NC',
    'World:US:ND',
    'World:US:NE',
    'World:US:NH',
    'World:US:NJ',
    'World:US:NM',
    'World:US:NV',
    'World:US:NY',
    'World:US:OH',
    'World:US:OK',
    'World:US:OR',
    'World:US:PA',
    'World:US:RI',
    'World:US:SC',
    'World:US:SD',
    'World:US:TN',
    'World:US:TX',
    'World:US:UT',
    'World:US:VA',
    'World:US:VI',
    'World:US:VT',
    'World:US:WA',
    'World:US:WI',
    'World:US:WV',
    'World:US:WY',
]

US_CA_COUNTIES = [
    'World:US:CA:Alameda',
    'World:US:CA:Alpine',
    'World:US:CA:Amador',
    'World:US:CA:Butte',
    'World:US:CA:Calaveras',
    'World:US:CA:Colusa',
    'World:US:CA:Contra Costa',
    'World:US:CA:Del Norte',
    'World:US:CA:El Dorado',
    'World:US:CA:Fresno',
    'World:US:CA:Glenn',
    'World:US:CA:Humboldt',
    'World:US:CA:Imperial',
    'World:US:CA:Inyo',
    'World:US:CA:Kern',
    'World:US:CA:Kings',
    'World:US:CA:Lake',
    'World:US:CA:Lassen',
    'World:US:CA:Los Angeles',
    'World:US:CA:Madera',
    'World:US:CA:Marin',
    'World:US:CA:Mariposa',
    'World:US:CA:Mendocino',
    'World:US:CA:Merced',
    'World:US:CA:Modoc',
    'World:US:CA:Mono',
    'World:US:CA:Monterey',
    'World:US:CA:Napa',
    'World:US:CA:Nevada',
    'World:US:CA:Orange',
    'World:US:CA:Placer',
    'World:US:CA:Plumas',
    'World:US:CA:Riverside',
    'World:US:CA:Sacramento',
    'World:US:CA:San Benito',
    'World:US:CA:San Bernardino',
    'World:US:CA:San Diego',
    'World:US:CA:San Francisco',
    'World:US:CA:San Joaquin',
    'World:US:CA:San Luis Obispo',
    'World:US:CA:San Mateo',
    'World:US:CA:Santa Barbara',
    'World:US:CA:Santa Clara',
    'World:US:CA:Santa Cruz',
    'World:US:CA:Shasta',
    'World:US:CA:Sierra',
    'World:US:CA:Siskiyou',
    'World:US:CA:Solano',
    'World:US:CA:Sonoma',
    'World:US:CA:Stanislaus',
    'World:US:CA:Sutter',
    'World:US:CA:Tehama',
    'World:US:CA:Trinity',
    'World:US:CA:Tulare',
    'World:US:CA:Tuolumne',
    'World:US:CA:Ventura',
    'World:US:CA:Yolo',
    'World:US:CA:Yuba',
]

US_WA_COUNTIES = [
    'World:US:WA:Adams',
    'World:US:WA:Asotin',
    'World:US:WA:Benton',
    'World:US:WA:Chelan',
    'World:US:WA:Clallam',
    'World:US:WA:Clark',
    'World:US:WA:Columbia',
    'World:US:WA:Cowlitz',
    'World:US:WA:Douglas',
    'World:US:WA:Ferry',
    'World:US:WA:Franklin',
    'World:US:WA:Garfield',
    'World:US:WA:Grant',
    'World:US:WA:Greys Harbor',
    'World:US:WA:Island',
    'World:US:WA:Jefferson',
    'World:US:WA:King',
    'World:US:WA:Kitsap',
    'World:US:WA:Kittitas',
    'World:US:WA:Klickitat',
    'World:US:WA:Lewis',
    'World:US:WA:Lincoln',
    'World:US:WA:Mason',
    'World:US:WA:Okanogan',
    'World:US:WA:Pacific',
    'World:US:WA:Pend Oreille',
    'World:US:WA:Pierce',
    'World:US:WA:San Juan',
    'World:US:WA:Skagit',
    'World:US:WA:Skamania',
    'World:US:WA:Snohomish',
    'World:US:WA:Spokane',
    'World:US:WA:Stevens',
    'World:US:WA:Thurston',
    'World:US:WA:Wahkiakum',
    'World:US:WA:Walla Walla',
    'World:US:WA:Whatcom',
    'World:US:WA:Whitman',
    'World:US:WA:Yakima',
]

FILE_HEADER_TEMPLATE = """
{
"""[1:-1]

FILE_TRAILER_TEMPLATE = """
}
"""[1:-1]

SECTION_HEADER_TEMPLATE = """
    "{section}": [
"""[1:-1]

SECTION_TRAILER_TEMPLATE = """
    ],
"""[1:-1]

REGION_TEMPLATE = """
        {{ "name": "{code}", "include": [ "{admin_area}" ] }},
"""[1:-1]

QUERY_TEMPLATE = """
        {{ "name": "{code}:Confirmed", "key": "Confirmed", "region": "{code}" }},
        {{ "name": "{code}:Deaths", "key": "Deaths", "region": "{code}", }},
        {{ "name": "{code}:Population Raw", "key": "Population", "region": "{code}", }},
"""[1:-1]

FILTERED_QUERY_TEMPLATE = """
        {{ "name": "{code}:Confirmed Daily", "filter": "daily", "source": "{code}:Confirmed" }},
        {{ "name": "{code}:Confirmed 7-Day", "filter": "7-day", "source": "{code}:Confirmed Daily" }},
        {{ "name": "{code}:Deaths Daily",  "filter": "daily", "source": "{code}:Deaths" }},
        {{ "name": "{code}:Deaths 7-Day", "filter": "7-day", "source": "{code}:Deaths Daily" }},
        {{ "name": "{code}:Population", "filter": "gap-fill", "source": "{code}:Population Raw" }},
"""[1:-1]

REPORT_TABLE_TEMPLATE = """
        {{
            "name": "{code}",
            "queries": [
                "{code}:Confirmed",
                "{code}:Confirmed 7-Day",
                "{code}:Deaths",
                "{code}:Deaths 7-Day",
                "{code}:Population",
            ],
        }},
"""[1:-1]

FIREBASE_OUTPUT_TEMPLATE = """
        {{
            "document_path": "{path}",
            "table": "{table}"
        }},
"""[1:-1]


def main():
    sys.path.append(os.path.join('..', 'scripts'))
    from us_state_locations import us_states_to_state_names

    admin_codes = list(itertools.chain(
        WORLD, COUNTRIES, CANADA_PROVINCES, US_STATES, US_CA_COUNTIES, US_WA_COUNTIES))

    print(FILE_HEADER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='regions'))
    for code in admin_codes:
        admin_area = re.sub(r'^World:?', '', code)
        print(REGION_TEMPLATE.format(code=code, admin_area=admin_area))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='region_queries'))
    for code in admin_codes:
        print(QUERY_TEMPLATE.format(code=code))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='filtered_queries'))
    for code in admin_codes:
        print(FILTERED_QUERY_TEMPLATE.format(code=code))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='report_tables'))
    for code in admin_codes:
        print(REPORT_TABLE_TEMPLATE.format(code=code))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='firebase_outputs'))
    for code in admin_codes:
        areas = code.split(':')
        if len(areas) >= 2 and areas[1] == 'US':
            areas[1] = 'United States'
        if len(areas) >= 3 and areas[2] in us_states_to_state_names:
            areas[2] = us_states_to_state_names[areas[2]]
        path_segments = []
        for index, area in enumerate(areas):
            path_segments.append(
                ROOT_COLLECTION if index == 0 else SUB_COLLECTION)
            path_segments.append(area)
        path = '/'.join(path_segments)
        print(FIREBASE_OUTPUT_TEMPLATE.format(path=path, table=code))
    print(SECTION_TRAILER_TEMPLATE)

    print(FILE_TRAILER_TEMPLATE)


if __name__ == '__main__':
    main()
