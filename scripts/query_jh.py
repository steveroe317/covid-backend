#!/usr/bin/env python3

import argparse
import json
import os
import sys
import time
from collections import deque

import json5

from filters import (run_daily_filter, run_gap_fill_filter,
                     run_rolling_average_filter)
from firebase_entities import write_firebase_entities
from johns_hopkins_journal import JohnsHopkinsJournal
from johns_hopkins_query import (AdminArea, CsvOutput, FilteredQuery,
                                 FirebaseOutput, QueryReport, Region,
                                 RegionQuery, SheetOutput)
from results_tables import make_results_table, make_tagged_results_table
from sheets_client import ColumnRange, WriteSheet
from utils import collapse_data_sets

# Throttle writes to Google Sheets to stay under writes per 100 seconds quota.
_WRITE_SLEEP_SEC = 10

COVID_CSV_DIR = os.path.join(
    'data',
    'COVID-19',
    'csse_covid_19_data',
    'csse_covid_19_daily_reports')


def init_parser():
    parser = argparse.ArgumentParser(
        description='analyze covid-19 data from John Hopkins csv files')

    parser.add_argument(
        '--covid-csv-dir',
        default=COVID_CSV_DIR,
        metavar='DIR_PATH',
        help='directory containing covid-19 csv files'
    )
    parser.add_argument(
        '--query',
        metavar='QUERY.JSON5',
        help='json5 format query'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='count',
        default=0
    )

    return parser


def find_region(region_name, regions):
    for region in regions:
        if region.name == region_name:
            return region
    raise ValueError('Could not find region "%s"' % region_name)


def sum_region_data(areas, data_key, journal):
    data_set = {}
    for area in areas:
        # print('AREA: ' + str(area))
        if area.country() is None:
            data_set = collapse_data_sets(data_set,
                                          journal.get_world_data([data_key]))
        elif area.state() is None:
            data_set = collapse_data_sets(data_set,
                                          journal.get_country_data(area.country(),
                                                                   [data_key]))
        elif area.county() is None:
            data_set = collapse_data_sets(data_set,
                                          journal.get_state_data(area.state(),
                                                                 area.country(),
                                                                 [data_key]))
        else:
            data_set = collapse_data_sets(data_set,
                                          journal.get_county_data(area.county(),
                                                                  area.state(),
                                                                  area.country(),
                                                                  [data_key]))
        # print(data_set)
    return data_set


# TODO: implement actual exclusion, not just subtraction of the exclude list.
def run_region_query(region, data_key, journal):
    include_data_set = sum_region_data(region.include, data_key, journal)
    exclude_data_set = sum_region_data(region.exclude, data_key, journal)

    data_set = {}
    dates = set(include_data_set.keys()) | set(exclude_data_set.keys())
    for date in dates:
        data_set[date] = 0
        if date in include_data_set:
            data_set[date] += include_data_set[date]
        if date in exclude_data_set:
            data_set[date] -= exclude_data_set[date]
    return data_set


def run_region_queries(region_queries, regions, journal):
    query_results = {}
    for query in region_queries:
        region = find_region(query.region, regions)
        query_results[query.name] = run_region_query(region, query.data_key,
                                                     journal)
    return query_results


def run_filtered_query(filter, source):
    if filter == 'daily':
        return run_daily_filter(source)
    elif filter == 'gap-fill':
        return run_gap_fill_filter(source)
    elif filter == '7-day':
        return run_rolling_average_filter(source, 7)
    else:
        raise ValueError('Unknown query filter "%s"' % filter)


def run_filtered_queries(filtered_queries, query_results):
    for query in filtered_queries:
        query_results[query.name] = run_filtered_query(
            query.filter,  query_results[query.source])


def make_report_tables(report_tables, query_results, tables):
    for report_table in report_tables:
        rows = make_results_table(report_table.queries, query_results)
        tables[report_table.name] = rows


def make_tagged_report_tables(tagged_report_tables, query_results, tables):
    for report_table in tagged_report_tables:
        tags = report_table.tags_bundle.split(':')
        rows = make_tagged_results_table(
            tags, report_table.queries, query_results)
        tables[report_table.name] = rows


def write_csv_output(csv_output, tables, verbose):
    if verbose:
        print(csv_output.table)
    rows = tables[csv_output.table]
    with open(csv_output.filepath, 'w') as csv_file:
        for row in rows:
            csv_file.write(','.join(row) + '\n')


def write_csv_outputs(csv_outputs, tables, verbose):
    for csv_output in csv_outputs:
        write_csv_output(csv_output, tables, verbose)


def write_sheet_output(sheet_output, tables, verbose):
    if verbose:
        print(sheet_output.table)
    rows = tables[sheet_output.table]
    range = ColumnRange(sheet_output.sheet_name, rows)
    WriteSheet(sheet_output.spreadsheet_id, range, rows)


def write_sheet_outputs(sheet_outputs, tables, verbose):
    for sheet_output in sheet_outputs:
        write_sheet_output(sheet_output, tables, verbose)
        time.sleep(_WRITE_SLEEP_SEC)


def main():
    parser = init_parser()
    args = parser.parse_args()

    query_file = open(args.query, 'r')
    query_spec = json5.load(query_file)

    query_report = QueryReport.create(query_spec)

    journal = JohnsHopkinsJournal(args.covid_csv_dir)
    query_results = run_region_queries(query_report.region_queries,
                                       query_report.regions, journal)

    run_filtered_queries(query_report.filtered_queries, query_results)

    tables = {}
    make_report_tables(query_report.report_tables, query_results, tables)
    make_tagged_report_tables(query_report.tagged_report_tables, query_results,
                              tables)

    write_csv_outputs(query_report.csv_outputs, tables, args.verbose)
    write_sheet_outputs(query_report.sheet_outputs, tables, args.verbose)
    write_firebase_entities(
        query_report.firebase_outputs, tables, args.verbose)


if __name__ == '__main__':
    main()
