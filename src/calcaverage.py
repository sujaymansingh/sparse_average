"""
"""
import copy

from streamparse import bolt


class CalcAverageBolt(bolt.Bolt):

    def process(self, tup):
        self.log(u"Received: {0}".format(tup))

        document = tup.values[0]
        self.log(u"Averaging: {0}".format(document))

        if document.get("count", 0) == 0:
            # We can't calculate an average here.
            self.log(u"Count is 0")
        else:
            document_with_average = calcaverage(document)
            next_tuple = (document_with_average, )
            self.log(u"Done with original tuple: {0}".format(tup.id))
            self.emit(next_tuple)


def calcaverage(original_document):
    """Summarises a document by totaling and counting the values.

    >>> calcaverage({"total": 6, "count": 3})
    {'count': 3, 'average': 2.0, 'total': 6}
    """
    document = copy.deepcopy(original_document)

    document["average"] = 1.0 * document["total"] / document["count"]

    return document
