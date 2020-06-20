#!/usr/bin/env python3

import argparse
import collections
import re
import os

from johns_hopkins_daily import JohnsHopkinsDaily
from johns_hopkins_journal import JohnsHopkinsJournal
from sheets_client import WriteSheet
from sheets_names import SheetInfo, SheetRange
from utils import collapse_data_sets
from utils import print_csv
from us_state_locations import convert_us_location_to_state
from us_state_locations import us_states_to_state_names


ColSpec = collections.namedtuple('ColSpec',
                                 ['label', 'data_key', 'country', 'state'])
ColGroupSpec = collections.namedtuple('ColGroupSpec', ['label', 'data_specs'])
DataSpec = collections.namedtuple('DataSpec', ['data_key', 'country', 'state'])


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
    '--sheet-id',
    metavar='ID',
    help='Google sheets long ID'
  )
  parser.add_argument(
    '--sheet-name',
    metavar='NAME',
    help='short name for Google sheets range to write'
  )
  parser.add_argument(
    '--sheet-range',
    metavar='RANGE',
    help='Google sheets range to write'
  )

  subparsers = parser.add_subparsers(help='sub-command help')

  parser_state_data = subparsers.add_parser(
      'state-data',
      help='list csv data for a specific state')
  parser_state_data.add_argument(
      '--state',
      default='WA',
      metavar='STATE',
      help='(WA, NY, ...')
  parser_state_data.set_defaults(func=state_data)

  parser_country_data = subparsers.add_parser(
      'country-data',
      help='list csv data for a specific country'
    )
  parser_country_data.add_argument(
      '--country',
      default='US',
      metavar='COUNTRY',
      help='(US, Ghana, ...')
  parser_country_data.set_defaults(func=country_data)

  parser_world_data = subparsers.add_parser(
      'world-data',
      help='list csv data for the whole world'
    )
  parser_world_data.set_defaults(func=world_data)

  parser_labelled_data = subparsers.add_parser(
    'labelled-data',
    help='list labelled csv data for world, country, and/or state.'
    )
  parser_labelled_data.add_argument(
      'label-region',
      action='store',
      nargs='*',
      help='list csv data - label, label:country, label:country:state',
      )
  parser_labelled_data.set_defaults(func=labelled_data)

  parser_labelled_groups = subparsers.add_parser(
    'labelled-groups',
    help='list labelled csv data for groups of world, country, and/or state.'
    )
  parser_labelled_groups.add_argument(
      '--region',
      action='append',
      nargs='+',
      help='list csv data - label [label:country, label:country:state] ...',
      )
  parser_labelled_groups.set_defaults(func=labelled_groups)

  parser_daily_keys = subparsers.add_parser(
    'daily-keys',
    help='show daily John Hopkins dataset keys (they may vary from day to day)')
  parser_daily_keys.add_argument('--condition',
    choices=['any', 'all', 'date'],
    default='any',
    help='show only keys for all date, keys for any dates, or keys by date')
  parser_daily_keys.set_defaults(func=daily_keys)

  parser_countries = subparsers.add_parser(
    'countries',
    help='show countries in data set')
  parser_countries.set_defaults(func=countries)

  parser_states = subparsers.add_parser(
    'states',
    help='show states (there may be variants)')
  parser_states.add_argument(
      '--country',
      default='US',
      metavar='COUNTRY',
      help='(US, Ghana, ...')
  parser_states.set_defaults(func=states)

  parser_country_locations = subparsers.add_parser(
    'country-locations',
    help='show country locations (counties, cruise ships, and so on')
  parser_country_locations.add_argument(
      '--country',
      default='US',
      metavar='COUNTRY',
      help='(US, Ghana, ...')
  parser_country_locations.set_defaults(func=country_locations)

  return parser


def resolve_args(args):
  if args.sheet_name is not None and not args.sheet_name in SheetInfo:
    raise ValueError('sheet name "%s" not recognized' % args.sheet_name)

  if args.sheet_id is None and args.sheet_name is not None:
    args.sheet_id = SheetInfo[args.sheet_name].id
  if args.sheet_range is None and args.sheet_name is not None:
    args.sheet_range = SheetInfo[args.sheet_name].range


def daily_keys(args):
  journal = JohnsHopkinsJournal(args.covid_csv_dir)

  if args.condition == 'date':
    date_to_keys = journal.daily_keys_by_date()
    for date in sorted(date_to_keys.keys()):
      print('{},{}'.format(date,','.join(sorted(date_to_keys[date]))))
  elif args.condition == 'any': 
      labels = journal.daily_keys_reduce(set.union)
      for label in sorted(labels):
        print(label)  
  elif args.condition == 'all':
      labels = journal.daily_keys_reduce(set.intersection)
      for label in sorted(labels):
        print(label)  
  else:
    raise ValueError('show-daily-keys condition "{}" not implemented'.format(
        args.condition))


def countries(args):
  journal = JohnsHopkinsJournal(args.covid_csv_dir)
  for country in sorted(journal.countries()):
    print(country)


def country_locations(args):
  journal = JohnsHopkinsJournal(args.covid_csv_dir)
  locations = journal.country_locations(args.country)
  for location in sorted(locations):
    print(location)


