"""
对于SEIR模型中的 I_actual 进行 LSTM 训练
"""
import time
import numpy as np
import pandas as pd
import torch
from torch import nn
import matplotlib.pyplot as plt

from SEIR.lstm.model import CovLSTM

# 参数设置
MAX_EPOCH = 200
MX_INCR = 100.
seq = 5
ratio = 0.6
nw = time.strftime('%m%d_%H%M%S', time.localtime(time.time()))

def get_data(path):
    df = pd.read_csv(path)
    t = pd.to_datetime(df["date"])
    return t, df["I_actual"], df["R_actual"]

def create_sequence(data, seq_len):
    xs = []
    ys = []
    for i in range(len(data)-seq_len-1):
        x = data[i:i+seq_len]
        y = data[i+seq_len]
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)


def train(data, train_len):
    x, y = create_sequence(data, seq)
    _x = (torch.tensor(x).float() / MX_INCR).reshape(-1, seq, 1)
    train_x = (torch.tensor(x[:train_len]).float() / MX_INCR).reshape(-1, seq, 1)
    train_y = (torch.tensor(y[:train_len]).float() / MX_INCR).reshape(-1, 1)
    model = CovLSTM(seq)
    opt = torch.optim.Adam(model.parameters(), lr=0.005)
    loss_func = nn.MSELoss()
    model.train()
    loss_record = []
    for epoch in range(MAX_EPOCH):
        output = model(train_x)
        loss = loss_func(output, train_y)
        loss_record.append(loss.item())
        opt.zero_grad()
        loss.backward()
        opt.step()
        if epoch % 10 == 0:
            print("epoch:{}, train_loss:{}".format(epoch, loss))
    return model, _x, loss_record


def model_fit(data, model):
    model.eval()
    torch.save(model.state_dict(), 'CoronaVirusPredictor.pkl')  # 保存参数
    prediction = list((model(data).data.reshape(-1)) * MX_INCR)
    return prediction


def plotIR(sec, dataI, dataR, y_I, y_R, t, train_len):
    tr_vI = dataI[seq + 1:]
    tr_vR = dataR[seq + 1:]
    tr_t = t[seq + 1:]
    plt.plot(tr_t[sec:], tr_vI[sec:], '-^', color="blue", label="True Value of I")
    plt.plot(tr_t[sec:], tr_vR[sec:], '-.', color="orange", label="True Value of R")
    plt.plot(tr_t[sec:train_len], y_I[sec:train_len], label='LSTM-fit(I)')
    plt.plot(tr_t[sec:train_len], y_R[sec:train_len], label='LSTM-fit(R)')
    plt.plot(tr_t[train_len:], y_I[train_len:], label='LSTM-pred(I)')
    plt.plot(tr_t[train_len:], y_R[train_len:], label='LSTM-pred(R)')
    plt.legend(loc='best')
    plt.title('Infected-Recovered prediction by LSTM (CN-SZ)')
    plt.xlabel('Date')
    plt.ylabel('Daily infected cases')
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.savefig("img/" + nw + "_IR.png")
    plt.show()

def plotLoss(loss, spec):
    plt.plot(range(MAX_EPOCH), loss, label="Train loss")
    plt.legend(loc='best')
    plt.title('Training loss of LSTM on COVID-19(CN-SZ) dataset')
    plt.savefig("img/" + nw + spec + "_loss.png")
    plt.show()

def main():
    # 读取数据
    t, y_I, y_R = get_data("../../data/lstm_0415.csv")
    # 划分数据集
    train_len = int(len(t) * ratio)
    # 对y_I进行训练
    yIModel, Ia, yILoss = train(y_I, train_len)
    yRModel, Ra, yRLoss = train(y_R, train_len)
    # 对y_I进行预测(拟合)
    yIp = model_fit(Ia, yIModel)
    yRp = model_fit(Ra, yRModel)
    # 进行作图可视化
    # sec = int((1 - ratio / 2) * len(t))
    sec = 0
    plotIR(sec, y_I, y_R, yIp, yRp, t, train_len)
    # plotLoss(yILoss, "_I_")
    # plotLoss(yRLoss, "_R_")
    # 计算Loss
    weight = [0.49, 0.51]
    yILoss = np.array(yILoss)
    yRLoss = np.array(yRLoss)
    # plotLoss(weight[0]*yILoss+weight[1]*yRLoss, "_IR_")
    I_MAE = np.mean(np.abs(y_I[seq+1:] - yIp))
    R_MAE = np.mean(np.abs(y_R[seq+1:] - yRp))
    I_MSE = np.sqrt(np.mean(np.square(y_I[seq+1:] - yIp)))
    R_MSE = np.sqrt(np.mean(np.square(y_R[seq+1:] - yRp)))
    # print(I_MAE, ", ", R_MAE, ", ", I_MSE, ", ", R_MSE)
    # print(I_MAE, ", ", R_MAE, ", ", I_MSE, ", ", R_MSE)
    print("MAE loss: ", weight[0]*I_MAE+weight[1]*R_MAE)
    print("RMSE loss: ", weight[0]*I_MSE+weight[1]*R_MSE)


if __name__ == '__main__':
    main()


