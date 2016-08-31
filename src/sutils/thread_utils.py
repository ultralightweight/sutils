
from threading import Thread
from queue import Queue, Empty


from .primitivies import qlist
__all__ = qlist()

# ---------------------------------------------------
# UnexpectedEndOfStream
# ---------------------------------------------------

@__all__.register
class UnexpectedEndOfStream(Exception): pass


# ---------------------------------------------------
# NonBlockingStreamReader
# ---------------------------------------------------
# origin: https://gist.github.com/EyalAr/7915597#file-nbstreamreader-py

@__all__.register
class NonBlockingStreamReader(object):

    def __init__(self, stream):
        """
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        """

        self._s = stream
        self._q = Queue()

        def _populateQueue(stream, queue):
            """
            Collect lines from 'stream' and put them in 'quque'.
            """
            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    raise UnexpectedEndOfStream

        self._t = Thread(target = _populateQueue,
                args = (self._s, self._q))
        self._t.daemon = True
        self._t.start() #start collecting lines from the stream

    def readline(self, timeout = None):
        try:
            return self._q.get(block = timeout is not None,
                    timeout = timeout)
        except Empty:
            return None

