from torch import nn
import torch

class CovLSTM(nn.Module):
    def __init__(self, seq, input_size=1, hidden_size=16, num_layers=1, output_size=1):
        super(CovLSTM, self).__init__()
        self.seq = seq
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size * seq, output_size)

    def forward(self, x):
        x, (h, c) = self.lstm(x)
        x = x.reshape(-1, self.hidden_size * self.seq)
        x = self.linear(x)
        return x
