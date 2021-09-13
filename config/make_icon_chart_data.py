#!/usr/bin/env python3

import re
import os
import sys


WORLD = {
    'world': '',
}

COUNTRIES = {
    'us': 'US',
}

US_STATES = {
    'washington': 'US:WA',
}


US_WA_COUNTIES = {
    'king': 'US:WA:King',
}

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
        {{ "name": "{code}:Deaths Daily", "filter": "daily", "source": "{code}:Deaths" }},
        {{ "name": "{code}:Confirmed 7-Day", "filter": "7-day", "source": "{code}:Confirmed Daily" }},
        {{ "name": "{code}:Deaths 7-Day", "filter": "7-day", "source": "{code}:Deaths Daily" }},
        {{ "name": "{code}:Population", "filter": "gap-fill", "source": "{code}:Population Raw" }},
"""[1:-1]

REPORT_TABLE_TEMPLATE = """
        {{
            "name": "{code}",
            "queries": [
                "{code}:Confirmed 7-Day",
                "{code}:Deaths 7-Day",
                "{code}:Population",
            ],
        }},
"""[1:-1]

CSV_OUTPUT_TEMPLATE = """
        {{
            "filepath": "icon_graph_data/{path}.csv",
            "table": "{table}"
        }},
"""[1:-1]


def main():
    sys.path.append(os.path.join('..', 'scripts'))
    from us_state_locations import us_states_to_state_names

    regions = WORLD | COUNTRIES | US_STATES | US_WA_COUNTIES

    print(FILE_HEADER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='regions'))
    for code in regions.keys():
        print(REGION_TEMPLATE.format(code=code, admin_area=regions[code]))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='region_queries'))
    for code in regions.keys():
        print(QUERY_TEMPLATE.format(code=code))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='filtered_queries'))
    for code in regions.keys():
        print(FILTERED_QUERY_TEMPLATE.format(code=code))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='report_tables'))
    for code in regions.keys():
        print(REPORT_TABLE_TEMPLATE.format(code=code))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='csv_outputs'))
    for code in regions.keys():
        print(CSV_OUTPUT_TEMPLATE.format(path=code, table=code))
    print(SECTION_TRAILER_TEMPLATE)

    print(FILE_TRAILER_TEMPLATE)


if __name__ == '__main__':
    main()
