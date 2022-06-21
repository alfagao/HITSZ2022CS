import numpy as np

y = np.array([1, 1])
y_hat = np.array([2, 3])
## 利用范数实现
"""
## MSE--相当于y-y_hat的二阶范数的平方/n
MSE = np.linalg.norm(y - y_hat, ord=2) ** 2 / len(y)
## RMSE--相当于y-y_hat的二阶范数/根号n
RMSE = np.linalg.norm(y - y_hat, ord=2) / len(y) ** 0.5
## MAE--相当于y-y_hat的一阶范数/n
MAE = np.linalg.norm(y - y_hat, ord=1) / len(y)
"""
## 自己写
MSE = np.mean(np.square(y - y_hat))
RMSE = np.sqrt(np.mean(np.square(y - y_hat)))
MAE = np.mean(np.abs(y - y_hat))
MAPE = np.mean(np.abs((y - y_hat) / y)) * 100
print(MSE)
print(RMSE)
print(MAE)
print(MAPE)
