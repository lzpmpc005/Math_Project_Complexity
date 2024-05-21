import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 读取文件并解析数据
filename = "execution_times.txt"
num_items_list = []
execution_times = []
with open(filename, 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            parts = line.split(", ")
            num_items = int(parts[0].split(": ")[1])
            exec_time = float(parts[1].split(": ")[1])
            num_items_list.append(num_items)
            execution_times.append(exec_time)

# 定义指数函数
def exponential_func(x, a, b):
    return a * np.exp(b * x)

# 计算数据的均值和标准差
mean_value = np.mean(execution_times)
std_dev = np.std(execution_times)

# 确定阈值，通常可以选择均值加减若干个标准差
threshold = 3 * std_dev

# 剔除极端值
cleaned_num_items_list = []
cleaned_execution_times = []
for i in range(len(num_items_list)):
    if abs(execution_times[i] - mean_value) < threshold:
        cleaned_num_items_list.append(num_items_list[i])
        cleaned_execution_times.append(execution_times[i])


# 使用清洗后的数据进行拟合
p0 = (mean_value, 0.0001)  # 初始参数值
popt_cleaned, pcov_cleaned = curve_fit(exponential_func, cleaned_num_items_list, cleaned_execution_times, p0=p0)

# 计算拟合的残差
residuals = np.array(cleaned_execution_times) - exponential_func(np.array(cleaned_num_items_list), *popt_cleaned)

# 计算残差平方和
rss = np.sum(residuals**2)

# 计算均方误差
mse = np.mean(residuals**2)

print("残差平方和 (RSS):", rss)
print("均方误差 (MSE):", mse)


# 输出拟合参数
print("拟合参数（剔除极端值后）:", popt_cleaned)

# 绘制数据和拟合曲线
plt.scatter(cleaned_num_items_list, cleaned_execution_times, label='Original Data')
plt.plot(cleaned_num_items_list, exponential_func(np.array(cleaned_num_items_list), *popt_cleaned), 'r', label='Exponential Fit')
plt.xlabel("Number of Items")
plt.ylabel("Execution Time (s)")
plt.title("Execution Time vs Number of Items")
plt.legend()
plt.show()

