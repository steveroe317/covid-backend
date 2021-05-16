#!/usr/bin/env python3

import functools

from google.cloud import firestore
from google.oauth2 import service_account


@functools.cache
def _Authorize():
    return service_account.Credentials.from_service_account_file(
        'covid-trends-1fafa-firebase-adminsdk.json')


def WriteFirebaseDocument(document_path, document_dict):
    print(document_path)
    cred = _Authorize()
    db = firestore.Client("covid-trends-1fafa", cred)
    doc_ref = db.document(document_path)
    doc_ref.set(document_dict)


def main():
    cred = _Authorize()
    db = firestore.Client("covid-trends-1fafa", cred)
    doc_ref = db.collection(u'test').document(u'World')
    doc_ref.set({
        u'Confirmed': [13, 17, 21]
    })

    time_series_ref = db.collection(u'time-series')

    for doc in db.get_all(time_series_ref.list_documents()):
        # print(doc)
        print(u'{} => {}'.format(doc.id, doc.to_dict()))


if __name__ == '__main__':
    main()
