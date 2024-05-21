import matplotlib.pyplot as plt
import numpy as np

n_values = []
average_times = []

with open("dynamic_results.txt", 'r') as result_file:
    for line in result_file:
        parts = line.strip().split(': ')
        n_values.append(int(parts[0][2:]))
        times = parts[1].split(',')
        average_time = sum(map(float, times)) / len(times)
        average_times.append(average_time)

poly_coeffs = np.polyfit(n_values, average_times, 1)
poly_func = np.poly1d(poly_coeffs)

residuals = average_times - poly_func(n_values)
mse = np.mean(residuals**2)
rmse = np.sqrt(mse)
mae = np.mean(np.abs(residuals))

ss_total = np.sum((average_times - np.mean(average_times))**2)
ss_residual = np.sum(residuals**2)
r_squared = 1 - (ss_residual / ss_total)
r = np.sqrt(r_squared)

print("Linear Fit Parameters:", poly_coeffs)
print("MSE:", mse)
print("RMSE:", rmse)
print("MAE:", mae)
print("R^2", r_squared)
print("R:", r)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.scatter(n_values, average_times, label='Average Runtime', color='black')
plt.plot(n_values, poly_func(n_values), color='red', label='Linear Fit')
plt.xlabel('Number of Items Input')
plt.ylabel('Average Runtime')
plt.title('Fit Plot of Experiment 1')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.scatter(n_values, residuals, label='Residuals', color='blue', marker='x')
plt.xlabel('Number of Items Input')
plt.ylabel('Residuals')
plt.title('Residuals Plot of Experiment 1')
plt.axhline(y=0, color='black', linestyle='--')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
