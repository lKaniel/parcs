from Pyro4 import Proxy, locateNS
import Solver

if __name__ == "__main__":
    ns = locateNS()
    workers = [Proxy("PYRONAME:example.worker" + str(i)) for i in range(1, 4)]  # Adjust the range as needed
    solver = Solver.Solver(workers, 'input.txt', 'output.txt')
    solver.solve()
