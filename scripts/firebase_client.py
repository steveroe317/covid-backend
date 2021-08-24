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


class FirebaseBatchWriter:
    DOCUMENT_WRITE_LIMIT = 200

    def __init__(self):
        self.documents = {}
        self.cred = _Authorize()

    def write(self, document_path, document_dict):
        self.documents[document_path] = document_dict
        if len(self.documents) >= FirebaseBatchWriter.DOCUMENT_WRITE_LIMIT:
            self.flush()

    def flush(self):
        db = firestore.Client("covid-trends-1fafa", self.cred)
        batch = db.batch()

        for document_path in sorted(self.documents.keys()):
            # 2 document access calls per document.
            document_ref = db.document(document_path)
            batch.set(document_ref, self.documents[document_path])

        batch.commit()
        self.documents = {}


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
