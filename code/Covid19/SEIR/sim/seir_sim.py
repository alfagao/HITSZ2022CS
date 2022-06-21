import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
class SeirSim(object):
    def __init__(self, model, days, Y0, args):
        """
        :param model: SI, SIR, SEIR, mSEIR
        :param days: 持续时间
        :param Y0: 初始时各类人群数量
        :param args: beta(1, 2), alpha, gamma 取决于模型
        """
        self.t = np.arange(0, days, 1)
        self.Y = odeint(model, Y0, self.t, args=args)
        self.yDim = len(Y0)

    def plot(self, styles, title, savePath):
        """
        :param savePath: after plot, where to save
        :param styles: a list of dict   [{"line", "label" }, ... ] and
                        len(styles) equal to len(Y0)
        :param title: the title of the picture
        """
        plt.figure()
        for i in range(self.yDim):
            plt.plot(self.t, self.Y[:, i], styles[i]["line"], label=styles[i]["label"])
        plt.title(title)
        plt.xlabel('days')
        plt.legend(loc='best')
        plt.savefig(savePath)