def states(args):
  journal = JohnsHopkinsJournal(args.covid_csv_dir)
  state_labels = journal.country_state_locations(args.country)

  states = set()
  for label in state_labels:
    states.add(convert_us_location_to_state(label))
  for state in sorted(states):
    print('{} - {}'.format(state, us_states_to_state_names[state]))

  for label in sorted(state_labels):
    if convert_us_location_to_state(label) == 'XX':
      print('warning: unknown state label "{}"'.format(label))


def state_data(args):
  resolve_args(args)
  journal = JohnsHopkinsJournal(args.covid_csv_dir)

  data_keys = ['Confirmed', 'Deaths']
  state_data = journal.get_state_data(args.state, 'US', data_keys)
  header_row = ['Date'] + data_keys
  rows = [header_row]
  for date in sorted(state_data.keys()):
    daily_data = [str(state_data[date][data_key]) for data_key in data_keys]
    data_row = [date] + daily_data
    rows.append(data_row)

  write_rows(args.sheet_id, args.sheet_range, rows)


def country_data(args):
  resolve_args(args)
  journal = JohnsHopkinsJournal(args.covid_csv_dir)

  data_keys = ['Confirmed', 'Deaths']
  country_data = journal.get_country_data(args.country, data_keys)
  header_row = ['Date'] + data_keys
  rows = [header_row]
  for date in sorted(country_data.keys()):
    daily_data = [str(country_data[date][data_key]) for data_key in data_keys]
    data_row = [date] + daily_data
    rows.append(data_row)

  write_rows(args.sheet_id, args.sheet_range, rows)


def world_data(args):
  resolve_args(args)
  journal = JohnsHopkinsJournal(args.covid_csv_dir)

  data_keys = ['Confirmed', 'Deaths']
  world_data = journal.get_world_data(data_keys)
  header_row = ['Date'] + data_keys
  rows = [header_row]
  for date in sorted(world_data.keys()):
    daily_data = [str(world_data[date][data_key]) for data_key in data_keys]
    data_row = [date] + daily_data
    rows.append(data_row)

  write_rows(args.sheet_id, args.sheet_range, rows)
  

def labelled_data(args):
  resolve_args(args)
  journal = JohnsHopkinsJournal(args.covid_csv_dir)

  col_specs = []
  for spec in args.__dict__['label-region']:
    fields = spec.split(':')
    if len(fields) < 3 or len(fields) > 4:
      raise ValueError(
          'arguments must be label:data_key:country or ' +
          'label:data_key:country:state')
    while len(fields) < 4:
      fields.append(None)
    col_specs.append(ColSpec(*fields))
    
  data_sets = {}
  for col_spec in col_specs:
    if col_spec.state is None:
      data_sets[col_spec] = journal.get_country_data(col_spec.country,
                                                       [col_spec.data_key])
    else:
      data_sets[col_spec] = journal.get_state_data(col_spec.state,
                                                   col_spec.country,
                                                   [col_spec.data_key])

  rows = []
  header_labels = ['Date']
  for col_spec in col_specs:
    header_labels.append(col_spec.label)
  rows.append(header_labels)

  for date in sorted(data_sets[col_specs[0]].keys()):
    data_fields = [date]
    for col_spec in col_specs:
      data_fields.append(str(data_sets[col_spec][date][col_spec.data_key]))
    rows.append(data_fields)

  write_rows(args.sheet_id, args.sheet_range, rows)


def labelled_groups(args):
  resolve_args(args)
  journal = JohnsHopkinsJournal(args.covid_csv_dir)

  col_group_specs = []
  for spec in args.__dict__['region']:
    group_label = spec[0]
    data_specs = []
    if len(spec) == 1:
      raise ValueError('labelled group "%" missing data specifications'
          % group_label)
    for data_spec in spec[1:]:
      fields = data_spec.split(':')
      if len(fields) < 2 or len(fields) > 3:
        raise ValueError(
            'arguments must be data_key:country or ' +
            'data_key:country:state - "%s"' % data_spec)
      while len(fields) < 3:
        fields.append(None)
      data_specs.append(DataSpec(*fields))
    col_group_specs.append(ColGroupSpec(group_label, tuple(data_specs)))

  data_sets = {}
  for col_group_spec in col_group_specs:
    data_sets[col_group_spec.label] = {}
    for data_spec in col_group_spec.data_specs:
      if data_spec.state is None:
        data_sets[col_group_spec.label] = collapse_data_sets(
          data_sets[col_group_spec.label],
          journal.get_country_data(data_spec.country, [data_spec.data_key]))
      else:
        data_sets[col_group_spec.label] = collapse_data_sets(
          data_sets[col_group_spec.label],
          journal.get_state_data(
            data_spec.state, data_spec.country, [data_spec.data_key]))

  rows = []
  header_labels = ['Date']
  for col_group_spec in col_group_specs:
    header_labels.append(col_group_spec.label)
  rows.append(header_labels)

  for date in sorted(data_sets[col_group_specs[0].label].keys()):
    data_fields = [date]
    for col_group_spec in col_group_specs:
      data_fields.append(
        str(data_sets[col_group_spec.label][date]))
    rows.append(data_fields)

  write_rows(args.sheet_id, args.sheet_range, rows)


def write_rows(sheet_id, sheet_range, rows):
  if sheet_id:
    WriteSheet(sheet_id, sheet_range, rows)
  else:
    print_csv(rows)


def main():
  parser = init_parser()
  args = parser.parse_args()
  args.func(args)


if __name__ == '__main__':
  main()
