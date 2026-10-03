import torch
import torch.nn as nn
import torch.nn.functional as f
import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize as wt


class Model(nn.Module):

    # in_features: punctuation, noun, verb (maybe)
    # Out features r the predicted words
    def __init__(self, in_features=3, h1=300, h2=300, h3=300, out_features=1000):
        super().__init__()
        self.fc1 = nn.Linear(in_features, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.fc3 = nn.Linear(h2, h3)
        self.out = nn.Linear(h3, out_features)

    def forward(self, x):
        x = f.relu(self.fc1(x))
        x = f.relu(self.fc2(x))
        x = f.relu(self.fc3(x))
        x = self.out(x)

        return x


torch.manual_seed(41)

model = Model

df = pd.read_csv("https://raw.githubusercontent.com/kaspercools/genz-dataset/refs/heads/main/genz_slang.csv")

tokenizedList = []

columns = ["keyword", "description"]

for column in columns:
    for word in column:
        token = wt(word)

        tokenizedList.append(token)



