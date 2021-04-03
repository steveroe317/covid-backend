#!/usr/bin/env python3

import collections

import json5


def _get_required_value(source_dict, source_name, key):
    if key not in source_dict:
        raise ValueError('%s dictionary missing "%s"' % (source_name, key))
    return source_dict[key]


def _get_optional_value(source_dict, source_name, key):
    if key not in source_dict:
        return None
    return source_dict[key]


def _get_object_list(source_dict, key, create_func):
    return [create_func(object_dict) for object_dict in source_dict[key]]


def _get_required_object_list(source_dict, source_name, key, create_func):
    if key not in source_dict:
        print(source_dict)
        raise ValueError('"%s" dictionary missing "%s"' % (source_name, key))
    return _get_object_list(source_dict, key, create_func)


def _get_optional_object_list(source_dict, source_name, key, create_func):
    if key not in source_dict:
        return []
    return _get_object_list(source_dict, key, create_func)


AdminAreaTuple = collections.namedtuple('AdminAreaTuple',
                                        ['admin0', 'admin1', 'admin2'])


class AdminArea(AdminAreaTuple):
    """Specifies a administrative area from the Johns Hopkins dataset."""

    @classmethod
    def create(cls, text):
        if not isinstance(text, str):
            raise TypeError('AdminArea.create - text arg is not a string')

        # Extract admin area text fields.
        fields = text.split(':')
        country = fields[0] if len(fields) > 0 else None
        state = fields[1] if len(fields) > 1 else None
        county = fields[2] if len(fields) > 2 else None

        # Convert empty strings to None
        country = country if country else None
        state = state if state else None
        county = county if county else None

        return AdminArea(country, state, county)

    def __new__(cls, country='', state='', county=''):
        self = super(AdminArea, cls).__new__(cls, country, state, county)
        return self

    def __str__(self):
        return 'country: %s, state: %s, county: %s' % (
            self.admin0, self.admin1, self.admin2)

    def country(self):
        return self.admin0

    def state(self):
        return self.admin1

    def province(self):
        return self.admin1

    def county(self):
        return self.admin2


class Region:
    """Specifies a data grouping from the Johns Hopkins dataset."""

    @classmethod
    def create(cls, region_dict):
        if not isinstance(region_dict, dict):
            raise TypeError('Region.create requires a dictionary')
        name = _get_required_value(region_dict, 'Region', 'name')
        if 'include' not in region_dict:
            raise ValueError('Region "%s" missing include' % name)
        include = [AdminArea.create(text) for text in region_dict['include']]
        if 'exclude' in region_dict:
            exclude = [AdminArea.create(text)
                       for text in region_dict['exclude']]
        else:
            exclude = []
        return Region(name, include, exclude)

    def __init__(self, name, include, exclude=[]):
        self.name = name
        self.include = include
        self.exclude = exclude

    def __str__(self):
        return 'name: %s, include: %s, exclude: %s' % (
            self.name, self.include, self.exclude)


class RegionQuery:
    """Specifies a data grouping from the Johns Hopkins dataset."""

    @classmethod
    def create(cls, query_dict):
        name = _get_required_value(query_dict, 'RegionQuery', 'name')
        data_key = _get_required_value(query_dict, 'RegionQuery', 'key')
        region = _get_required_value(query_dict, 'RegionQuery', 'region')
        return RegionQuery(name, data_key, region)

    def __init__(self, name, data_key, region):
        self.name = name
        self.data_key = data_key
        self.region = region

    def __str__(self):
        return 'name: %s, data_key: %s, region: %s' % (
            self.name, self.data_key, self.region)


class FilteredQuery:
    """Specifies a filter for query data."""

    @classmethod
    def create(cls, query_dict):
        name = _get_required_value(query_dict, 'FilteredQuery', 'name')
        filter = _get_required_value(query_dict, 'FilteredQuery', 'filter')
        source = _get_required_value(query_dict, 'FilteredQuery', 'source')
        return FilteredQuery(name, filter, source)

    def __init__(self, name, filter, source):
        self.name = name
        self.filter = filter
        self.source = source

    def __str__(self):
        return 'name: %s, filter: %s, source: %s' % (
            self.name, self.filter, self.source)


class ReportTable:
    """Specifies a query report."""

    @classmethod
    def create(cls, output_dict):
        name = _get_required_value(output_dict, 'ReportTable', 'name')
        if 'queries' not in output_dict:
            raise ValueError(
                'ReportTable "%s" missing queries' % name)
        queries = [text for text in output_dict['queries']]
        return ReportTable(name, queries)

    def __init__(self, name, queries):
        self.name = name
        self.queries = queries

    def __str__(self):
        return 'name: %s, queries: %s' % (self.name, self.queries)


