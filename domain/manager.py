import threading
import time
from queue import Queue

from tcp_factory import TCPWorkerFactory


class Manager(threading.Thread):
    def __init__(self,
                 worker_factory: "TCPWorkerFactory",
                 result_struct,
                 input_args):
        super().__init__()
        self.worker_factory = worker_factory
        self.result_struct = result_struct
        self.worker_factory.set_resulter(self.result_struct)
        self.input_args = input_args
        self.is_stopped = False

    def run(self):
        queue = Queue()
        for i in range(10000, 10000 + self.input_args.max_count):
            queue.put(i)
        for seq in range(self.input_args.max_count):
            if self.is_stopped:
                return
            worker = self.worker_factory.make(
                self.input_args.timeout,
                self.input_args.src,
                self.input_args.host,
                self.input_args.port,
                queue,
                seq,
            )
            worker.start()
            time.sleep(self.input_args.nseconds)
        queue.join()
