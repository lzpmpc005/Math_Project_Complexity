# modified from the originial code: 
# https://high-python-ext-3-algorithms.readthedocs.io/ko/latest/chapter8.html

import time

class Item(object):

    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

def get_maximum_value(items, capacity):
    dp = [0] * (capacity + 1)
    for item in items:
        dp_tmp = [total_value for total_value in dp]
        for current_weight in range(capacity + 1):
            total_weight = current_weight + item.weight
            if total_weight <= capacity:
                dp_tmp[total_weight] = max(dp_tmp[total_weight], dp[current_weight] + item.value)
        dp = dp_tmp
    return max(dp)

with open("dataset.txt", 'r') as file:
    lines = file.readlines()
    items = [Item(*map(int, line.strip().split())) for line in lines]

trial = 5
capacity = 50

with open("dynamic_results.txt", 'w') as result_file:
    for n in range(1, 501):
        trial_times = []
        for _ in range(trial):
            start_time = time.time()
            get_maximum_value(items[:n], capacity)
            end_time = time.time()
            exe_time = end_time - start_time
            trial_times.append(str(exe_time))
        
        result_file.write(f"n={n}: {','.join(trial_times)}\n")