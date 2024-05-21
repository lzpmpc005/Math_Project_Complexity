from ortools.linear_solver import pywraplp
import time
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# 生成数据
num_items_list = [i for i in range(1, 101)]
execution_times = []

min_weight = 20
max_weight = 50
min_value = 10
max_value = 40

bin_capacities = [100, 100, 100, 100, 100]
num_bins = len(bin_capacities)
all_bins = range(num_bins)

# 主循环
for num_items in num_items_list:
    data = {}
    data["weights"] = [random.randint(min_weight, max_weight) for _ in range(num_items)]
    data["values"] = [random.randint(min_value, max_value) for _ in range(num_items)]
    assert len(data["weights"]) == len(data["values"])
    data["num_items"] = len(data["weights"])
    data["all_items"] = range(data["num_items"])

    # 使用SCIP后端创建MIP求解器。
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if solver is None:
        print("SCIP solver unavailable.")
        continue

    # 变量。
    # 如果项目i放入bin b，则x[i, b]为1。
    x = {}
    for i in data["all_items"]:
        for b in all_bins:
            x[i, b] = solver.BoolVar(f"x_{i}_{b}")

    # 约束条件。
    # 每个项目最多分配到一个bin。
    for i in data["all_items"]:
        solver.Add(sum(x[i, b] for b in all_bins) <= 1)

    # 每个bin中的总重量不能超过其容量。
    for b in all_bins:
        solver.Add(
            sum(x[i, b] * data["weights"][i] for i in data["all_items"])
            <= bin_capacities[b]
        )

    # 目标函数。
    # 最大化放入bin中项目的总价值。
    objective = solver.Objective()
    for i in data["all_items"]:
        for b in all_bins:
            objective.SetCoefficient(x[i, b], data["values"][i])
    objective.SetMaximization()

    start_time = time.time()
    status = solver.Solve()
    end_time = time.time()
    execution_times.append(end_time - start_time)

    # 打开一个文件，准备写入输出
    with open("output.txt", "w") as file:
        if status == pywraplp.Solver.OPTIMAL:
            file.write(f"Total packed value: {objective.Value()}\n")
            total_weight = 0
            for b in all_bins:
                file.write(f"Bin {b}\n")
                bin_weight = 0
                bin_value = 0
                for i in data["all_items"]:
                    if x[i, b].solution_value() > 0:
                        file.write(f"Item {i} weight: {data['weights'][i]} value: {data['values'][i]}\n")
                        bin_weight += data["weights"][i]
                        bin_value += data["values"][i]
                file.write(f"Packed bin weight: {bin_weight}\n")
                file.write(f"Packed bin value: {bin_value}\n\n")
                total_weight += bin_weight
            file.write(f"Total packed weight: {total_weight}\n")
        else:
            file.write("The problem does not have an optimal solution.\n")


    # 保存执行时间到文本文件
    with open("execution_times.txt", "w") as file:
        for i, exe_time in enumerate(execution_times):
            file.write(f"{num_items_list[i]},{exe_time}\n")
