from multiprocessing import Process, Queue


class EvalProcess(Process):
    """
    Class that handles a new thread behaviour for chromosome evaluation.
    """
    def __init__(self, queue: Queue, individual_queue: Queue):
        Process.__init__(self)
        self.queue = queue
        self.individual = individual_queue.get()

    def run(self):
        self.individual.eval()
        self.queue.put(self.individual)
