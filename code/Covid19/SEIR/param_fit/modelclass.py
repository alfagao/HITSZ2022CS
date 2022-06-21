import numpy as np
from scipy.integrate import odeint, solve_ivp


def mSEIR(t, Y, args):
    S, E, I, R = Y
    alpha = 0.2
    gamma = 1/25
    beta1, beta2 = args
    # I, E 均具有传染性, 且分别以beta1, beta2的概率使S转为E
    # 对于 E , 有 alpha 的概率 变为 感染者
    # 对于 I , 有 gamma 的概率 变为 康复者
    return np.array([-S*(beta1*I+beta2*E), S*(beta1*I+beta2*E)-alpha*E, alpha*E-gamma*I, gamma*I])

def SEIR(t, Y, args):
    S, E, I, R = Y
    alpha = 0.2
    gamma = 2/45
    beta = args[0]
    # I具有传染性, 且以beta的概率使S转为E
    return np.array([-S*(beta*I), S*(beta*I)-alpha*E, alpha*E-gamma*I, gamma*I])

# RMSE
def loss(opt, actual_data, Y0, weights, model=mSEIR):
    t = np.arange(0, len(actual_data[0]), 1)
    y = odeint(model, Y0, t, args=(list(opt),), tfirst=True)
    c = [(weights[i]*np.sqrt(np.mean(np.square(y[:, i] - actual_data[i])))) for i in range(len(actual_data))]
    # print(f"loss: {np.sum(c)}")
    return np.sum(c)

def MAELoss(y, y_hat, weights):
    return np.sum(
        [(weights[i] * (np.mean(np.abs(y[i] - y_hat[i])))) for i in range(len(weights))]
    )

def RMSELoss(y, y_hat, weights):
    return np.sum(
        [(weights[i] * (np.sqrt(np.mean(np.square(y[i] - y_hat[i]))))) for i in range(len(weights))]
    )
