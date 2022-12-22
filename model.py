import torch
import torch.nn as nn


class NeuralNet(nn.Module):
    def __init__(self,input_size,hidden_size,num_classes):
        super(NeuralNet,self).__init__()
        self.f1 = nn.Linear(input_size,hidden_size)
        self.f2 = nn.Linear(hidden_size,hidden_size),
        self.f3 = nn.Linear(hidden_size,num_classes),
        self.relu = nn.ReLU()
    
    def forward(self,x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(x)
        out = self.relu(out)
        out = self.l3(out)
        # no activation and no softmax at the end bcs that's for 
        return out