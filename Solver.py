from Pyro4 import expose
import random
import time

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        current_timestamp = time.time()
        print("Current Timestamp:", current_timestamp)

        (n, k) = self.read_input()
        a = 1 << n
        b = 1 << (n + 1)
        step_n = (b - a) // len(self.workers)
        step_k = k // len(self.workers)

        # map
        mapped = []
        for i in range(len(self.workers)):
            print("map %d" % i)
            start_range = a + i * step_n
            end_range = a + (i + 1) * step_n
            mapped.append(self.workers[i].mymap(str(start_range), str(end_range), step_k))

        # reduce
        primes = self.myreduce(mapped)

        # output
        self.write_output(primes)

        print("Job Finished")
        current_timestamp_2 = time.time()
        print("Current Timestamp:", current_timestamp_2)
        print("total time: ",  current_timestamp_2 - current_timestamp)

    @staticmethod
    @expose
    def mymap(a, b, count):
        print(a)
        print(b)
        print(count)
        a = int(a)
        b = int(b)
        count = int(count)  # Ensure count is an integer
        primes = []

        if a % 2 == 0:
            a += 1

        while len(primes) < count and a < b:
            if Solver.is_probable_prime(a):
                primes.append(str(a))
            a += 2

        return primes

    @staticmethod
    @expose
    def myreduce(mapped):
        print("reduce")
        output = []

        for primes in mapped:
            print("reduce loop")
            output += primes  # Directly concatenate the lists
        print("reduce done")
        return output

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            n = int(f.readline())
            k = int(f.readline())
        return n, k

    def write_output(self, output):
        with open(self.output_file_name, 'w') as f:
            f.write(', '.join(output))
            f.write('\n')
        print("output done")

    @staticmethod
    @expose
    def is_probable_prime(n):
        assert n >= 2
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        s = 0
        d = n - 1
        while True:
            quotient, remainder = divmod(d, 2)
            if remainder == 1:
                break
            s += 1
            d = quotient
        assert (2 ** s * d == n - 1)

        def try_composite(a):
            if pow(a, d, n) == 1:
                return False
            for i in range(s):
                if pow(a, 2 ** i * d, n) == n - 1:
                    return False
            return True

        for i in range(1):
            a = random.randrange(2, n)
            if try_composite(a):
                return False

        return True
