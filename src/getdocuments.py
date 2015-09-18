"""This spout connects to rabbitmq and gets messages off a queue.
It will map tuples to queues, and when told to ack a tuple, it will ack the
relevant message as well.
"""
import Queue

from streamparse import spout
import kombu

import genuid, settings


class GetDocumentsSpout(spout.Spout):

    def initialize(self, stormconf, context):
        self.source_queue = get_source_queue(settings.SOURCE)
        self.open_messages = {}

    def next_tuple(self):
        try:
            message = self.source_queue.get(block=False)
        except Queue.Empty:
            # This is fine. It's just that we have no messages at this point.
            return

        tuple_id = genuid.genuid()
        self.open_messages[tuple_id] = message

        payload_as_tuple = (message.payload,)
        self.log(u"about to emit {0} {1}".format(tuple_id, payload_as_tuple))
        self.emit(payload_as_tuple, tup_id=tuple_id)

    def ack(self, tuple_id):
        message = self.open_messages[tuple_id]
        self.log(u"about to ack {0} {1}".format(tuple_id, message.payload))
        message.ack()

        # We are done with the message!
        del self.open_messages[tuple_id]

    def fail(self, tuple_id):
        """Mark a tuple as failed. We put it back on the rabbitmq queue so
        it is processed again. So, we only want to fail tuples that we think
        might succeed if we try again (e.g. a host down erroe).
        """
        message = self.open_message[tuple_id]
        self.log(u"about to fail {0} {1}".format(tuple_id, message.payload))
        message.requeue()

        del self.open_messages[tuple_id]


def get_source_queue(source_setting):
    """Connect to a rabbitmq queue.
    """
    rabbitmq_host, queue_name = source_setting[:2]
    if len(source_setting) > 2:
        kwargs = source_setting[2]
    else:
        kwargs = {}

    broker = kombu.BrokerConnection(rabbitmq_host)
    return broker.SimpleQueue(queue_name, **kwargs)
