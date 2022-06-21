"""
SEIR模型是经典的传染病模型，它将人群分为4类：
    易感者(susceptible)，健康但有可能感染病毒的人，总人数为 S ;
    潜伏者(exposed)，已感染病毒但仍未出现病症的人，总人数为 E;
    感染者(infected)，已感染病毒并出现病症的确诊患者，总人数为 I；
    康复者(removed)，感染病毒后因病死亡或成功治愈的人，总人数为 R。

符号说明:
    beta1: 潜伏者(E) 将病毒传染给 易感者(S) 的概率;
    beta2: 感染者(I) 将病毒传染给 易感者(S) 的概率;
    alpha: 潜伏者(E) 转化为 感染者(I) 的概率;
    gama:  感染者(I) 转化为 康复者(R) 的概率.
    s, e, i, r: 分别表示各类人群占比

SEIR的动力学方程为
    dS/dt = -s(beta1*E + beta2*I)
    dE/dt = -dS/dt - alpha*E
    dI/dt = alpha*E - gama*I
    dR/dt = gama*I
    S+E+I+R = N
"""
import numpy as np


# SI/SIR/SEIR/m-SEIR模型
# 1. SI模型: 仅把人群分为 S / I 两类, 适用于不可治愈的传染性疾病
def SI(y, t, args):
    S, I = y
    N = S + I
    beta = args
    return np.array([-(S / N) * (beta * I), (S / N) * (beta * I)])


# 2. SIR模型: 把人群分为S / I / R 三类, 适用于可治愈的传染性疾病
def SIR(y, t, args):
    S, I, R = y
    N = S + I + R
    beta, gamma = args
    return np.array([-(S / N) * (beta * I), (S / N) * (beta * I) - gamma * I, gamma * I])


# 3. SEIR模型: 在SIR的基础上考虑了 潜伏者E 这一中间角色, 认为 E 可由 S 转化过来, 同时又可转为 I
def SEIR(y, t, args):
    S, E, I, R = y
    N = S + E + I + R
    beta, alpha, gamma = args
    return np.array([-(S / N) * (beta * I), (S / N) * (beta * I) - alpha * E, alpha * E - gamma * I, gamma * I])


# 4. m-SEIR模型: 在SEIR的基础上考虑 E 也会 感染 S
def mSEIR(y, t, args):
    S, E, I, R = y
    N = S + E + I + R
    beta1, beta2, alpha, gama = args
    return np.array(
        [-(S / N) * (beta1 * E + beta2 * I), (S / N) * (beta1 * E + beta2 * I) - alpha * E, alpha * E - gama * I,
         gama * I])
