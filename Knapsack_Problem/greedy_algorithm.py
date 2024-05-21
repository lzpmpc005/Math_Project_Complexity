from fractions import Fraction
import time

class KnapsackPackage(object):

    def __init__(self, value, weight):
        self.weight = weight
        self.value = value
        self.cost = value / weight

    def __lt__(self, other):
        return self.cost < other.cost

class FractionalKnapsack(object):
    def knapsackGreProc(self, W, V, M, n):
        packs = []
        for i in range(n):
            packs.append(KnapsackPackage(W[i], V[i]))
        packs.sort(reverse=True)
        remain = M
        result = 0
        for pack in packs:
            if remain >= pack.weight:
                result += pack.value
                remain -= pack.weight
            else:
                fraction = Fraction(remain, pack.weight)
                result += fraction * pack.value
                break
        return result

with open("dataset.txt", 'r') as file:
    lines = file.readlines()
    items = [KnapsackPackage(*map(int, line.strip().split())) for line in lines]

trial = 5 
M = 50

with open("greedy_results.txt", 'w') as result_file:
    for n in range(1, 501):
        trial_times = []
        for _ in range(trial):
            start_time = time.time()
            FractionalKnapsack().knapsackGreProc([item.weight for item in items[:n]], [item.value for item in items[:n]], M, n)
            end_time = time.time()
            exe_time = end_time - start_time
            trial_times.append(str(exe_time))
        
        result_file.write(f"n={n}: {','.join(trial_times)}\n")
