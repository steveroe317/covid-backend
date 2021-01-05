#!/usr/bin/env python3

US_STATES = [
    'Alabama',
    'Alaska',
    'American Samoa',
    'Arizona',
    'Arkansas',
    'California',
    'Colorado',
    'Connecticut',
    'Delaware',
    'District of Columbia',
    'Florida',
    'Georgia',
    'Guam',
    'Hawaii',
    'Idaho',
    'Illinois',
    'Indiana',
    'Iowa',
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Maine',
    'Maryland',
    'Massachusetts',
    'Michigan',
    'Minnesota',
    'Mississippi',
    'Missouri',
    'Montana',
    'Nebraska',
    'Nevada',
    'New Hampshire',
    'New Jersey',
    'New Mexico',
    'New York',
    'North Carolina',
    'North Dakota',
    'Northern Marina Islands',
    'Ohio',
    'Oklahoma',
    'Oregon',
    'Pennsylvania',
    'Puerto Rico',
    'Rhode Island',
    'South Carolina',
    'South Dakota',
    'Tennessee',
    'Texas',
    'U.S. Virgin Islands',
    'Utah',
    'Vermont',
    'Virginia',
    'Washington',
    'West Virginia',
    'Wisconsin',
    'Wyoming',
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

STATE_TEMPLATE = """
        {{ "name": "{code}", "include": [ "US:{code}" ] }},
"""[1:-1]

STATE_QUERY_TEMPLATE = """
        {{ "name": "{code}:Confirmed", "key": "Confirmed", "region": "{code}" }},
        {{ "name": "{code}:Deaths", "key": "Deaths", "region": "{code}", }},
"""[1:-1]

FILTERED_QUERY_TEMPLATE = """
        {{ "name": "{code}:Confirmed Daily", "filter": "daily", "source": "{code}:Confirmed" }},
        {{ "name": "{code}:Confirmed 7-Day", "filter": "7-day", "source": "{code}:Confirmed Daily" }},
        {{ "name": "{code}:Deaths Daily",  "filter": "daily", "source": "{code}:Deaths" }},
        {{ "name": "{code}:Deaths 7-Day", "filter": "7-day", "source": "{code}:Deaths Daily" }},
"""[1:-1]

REPORT_TABLES_HEADER_TEMPLATE = """
        {{
            "name": "US States",
            "tags_bundle": "State",
            "queries": [
"""[1:-1]

REPORT_TABLES_BODY_TEMPLATE = """
                "{code}:Confirmed",
                "{code}:Confirmed Daily",
                "{code}:Confirmed 7-Day",
                "{code}:Deaths",
                "{code}:Deaths Daily",
                "{code}:Deaths 7-Day",
"""[1:-1]

REPORT_TABLES_TRAILER_TEMPLATE = """
           ],
        }},
"""[1:-1]

SHEET_OUTPUT_TEMPLATE = """
        {{
            "spreadsheet_id": "1L1n4ty9qAawpOx3vgAg8r_bTlr34vgAX1bbS3vFy4YQ",
            "sheet_name": "Source Data",
            "table": "US States"
        }},
"""[1:-1]


def main():
    states = sorted(US_STATES)

    print(FILE_HEADER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='regions'))
    for code in states:
        print(STATE_TEMPLATE.format(code=code))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='region_queries'))
    for code in states:
        print(STATE_QUERY_TEMPLATE.format(code=code))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='filtered_queries'))
    for code in states:
        print(FILTERED_QUERY_TEMPLATE.format(code=code))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='tagged_report_tables'))
    print(REPORT_TABLES_HEADER_TEMPLATE.format())
    for code in states:
        print(REPORT_TABLES_BODY_TEMPLATE.format(code=code))
    print(REPORT_TABLES_TRAILER_TEMPLATE.format())
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='sheet_outputs'))
    print(SHEET_OUTPUT_TEMPLATE.format())
    print(SECTION_TRAILER_TEMPLATE)

    print(FILE_TRAILER_TEMPLATE)


if __name__ == '__main__':
    main()
