""" Functions producing result tables from query lists."""

import sys

from collections import defaultdict


""" Create a results table from a list of queries.

The table column names are "Date" plus the query names.  The table rows
are the date plus the query results for the date.

Args:
    queries: list of query names.
    query results: mapping from query name to query results by date.

Returns a results table with a header row and data rows.
"""


def make_results_table(queries, query_results):

    dates = set()
    for query_name in queries:
        dates |= set(query_results[query_name].keys())

    header_row = ['Date'] + queries
    rows = [header_row]
    for date in sorted(dates):
        data_row = [date] + [
            str(query_results[name][date]) for name in queries]
        rows.append(data_row)

    return rows


""" Create a tagged results table from a list of tags and a list of queries.

The query names are tag values plus a metric name, separated by ':'.  The
number of tag values in the query names must match the number of tags passed
to the function.

The table column names are "Date" plus the tag column names plus the query
metric names.  The table column rows are the date plus the query name tag
values plus the query results for the date.

Args:
    tags: list of tag column names.
    queries: list of query names.
    query results: mapping from query name to query results by date.

Returns a results table with a header row and data rows.
"""


def make_tagged_results_table(tags, queries, query_results):

    dates = set()
    for query_name in queries:
        dates |= set(query_results[query_name].keys())

    tagged_results = {}
    for date in dates:
        tagged_results[date] = {}
        for name in queries:
            tokens = name.split(':')
            tag_tuple = tuple(tokens[:-1])
            metric_name = tokens[-1]
            if tag_tuple not in tagged_results[date]:
                tagged_results[date][tag_tuple] = defaultdict(int)
            tagged_results[
                date][tag_tuple][metric_name] = query_results[name][date]

    metric_names = set()
    for date in dates:
        for tag_tuple in tagged_results[date].keys():
            metric_names |= set(tagged_results[date][tag_tuple].keys())
    metric_columns = sorted(metric_names)

    header_row = ['Date'] + tags + metric_columns
    rows = [header_row]
    for date in sorted(dates):
        for tag_tuple in sorted(tagged_results[date].keys()):
            data_row = [date]
            data_row.extend(tag_tuple)
            for metric in metric_columns:
                data_row.append(str(tagged_results[date][tag_tuple][metric]))
            rows.append(data_row)

    return rows


def table_column_tail(table, column_index, tail_size):
    """Returns the last N integer values ot a table column as a list.

    The column nust contain integer data.  The column name is not returned.
    If there are not N values in the column, all values will be returned.

    Args:
        table: a query result table.
        column_index: specifies the column to return.
        tail_size: the number of entries to return.
    """
    tail_start = max(1, len(table) - tail_size)
    tail = []
    for row in range(tail_start, len(table)):
        tail.append(int(table[row][column_index]))
    return tail
