import random
import sys

import kombu


def create_document():
    num_values = random.choice([5, 6, 10])
    values = [random.randint(1, 100) for n in range(num_values)]
    return {"values": values}


if __name__ == "__main__":
    broker = kombu.BrokerConnection(sys.argv[1])
    queue = broker.SimpleQueue(sys.argv[2])

    num_documents = int(sys.argv[3])

    for i in range(num_documents):
        document = create_document()
        print u"Publishing {0}".format(document)
        queue.put(document)
