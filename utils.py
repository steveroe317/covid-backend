#!/usr/bin/env python3

def print_csv(rows):
  for row in rows:
    print(','.join(row))


def collapse_data_sets(collapsed_data_set, full_data_set):
    dates = set(collapsed_data_set.keys()) | set(full_data_set.keys())
    data_set = {}
    for date in dates:
        data_set[date] = 0
        if date in collapsed_data_set:
            data_set[date] += collapsed_data_set[date]
        if date in full_data_set:
            data_set[date] += sum(full_data_set[date].values())
    return data_set