class TaggedReportTable:
    """Specifies a query report with tags extracted from query names."""

    @classmethod
    def create(cls, query_dict):
        name = _get_required_value(query_dict, 'TaggedReportTable', 'name')
        tags_bundle = _get_required_value(query_dict, 'TaggedReportTable',
                                          'tags_bundle')
        if 'queries' not in query_dict:
            raise ValueError(
                'TaggedReportTable "%s" missing queries' % name)
        queries = [text for text in query_dict['queries']]
        return TaggedReportTable(name, tags_bundle, queries)

    def __init__(self, name, tags_bundle, queries):
        self.name = name
        self.tags_bundle = tags_bundle
        self.queries = queries

    def __str__(self):
        return 'name: %s, tags_bundle: %s, queries: %s' % (
            self.name, self.tags_bundle, self.queries)


class SheetOutput:
    """Specifies a Google spreadsheet output range."""

    @classmethod
    def create(cls, output_dict):
        spreadsheet_id = _get_required_value(output_dict, 'SheetOutput',
                                             'spreadsheet_id')
        sheet_name = _get_required_value(output_dict, 'SheetOutput',
                                         'sheet_name')
        table = _get_required_value(output_dict, 'SheetOutput', 'table')
        return SheetOutput(spreadsheet_id, sheet_name, table)

    def __init__(self, spreadsheet_id, sheet_name, table):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.table = table

    def __str__(self):
        return 'spreadsheet_id: %s, sheet_name: %s, table: %s' % (
            self.spreadsheet_id, self.sheet_name, self.table)


class CsvOutput:
    """Specifies a CSV file output."""

    @classmethod
    def create(cls, output_dict):
        filepath = _get_required_value(output_dict, 'CsvOutput', 'filepath')
        table = _get_required_value(
            output_dict, 'SheetCsvOutputOutput', 'table')
        return CsvOutput(filepath, table)

    def __init__(self, filepath, table):
        self.filepath = filepath
        self.table = table

    def __str__(self):
        return 'filepath: %s, table: %s' % (self.filepath, self.table)


class FirebaseOutput:
    """Specifies a Google Firebase document output."""

    @classmethod
    def create(cls, output_dict):
        collection_path = _get_required_value(output_dict, 'FirebaseOutput',
                                              'collection_path')
        table = _get_required_value(output_dict, 'FirebaseOutput', 'table')
        return FirebaseOutput(collection_path, table)

    def __init__(self, collection_path, table):
        self.collection_path = collection_path
        self.table = table

    def __str__(self):
        return 'collection_path: %s, table: %s' % (self.collection_path,
                                                   self.table)


class QueryReport:
    """Specifies a set of queries and reports."""

    @classmethod
    def create(cls, reports_dict):
        regions = _get_required_object_list(
            reports_dict, 'reports', 'regions', Region.create)
        reqion_queries = _get_required_object_list(
            reports_dict, 'reports', 'region_queries', RegionQuery.create)
        filtered_queries = _get_optional_object_list(
            reports_dict, 'reports', 'filtered_queries', FilteredQuery.create)
        report_tables = _get_optional_object_list(
            reports_dict, 'reports', 'report_tables', ReportTable.create)
        tagged_report_tables = _get_optional_object_list(
            reports_dict, 'reports', 'tagged_report_tables',
            TaggedReportTable.create)
        sheet_outputs = _get_optional_object_list(
            reports_dict, 'reports', 'sheet_outputs', SheetOutput.create)
        csv_outputs = _get_optional_object_list(
            reports_dict, 'reports', 'csv_outputs', CsvOutput.create)
        firebase_outputs = _get_optional_object_list(
            reports_dict, 'reports', 'firebase_outputs', FirebaseOutput.create)

        return QueryReport(regions, reqion_queries, filtered_queries,
                           report_tables, tagged_report_tables, sheet_outputs,
                           csv_outputs, firebase_outputs)

    def __init__(self, regions, reqion_queries, filtered_queries,
                 report_tables, tagged_report_tables, sheet_outputs,
                 csv_outputs, firebase_outputs):
        self.regions = regions
        self.region_queries = reqion_queries
        self.filtered_queries = filtered_queries
        self.report_tables = report_tables
        self.tagged_report_tables = tagged_report_tables
        self.sheet_outputs = sheet_outputs
        self.csv_outputs = csv_outputs
        self.firebase_outputs = firebase_outputs

    def __str__(self):
        return ('regions: %s, region_queries: %s, filtered_queries: %s '
                'report_tables: %s, tagged_report_tables: %s, sheet_outputs: %s, '
                'csv_outputs: %s, firebase_outputs %s' % (
                    [str(region) for region in self.regions],
                    [str(query) for query in self.region_queries],
                    [str(query) for query in self.filtered_queries],
                    [str(table) for table in self.report_tables],
                    [str(table) for table in self.tagged_report_tables],
                    [str(sheet) for sheet in self.sheet_outputs],
                    [str(csv) for csv in self.csv_outputs],
                    [str(firebase) for firebase in self.firebase_outputs]))
