import random

n = 500
filename = "dataset.txt"


with open(filename, 'w') as file:
    for _ in range(n):
        value = random.randint(1, 100)
        weight = random.randint(1, 10)
        file.write(f"{value} {weight}\n")