#!/usr/bin/env python3

import itertools
import re

ROOT_COLLECTION = 'time-series'
SUB_COLLECTION = 'entities'

WORLD = [
    "World",
]

COUNTRIES = [
    'World:US',
    'World:Brazil',
    'World:India',
    'World:Russia',
    'World:South Africa',
    'World:Mexico',
    'World:Peru',
    'World:Chile',
    'World:Iran',
    'World:Colombia',
    'World:United Kingdom',
    'World:Spain',
    'World:Pakistan',
    'World:Saudi Arabia',
    'World:Italy',
    'World:Bangladesh',
    'World:Turkey',
    'World:France',
    'World:Germany',
    'World:Argentina',
    'World:Iraq',
    'World:Canada',
    'World:Qatar',
    'World:Indonesia',
    'World:Philippines',
    'World:Egypt',
    'World:Kazakhstan',
    'World:China',
    'World:Ecuador',
    'World:Sweden',
    'World:Norway',
    'World:Denmark',
    'World:Finland',
    'World:Ghana',
    'World:Uruguay',
    'World:Paraguay',
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
"""[1:-1]

FILTERED_QUERY_TEMPLATE = """
        {{ "name": "{code}:Confirmed Daily", "filter": "daily", "source": "{code}:Confirmed" }},
        {{ "name": "{code}:Confirmed 7-Day", "filter": "7-day", "source": "{code}:Confirmed Daily" }},
        {{ "name": "{code}:Deaths Daily",  "filter": "daily", "source": "{code}:Deaths" }},
        {{ "name": "{code}:Deaths 7-Day", "filter": "7-day", "source": "{code}:Deaths Daily" }},
"""[1:-1]

REPORT_TABLE_TEMPLATE = """
        {{
            "name": "{code}",
            "queries": [
                "{code}:Confirmed",
                "{code}:Confirmed Daily",
                "{code}:Confirmed 7-Day",
                "{code}:Deaths",
                "{code}:Deaths Daily",
                "{code}:Deaths 7-Day",
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
    admin_codes = list(itertools.chain(
        WORLD, COUNTRIES, US_STATES, US_WA_COUNTIES))

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
