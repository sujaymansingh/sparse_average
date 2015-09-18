"""Take a document that has a key values: list<int> and add the following keys
* total: the sum of all the values
* count: how many values
"""
import copy
import random

from streamparse import bolt


class SummariseBolt(bolt.Bolt):

    def process(self, tup):
        self.log(u"Received: {0}".format(tup))

        if random.choice([1, 2, 3, 4]) == 1:
            # This is to simulate a failure that we should retry. E.g. a host
            # being temporarily down etc.
            self.log(u"Failing: {0}".format(tup))
            self.fail(tup.id)
            return

        document = tup.values[0]
        self.log(u"Summarising: {0}".format(document))

        if not document.get("values"):
            # This is a failure from which we can not recover. So we don't
            # fail it, we just log and continue.
            self.log(u"Bad Document! No values")
        else:
            document_with_summary = summarise(document)
            next_tuple = (document_with_summary, )
            self.log(u"Done with original tuple: {0}".format(tup.id))
            self.emit(next_tuple)


def summarise(original_document):
    """Summarises a document by totaling and counting the values.

    >>> summarise({"values": [1, 2, 3]})
    {'count': 3, 'total': 6, 'values': [1, 2, 3]}
    """
    document = copy.deepcopy(original_document)

    values = document["values"]
    document["total"] = sum(values)
    document["count"] = len(values)

    return document
