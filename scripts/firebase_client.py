#!/usr/bin/env python3

import datetime
import re

from google.cloud import firestore
from google.oauth2 import service_account


def _Authorize():
    return service_account.Credentials.from_service_account_file(
        'covid-trends-1fafa-firebase-adminsdk.json')


def WriteFirebaseDocuments(collection_path, values):
    doc_dict = {}
    header_row = values[0]
    for field in header_row:
        doc_dict[field] = []
    for row in values[1:]:
        for index, value in enumerate(row):
            if value.isnumeric():
                value = int(value)
            elif re.match(r'\d{4}-\d{2}-\d{2}$', value):
                value = datetime.datetime.fromisoformat(value)
            doc_dict[header_row[index]].append(value)

    cred = _Authorize()
    db = firestore.Client("covid-trends-1fafa", cred)
    doc_ref = db.collection(u'time-series').document(u'World')
    doc_ref.set(doc_dict)


def main():
    cred = _Authorize()
    db = firestore.Client("covid-trends-1fafa", cred)
    doc_ref = db.collection(u'time-series').document(u'World')
    doc_ref.set({
        u'Confirmed': [13, 17, 21]
    })

    time_series_ref = db.collection(u'time-series')

    for doc in db.get_all(time_series_ref.list_documents()):
        # print(doc)
        print(u'{} => {}'.format(doc.id, doc.to_dict()))


if __name__ == '__main__':
    main()
