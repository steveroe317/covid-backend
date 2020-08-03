#!/usr/bin/env python3

regions = [
]

REGION_MAP = {name: name for name in regions}
REGION_MAP['World'] = ''

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
        {{ "name": "{name}", "include": [ "{area}" ] }},
"""[1:-1]

REGION_QUERY_TEMPLATE = """
        {{ "name": "{name}:Confirmed", "key": "Confirmed", "region": "{name}" }},
        {{ "name": "{name}:Deaths", "key": "Deaths", "region": "{name}", }},
"""[1:-1]

FILTERED_QUERY_TEMPLATE = """
        {{ "name": "{name}:Confirmed Daily", "filter": "daily", "source": "{name}:Confirmed" }},
        {{ "name": "{name}:Confirmed 7-Day", "filter": "7-day", "source": "{name}:Confirmed Daily" }},
        {{ "name": "{name}:Deaths Daily",  "filter": "daily", "source": "{name}:Deaths" }},
        {{ "name": "{name}:Deaths 7-Day", "filter": "7-day", "source": "{name}:Deaths Daily" }},
"""[1:-1]

REPORT_TABLES_HEADER_TEMPLATE = """
        {{
            "name": "World",
            "tags_bundle": "Region",
            "queries": [
"""[1:-1]

REPORT_TABLES_BODY_TEMPLATE = """
                "{name}:Confirmed",
                "{name}:Confirmed Daily",
                "{name}:Confirmed 7-Day",
                "{name}:Deaths",
                "{name}:Deaths Daily",
                "{name}:Deaths 7-Day",
"""[1:-1]

REPORT_TABLES_TRAILER_TEMPLATE = """
           ],
        }},
"""[1:-1]

SHEET_OUTPUT_TEMPLATE = """
        {{
            "spreadsheet_id": "1E_r-EShCwHD6qs0VSEN-RlxgLotDbRWVBjpBcZ1K8EY",
            "sheet_name": "Source Data",
            "table": "World"
        }},
"""[1:-1]


def main():
    countries = sorted(REGION_MAP.keys())

    print(FILE_HEADER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='regions'))
    for name in countries:
        print(REGION_TEMPLATE.format(name=name, area=REGION_MAP[name]))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='region_queries'))
    for name in countries:
        print(REGION_QUERY_TEMPLATE.format(name=name))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='filtered_queries'))
    for name in countries:
        print(FILTERED_QUERY_TEMPLATE.format(name=name))
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='tagged_report_tables'))
    print(REPORT_TABLES_HEADER_TEMPLATE.format())
    for name in countries:
        print(REPORT_TABLES_BODY_TEMPLATE.format(name=name))
    print(REPORT_TABLES_TRAILER_TEMPLATE.format())
    print(SECTION_TRAILER_TEMPLATE)

    print(SECTION_HEADER_TEMPLATE.format(section='sheet_outputs'))
    print(SHEET_OUTPUT_TEMPLATE.format())
    print(SECTION_TRAILER_TEMPLATE)

    print(FILE_TRAILER_TEMPLATE)


if __name__ == '__main__':
    main()
