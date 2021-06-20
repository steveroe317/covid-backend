#!/usr/bin/env python3

import itertools
import re
import os
import sys


ROOT_COLLECTION = 'time-series'
SUB_COLLECTION = 'entities'

Test = [
    "Test",
]

COUNTRIES = [
    'Test:Brazil',
    'Test:India',
    'Test:Israel',
    'Test:United Kingdom',
    'Test:US',
]

US_STATES = [
    'Test:US:CA',
    'Test:US:WA',
]


US_WA_COUNTIES = [
    'Test:US:WA:King',
    'Test:US:WA:Snohomish',
    'Test:US:WA:Spokane',
    'Test:US:WA:Yakima',
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
        Test, COUNTRIES, US_STATES, US_WA_COUNTIES))

    print(FILE_HEADER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='regions'))
    for code in admin_codes:
        admin_area = re.sub(r'^Test:?', '', code)
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
