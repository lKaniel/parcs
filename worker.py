from Pyro4 import expose, Daemon, locateNS
import Solver
import sys

class Worker:
    def __init__(self):
        self.solver = Solver.Solver()

    @expose
    def mymap(self, a, b, count):
        return self.solver.mymap(a, b, count)

    @expose
    def myreduce(self, mapped):
        return self.solver.myreduce(mapped)

if __name__ == "__main__":
    # Register the worker with the Pyro nameserver
    worker = Worker()
    daemon = Daemon()
    ns = locateNS()
    uri = daemon.register(worker)
    ns.register("example.worker" + sys.argv[1], uri)
    print(f"Worker {sys.argv[1]} ready.")
    daemon.requestLoop()
