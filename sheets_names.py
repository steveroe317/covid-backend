#!/usr/bin/env python3

import collections

SheetRange = collections.namedtuple('SheetRange', ['id', 'range'])

SheetInfo = {
    'countries_group_1': SheetRange(
        '1ekUPoo2pCTkdevK0y5CFLNvDYPoLo2oCOCfrgU5WuzQ',
        'countries_group_1!A:O'
    ),
    'states_group_1': SheetRange(
        '1Xn_xiVgot0zFpk65EIWyfE0iW-jQOXf5sNsdofpOoE8',
        'states_group_1!A:O'
    ),
    'usa': SheetRange(
        '1Rz9jxXhuT_qwkujlU35llzlcLyxj51fvlA9re4Wx22g', 
        'Source Data!A:D'
    ),
}
