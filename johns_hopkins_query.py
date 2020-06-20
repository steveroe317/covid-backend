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
        fields = text.split(':')
        country = fields[0] if len(fields) > 0 else None
        state = fields[1] if len(fields) > 1 else None
        county = fields[2] if len(fields) > 2 else None
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
            exclude = [AdminArea.create(text) for text in region_dict['exclude']]
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


class SheetOutput:
    """Specifies a Google spreadsheet output range."""

    @classmethod
    def create(cls, output_dict):
        spreadsheet_id = _get_required_value(output_dict, 'SheetOutput',
                                             'spreadsheet_id')
        sheet_name = _get_required_value(output_dict, 'SheetOutput',
                                         'sheet_name')
        if 'queries' not in output_dict:
            raise ValueError(
                'SheetOutput "%s" missing queries' % spreadsheet_id)
        queries = [text for text in output_dict['queries']]
        return SheetOutput(spreadsheet_id, sheet_name, queries)

    def __init__(self, spreadsheet_id, sheet_name, queries):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.queries = queries

    def __str__(self):
        return 'spreadsheet_id: %s, sheet_name: %s, queries: %s' % (
            self.spreadsheet_id, self.sheet_name, self.queries)


class CsvOutput:
    """Specifies a CSV file output."""

    @classmethod
    def create(cls, output_dict):
        filepath = _get_required_value(output_dict, 'CsvOutput',
                                             'filepath')
        if 'queries' not in output_dict:
            raise ValueError(
                'CsvOutput "%s" missing queries' % filepath)
        queries = [text for text in output_dict['queries']]
        return CsvOutput(filepath, queries)

    def __init__(self, filepath, queries):
        self.filepath = filepath
        self.queries = queries

    def __str__(self):
        return 'filepath: %s, queries: %s' % (self.filepath, self.queries)


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
        sheet_outputs = _get_optional_object_list(
            reports_dict, 'reports', 'sheet_outputs', SheetOutput.create)
        csv_outputs = _get_optional_object_list(
            reports_dict, 'reports', 'csv_outputs', CsvOutput.create)

        return QueryReport(regions, reqion_queries, filtered_queries,
                           sheet_outputs, csv_outputs)

    def __init__(self, regions, reqion_queries, filtered_queries,
                 sheet_outputs, csv_outputs):
        self.regions = regions
        self.region_queries = reqion_queries
        self.filtered_queries = filtered_queries
        self.sheet_outputs = sheet_outputs
        self.csv_outputs = csv_outputs

    def __str__(self):
        return ('regions: %s, region_queries: %s, filtered_queries: %s'
                'sheet_outputs: %s, csv_outputs: %s' % (
                [str(region) for region in self.regions],
                [str(query) for query in self.region_queries],
                [str(query) for query in self.filtered_queries],
                [str(sheet) for sheet in self.sheet_outputs],
                [str(csv) for csv in self.csv_outputs]))