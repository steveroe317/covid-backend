#!/usr/bin/env python3

WA_COUNTIES = [
    'Adams',
    'Asotin',
    'Benton',
    'Chelan',
    'Clallam',
    'Clark',
    'Columbia',
    'Cowlitz',
    'Douglas',
    'Ferry',
    'Franklin',
    'Garfield',
    'Grant',
    'Greys Harbor',
    'Island',
    'Jefferson',
    'King',
    'Kitsap',
    'Kittitas',
    'Klickitat',
    'Lewis',
    'Lincoln',
    'Mason',
    'Okanogan',
    'Pacific',
    'Pend Oreille',
    'Pierce',
    'San Juan',
    'Skagit',
    'Skamania',
    'Snohomish',
    'Spokane',
    'Stevens',
    'Thurston',
    'Wahkiakum',
    'Walla Walla',
    'Whatcom',
    'Whitman',
    'Yakima',
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

COUNTY_TEMPLATE = """
        {{ "name": "{code}", "include": [ "US:WA:{code}" ] }},
"""[1:-1]

COUNTY_QUERY_TEMPLATE = """
        {{ "name": "{code} Confirmed", "key": "Confirmed", "region": "{code}" }},
        {{ "name": "{code} Deaths", "key": "Deaths", "region": "{code}", }},
"""[1:-1]

FILTERED_QUERY_TEMPLATE = """
        {{ "name": "{code} Confirmed Daily", "filter": "daily", "source": "{code} Confirmed" }},
        {{ "name": "{code} Confirmed 7-Day", "filter": "7-day", "source": "{code} Confirmed Daily" }},
        {{ "name": "{code} Deaths Daily",  "filter": "daily", "source": "{code} Deaths" }},
        {{ "name": "{code} Deaths 7-Day", "filter": "7-day", "source": "{code} Deaths Daily" }},
"""[1:-1]

REPORT_TABLES_HEADER_TEMPLATE = """
        {{
            "name": "WA Counties",
            "queries": [
"""[1:-1]

REPORT_TABLES_BODY_TEMPLATE = """
                "{code} Confirmed",
                "{code} Confirmed Daily",
                "{code} Confirmed 7-Day",
                "{code} Deaths",
                "{code} Deaths Daily",
                "{code} Deaths 7-Day",
"""[1:-1]

REPORT_TABLES_TRAILER_TEMPLATE = """
           ],
        }},
"""[1:-1]

SHEET_OUTPUT_TEMPLATE = """
        {{
            "spreadsheet_id": "1bKhzZE7BOmTZmksWRaTRuGfDSPQKbxmkBeyp5Ed9i1o",
            "sheet_name": "Source Data",
            "table": "WA Counties"
        }},
"""[1:-1]

def main():
  county_codes = sorted(WA_COUNTIES)

  print(FILE_HEADER_TEMPLATE)

  print(SECTION_HEADER_TEMPLATE.format(section='regions'))
  for code in county_codes:
    print(COUNTY_TEMPLATE.format(code=code))
  print(SECTION_TRAILER_TEMPLATE)

  print(SECTION_HEADER_TEMPLATE.format(section='region_queries'))
  for code in county_codes:
    print(COUNTY_QUERY_TEMPLATE.format(code=code))
  print(SECTION_TRAILER_TEMPLATE)

  print(SECTION_HEADER_TEMPLATE.format(section='filtered_queries'))
  for code in county_codes:
    print(FILTERED_QUERY_TEMPLATE.format(code=code))
  print(SECTION_TRAILER_TEMPLATE)

  print(SECTION_HEADER_TEMPLATE.format(section='report_tables'))
  print(REPORT_TABLES_HEADER_TEMPLATE.format())
  for code in county_codes:
      print(REPORT_TABLES_BODY_TEMPLATE.format(code=code))
  print(REPORT_TABLES_TRAILER_TEMPLATE.format())
  print(SECTION_TRAILER_TEMPLATE)

  print(SECTION_HEADER_TEMPLATE.format(section='sheet_outputs'))
  print(SHEET_OUTPUT_TEMPLATE.format())
  print(SECTION_TRAILER_TEMPLATE)

  print(FILE_TRAILER_TEMPLATE)

if __name__ == '__main__':
  main()
