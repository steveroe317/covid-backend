#!/usr/bin/env python3

US_STATE_SHEETS = {
  'AK': '13E84fEKRWBmyUlJYQUx-xyqUdd71PlKFv0VBetYfBOg',
  'AL': '1zwM9NJ2Qb68Y8tiFQeywa0sbCZ71XbJxHrcgm3b5NX0',
  'AR': '16Y5FwM57ztPVIKPDAQf0RFVbONkWn2QSWwP5QrGD-xo',
  'AS': '1KDP74RYWN4qwS8wUK3fxW2vZMGhKo_03ArJsAHQzD_A',
  'AZ': '1g9FSXeImUK_zLDqxypLuueCIXyKrxrfOcjaFGbdwU1M',
  'CA': '1E489tvTqkEZQOJPswSxYv6lVL0KAmzLfRsoaYh03YVo',
  'CO': '1XsgO8Rjj2cWO8Q6Az-008G-vDEjyg46SGqSAdOKfRSc',
  'CP': '17ejnGHyKsMDLyExJbxkxdMVAoXyv4zObl_f4DJIMTZQ',
  'CT': '1l2M6lf374Lxz1gpnd6aZcJsBTX9sR5VMDZxTlOB3s08',
  'DC': '1IowMV-w_2eJQLiRZeIiYSBUSkWEzwx03wi29tAbXniw',
  'DE': '1QncJpeid2rqG9DLF73TT8CLM2wiNLPm1bJJsk76y17k',
  'FL': '1xDOtZ8owLapcVrD26oiFTaInSVcOXpGF5p9ZaRjBWlA',
  'GA': '1J-U0rL6C6Ozs-jqBRl8cXGztRLQzptch_Jyf_op14D4',
  'GU': '1l7DKCJ4LH2mgli_VIGBI4K_pcgoWahxPEoiPq4wJ484',
  'HI': '1PCgdv48VN4qi01-l_uLWL3irxERiEEDXpcpc3CH0wVw',
  'IA': '1JN77eWisjA7bWBlWhozp8dPaP8f5O0JPLo3JWI4KIZA',
  'ID': '1JvP2_ipsMnOTI7fQYTdraPhPzswagGj6DfqvUHtct3E',
  'IL': '1QbnK1i0Ycbb5NGL_PyO7TSAD_FKQPXGggyy2UQ02hCE',
  'IN': '1FBkys-06izhmks9xHhWHKQYSZ_g2AL2MlhJwydWArRM',
  'KS': '1VDSN9Q7GCaHB04-2py58zwiKwa72bM-gAtnMWzA0zgU',
  'KY': '17zBN0uBK9fEobrUzHZ2-4K2I2eaxUmasqd5id3RYluA',
  'LA': '1bjs15-3hfxvaGYDI4hDRGg5tARyUERbFBH-y1adwrAI',
  'MA': '1CXchFDUulnTZkjJBoJn9s43L3GfFpcO3TqCNaNBBLQg',
  'MD': '1Gpvsj_aXCl9awg2v4Ay_zvV6PY4hYnFNBoJf1CJCFyU',
  'ME': '1XeEyWPnNCRzdV3p5KHzqeqaUFIAa3KUbk0JALz6wSk4',
  'MI': '1PgJQOVrXID0rR_8P7NCB-O6CGXJ7ymqKkflHXdOSt-A',
  'MN': '1mPnVHfjTxH6WAD6ONCUDSE642EvRLCgpZleCtmzJPsM',
  'MO': '1ORmxXASHh1IndDsztCYI8K1C7SIr-8x8j9VOXzfdEgs',
  'MS': '1ggvFdj-hGicDUeq6EhTvauaHS3tifxpD1m1GKqNYnnI',
  'MT': '1hyt0AWuDRFLzSiehKmfgzsvOGycs8PJ9FFEbdDSw0fU',
  'NC': '1z3Tavs3fx2IQOQ0D7-EAfNdT2_qYZfrVoEAGUV7ecwY',
  'ND': '1bkWRLRvZ6tVcXJBXXw1aUzAre4dS_3w59hLqIbkdrhk',
  'NE': '1bQt8zOi-AjEAx-3FpK-ncOuFTtzs2GT_kDrR91WriUA',
  'NH': '1gw9vAFjTtaqsQPgIJvkq3gYrPxnnixbgTTCKxOJ_CDs',
  'NJ': '1tIulxbwiCo2vK2mpezP1fxaVIniVILUtEzxkuIvN4TE',
  'NM': '1CSeS5lk3dMpYpUWDsd8hGX9fMpGGOtPTcioQf4k1PHU',
  'NV': '1gRVEi8zubWA0_gfWnDsGsXPiN8g8HXyuHPOdmi-lxhs',
  'NY': '1vnNNs6dQtlhM4FAs_vIWvM8lAGf23SPnemp9RNWG9aI',
  'OH': '1IhwBnD9ZQj-suXW9KREFeq4tPpOVk_oY0PBeYFIt-mc',
  'OK': '1f-eCWiLdNqLHmKpDwTpNsYJD1mbbINmGN_rieh5zTTA',
  'OR': '1hxGkWucjrCJ4EAKuO5F8DfFDRWBik9HdsnvIaTmQeKo',
  'PA': '1pLdLJ14g4P66xm3KBDMCNywaWL5JvWyFNL7VyzyLTI4',
  'RI': '1BpMCQg1mkSUInetkj1jGjBaGie-3yJ1IhjgW1NaaUVU',
  'SC': '17jXLEPVSacXmHMdRt6T_B8QQh4kqzp15BpdG37M8C7M',
  'SD': '1_wi6acyZidFbQ63q4qryfZAEgaY7sOA4Rdz61BXFoNY',
  'TN': '1mqCG-WxK20RtLgcjLgDeCx11Vlq789XBxCybBatIaVg',
  'TX': '1kpD_Q2DpJu7TYSoYOisCuNf8MhpzwcPNN9GXlC7HVoc',
  'UT': '1Fx8iKzWMiuZYyJ5SD5RU8J3Q9l9ntc2helM62qXLfUA',
  'VA': '14nCn0dJXQO3iK_WZ3a3KR0aEjB0A7usTDNnGelE1RiA',
  'VI': '1BifoI7dh_69S9HXIWgU50Dy3R3S0KbsfSjCDGhdEIYI',
  'VT': '1uYaHQjBqaOWF16ITwkIErGCo4XjrR7OQeyW0OdwUxnc',
  'WA': '177TECfs3rfDBUbNDyM3TQLZEjJu7N06rzc4BsVuxc3k',
  'WI': '18pLZQm4CG2O992oBdAp58MlD5LXO_VHVPyE6Wwb3UeM',
  'WV': '1B_I-gG91dyK9z8_TFpLkdEPB-qAZwTiD1tBTlpuBdRo',
  'WY': '1x45zTM8QELjNz452UdBKe0S2LZ0bCMzGDwmH6f0Z5Ok',

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
        {{ "name": "{code}", "include": [ "US:{code}" ] }},
"""[1:-1]

NATIONAL_REGIONS = """
        { "name": "US", "include": [ "US" ] },
        {
            "name": "US without NY",
            "include": [ "US" ],
            "exclude": [
                "US:NY",
                "US:NJ",
                "US:CT",
            ],
        },
"""[1:-1]

REGION_QUERY_TEMPLATE = """
        {{ "name": "{code} Confirmed", "key": "Confirmed", "region": "{code}" }},
        {{ "name": "{code} Deaths", "key": "Deaths", "region": "{code}", }},
"""[1:-1]

NATIONAL_REGION_QUERIES = """
        { "name": "US Confirmed",  "key": "Confirmed", "region": "US", },
        { "name": "US Deaths", "key": "Deaths", "region": "US", },
        {
            "name": "US without NY Confirmed",
            "key": "Confirmed",
            "region": "US without NY",
        },
        {
            "name": "US without NY Deaths",
            "key": "Deaths",
            "region": "US without NY",
        },
"""[1:-1]

FILTERED_QUERY_TEMPLATE = """
        {{ "name": "{code} Confirmed Daily", "filter": "daily", "source": "{code} Confirmed" }},
        {{ "name": "{code} Confirmed 7-Day", "filter": "7-day", "source": "{code} Confirmed Daily" }},
        {{ "name": "{code} Deaths Daily",  "filter": "daily", "source": "{code} Deaths" }},
        {{ "name": "{code} Deaths 7-Day", "filter": "7-day", "source": "{code} Deaths Daily" }},
"""[1:-1]

NATIONAL_FILTERED_QUERIES = """
        { "name": "US Confirmed Daily", "filter": "daily", "source": "US Confirmed", },
        { "name": "US Confirmed 7-Day", "filter": "7-day", "source": "US Confirmed Daily", },
        { "name": "US Deaths Daily", "filter": "daily", "source": "US Deaths", },
        { "name": "US Deaths 7-Day", "filter": "7-day", "source": "US Deaths Daily", },
        {
            "name": "US without NY Confirmed Daily",
            "filter": "daily",
            "source": "US without NY Confirmed",
        },
        {
            "name": "US without NY Confirmed 7-Day",
            "filter": "7-day",
            "source": "US without NY Confirmed Daily",
        },
        {
            "name": "US without NY Deaths Daily",
            "filter": "daily",
            "source": "US without NY Deaths",
        },
        {
            "name": "US without NY Deaths 7-Day",
            "filter": "7-day",
            "source": "US without NY Deaths Daily",
        },
"""[1:-1]

REPORT_TABLE_TEMPLATE = """
        {{
            "name": "{code}",
            "queries": [
                "{code} Confirmed",
                "{code} Confirmed Daily",
                "{code} Confirmed 7-Day",
                "{code} Deaths",
                "{code} Deaths Daily",
                "{code} Deaths 7-Day",
            ],
        }},
"""[1:-1]

NATIONAL_REPORT_TABLES = """
        {
            "name": "US",
            "queries": [
                "US Confirmed",
                "US Confirmed Daily",
                "US Confirmed 7-Day",
                "US Deaths",
                "US Deaths Daily",
                "US Deaths 7-Day",
            ],
        },
        {
            "name": "US without NY",
            "queries": [
                "US without NY Confirmed",
                "US without NY Confirmed Daily",
                "US without NY Confirmed 7-Day",
                "US without NY Deaths",
                "US without NY Deaths Daily",
                "US without NY Deaths 7-Day",
            ],
        },
"""[1:-1]


SHEET_OUTPUT_TEMPLATE = """
        {{
            // {code}
            "spreadsheet_id": "{sheet_id}",
            "sheet_name": "Source Data",
            "table": "{code}",
        }},
"""[1:-1]

NATIONAL_SHEET_OUTPUTS = """
        {
            // US
            "spreadsheet_id": "1xmEkDRZUZQefsD9yll24Q_VyTYaRteIvplok6S8JRMg",
            "sheet_name": "Source Data",
            "table": "US",
        },
        {
            // US without NY
            "spreadsheet_id": "1-IC22hnPHnmueM1g99PZkuvP5bLtAm_0_1bYMgrKGSY",
            "sheet_name": "Source Data",
            "table": "US without NY",
        },
"""[1:-1]


def main():
  state_codes = sorted(US_STATE_SHEETS.keys())

  print(FILE_HEADER_TEMPLATE)

  print(SECTION_HEADER_TEMPLATE.format(section='regions'))
  for code in state_codes:
    print(REGION_TEMPLATE.format(code=code))
  print(NATIONAL_REGIONS)
  print(SECTION_TRAILER_TEMPLATE)

  print(SECTION_HEADER_TEMPLATE.format(section='region_queries'))
  for code in state_codes:
    print(REGION_QUERY_TEMPLATE.format(code=code))
  print(NATIONAL_REGION_QUERIES)
  print(SECTION_TRAILER_TEMPLATE)

  print(SECTION_HEADER_TEMPLATE.format(section='filtered_queries'))
  for code in state_codes:
    print(FILTERED_QUERY_TEMPLATE.format(code=code))
  print(NATIONAL_FILTERED_QUERIES)
  print(SECTION_TRAILER_TEMPLATE)

  print(SECTION_HEADER_TEMPLATE.format(section='report_tables'))
  for code in state_codes:
    if code in US_STATE_SHEETS and US_STATE_SHEETS[code]:
      print(REPORT_TABLE_TEMPLATE.format(
          code=code, sheet_id=US_STATE_SHEETS[code]))
  print(NATIONAL_REPORT_TABLES)
  print(SECTION_TRAILER_TEMPLATE)

  print(SECTION_HEADER_TEMPLATE.format(section='sheet_outputs'))
  for code in state_codes:
    if code in US_STATE_SHEETS and US_STATE_SHEETS[code]:
      print(SHEET_OUTPUT_TEMPLATE.format(
          code=code, sheet_id=US_STATE_SHEETS[code]))
  print(NATIONAL_SHEET_OUTPUTS)
  print(SECTION_TRAILER_TEMPLATE)

  print(FILE_TRAILER_TEMPLATE)

if __name__ == '__main__':
  main()
