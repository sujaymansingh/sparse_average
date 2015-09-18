"""Index results to a file.
"""
import json

from streamparse import bolt

import settings


class IndexBolt(bolt.Bolt):

    def process(self, tup):
        self.log(u"Indexing: {0}".format(tup))
        document = tup.values[0]
        with open(settings.DEST, "a") as out:
            json.dump(document, out, sort_keys=True)
            out.write("\n")
