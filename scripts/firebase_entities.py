#!/usr/bin/env python3

import datetime
import numbers
import re

from firebase_client import WriteFirebaseDocument


class FirebaseEntity:

    def __init__(self, document_path, table_name):
        self._validate_document_path(document_path)
        self.path = tuple(document_path.split('/'))
        self.table_name = table_name
        self.table_rows = None
        self.name = document_path.split('/')[-1]
        self.parent = None
        self.children = set()
        self.sort_keys = {}

    def _validate_document_path(self, path):
        tokens = path.split('/')
        for index in range(2, len(tokens), 2):
            if tokens[index] != 'entities':
                raise ValueError('Document path "{path}" missing "entities" '
                                 f'collection at index {index}')

    def parent_path(self):
        return tuple(self.path[:-2])


def build_firebase_entity_tree(firebase_outputs, tables, verbose):
    """Builds tree based on firebase output document paths."""

    # Construct tree nodes from firebase outputs.
    entities = {}
    for firebase_output in firebase_outputs:
        entity = FirebaseEntity(firebase_output.document_path,
                                firebase_output.table)
        if entity.path in entities:
            raise ValueError(f'Duplicate firebase output path ${entity.path}')
        entities[entity.path] = entity
        if (verbose):
            print('Added entity', entity.path)

    # Add tree node table rows and sort keys.
    for entity in entities.values():
        entity.table_rows = tables[entity.table_name]
        entity.sort_keys = {}
        for index, column in enumerate(entity.table_rows[0]):
            last_column_value = entity.table_rows[-1][index]
            if last_column_value.isnumeric():
                column_metric = column.split(':')[-1]
                entity.sort_keys[column_metric] = int(last_column_value)
        if (verbose):
            print('Added rows and sort keys', entity.name, entity.sort_keys)

    # Add tree parent and child links based on document paths.
    for entity in entities.values():
        if entity.parent_path() in entities:
            entity.parent = entities[entity.parent_path()]
            entity.parent.children.add(entity)
        if (verbose):
            print('Added child parent links', entity.name,
                  entity.parent.name if entity.parent else 'root')

    # Find tree root.
    root = None
    for entity in entities.values():
        if not entity.parent:
            if not root:
                root = entity
            else:
                raise ValueError(f'Firebase outputs do not form a tree. '
                                 f'Multiple roots include ${root.path} and ${entity.path}')

    return root


def write_firebase_entity(entity, verbose):
    document_path = '/'.join(entity.path)
    if verbose:
        print(document_path)

    # Build Firebase document dictionary.
    document_dict = {}
    header_row = []
    for name in entity.table_rows[0]:
        tokens = name.split(':')
        header_row.append(tokens[-1])
    for field in header_row:
        document_dict[field] = []
    for row in entity.table_rows[1:]:
        for index, value in enumerate(row):
            if value.isnumeric():
                value = int(value)
            elif re.match(r'\d{4}-\d{2}-\d{2}$', value):
                value = datetime.datetime.fromisoformat(value)
            document_dict[header_row[index]].append(value)
    document_dict['Children'] = {}
    for child in entity.children:
        document_dict['Children'][child.name] = {}
        document_dict['Children'][child.name]['SortKeys'] = child.sort_keys
        document_dict['Children'][child.name]['HasChildren'] = True if child.children else False

    if verbose:
        print(f'Writing ${entity.path}')
    WriteFirebaseDocument(document_path, document_dict)


def write_firebase_entity_tree(root, verbose):
    if not root:
        return
    for node in root.children:
        write_firebase_entity_tree(node, verbose)
    write_firebase_entity(root, verbose)


def write_firebase_timestamp(document_path):
    timestamp_value = datetime.datetime.now(datetime.timezone.utc)
    document_dict = {'timestamp': timestamp_value}
    WriteFirebaseDocument(document_path, document_dict)


def write_firebase_entities(firebase_outputs, tables, verbose):
    if verbose:
        print('Writing data to firebase')
    entity_tree = build_firebase_entity_tree(firebase_outputs, tables, verbose)
    write_firebase_entity_tree(entity_tree, verbose)

    timestamp_path = '/'.join([entity_tree.path[0], 'Timestamp'])
    write_firebase_timestamp(timestamp_path)
