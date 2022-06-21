import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint, solve_ivp
from datetime import datetime, timedelta
from scipy.optimize import minimize
from SEIR.param_fit.modelclass import loss, mSEIR


class SeirSelfFit(object):
    def __init__(self, Y0, args, path, N0, model=mSEIR):
        self.df = pd.read_csv(path)
        self.Y0 = Y0
        self.N0 = N0
        self.model = model
        self.args = args
        self.actual_data = []
        self.t = [datetime.strptime(value, '%Y-%m-%d').date() for value in self.df["date"]]

    def load_actual_data(self):
        # 得到S, E, I, R的数据
        # R, recovered, 康复者的总数, 直接就可以获取
        Re = self.df["totalHealed"].T
        # I, infected, 感染者总数, 注意是现存感染者总数, 可以用 累计确诊-累计治愈-累计死亡 得到
        In = (self.df["totalConfirmed"] - self.df["totalHealed"] - self.df["totalDeath"])
        # E, 潜伏者, 也就是感染了, 但是症状轻微不表现, 具有一定感染性, 这里实际上未知
        # 由于E, I相似, 设 E = k(t)*I(t), k(t)与I, 当I更多时, k(t)也更大(共鸣), 可以大于1
        # S, 易感者, 也就是健康的易受感染的人群. 从感染的过程来讲, 终态累计确诊包含始态易感者
        Inm = np.max(In)
        Ex = []
        Su = []
        for i in range(len(Re)):
            k = In[i]/Inm
            k += np.random.rand()/16-1/8
            k = k if k > 0 else In[i]/Inm
            Exi = k*In[i]
            Sui = self.N0 - Exi - In[i] - Re[i]
            if Sui < 0:
                Sui = 0
            Ex.append(Exi)
            Su.append(Sui)
        self.actual_data = [Su, Ex, In, Re]
        return self.actual_data

    def plot(self, y, t, path, title, choice=None, styles=None, labels=None):
        if choice is not None:
            # choice非None, 表示此时选择self.actual_data的某一个(几个)进行展示
            if t is None:
                t = self.t
            for c in choice:
                plt.plot(t, y[c], styles[c], label=labels[c])
        else:
            # 指定的其它图像
            plt.plot(t, y, styles, label=labels)
        plt.legend(loc='best')
        plt.title(title)
        plt.gcf().autofmt_xdate()  # 自动旋转日期标记
        plt.savefig(path)

    def train(self, weights, log):
        # 通过最小化loss调试到参数最佳值
        # print(f"data.shape = ({len(self.actual_data)}, {len(self.actual_data[0])})")
        optimal = minimize(
            loss,       # 需要进行最小化的loss func, 函数参数第一个必须是待优化的参数beta1, beta2
            self.args,
            args=(
                self.actual_data,
                self.Y0,
                weights,
                self.model
            ),
        )
        # beta1, beta2是拟合得到的值
        print(optimal, file=log)
        return list(optimal.x)

    def predict(self, args, predict_range):
        _te = self.t[-1]
        prd_tr = self.t + [(_te+timedelta(i+1)) for i in range(predict_range)]
        y = odeint(self.model, self.Y0, np.arange(0, len(self.t)+predict_range), args=(args, ), tfirst=True)
        # y = solve_ivp(self.model, t_span=(0, len(prd_tr)), y0=self.Y0, t_eval=range(0, len(prd_tr), 1), args=args)
        return prd_tr, y[:, 0], y[:, 1], y[:, 2], y[:, 3]
