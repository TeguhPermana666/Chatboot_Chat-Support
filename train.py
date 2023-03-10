import json
import random

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

from model import NeuralNet
from nltk_utils import bag_of_words, stem, tokenize

with open("intents.json","r") as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

# loop through each sentence in out intents patterns
for intent in intents["intents"]:
    tag = intent['tag']
    # add to tag list
    tags.append(tag)
    
    for pattern in intent["patterns"]:
        # tokenize each word in the sentence
        w = tokenize(pattern)
        # add to out word lists
        all_words.extend(w)
        # add to xy pair
        xy.append([w,tag])

# stem and lower each word
ignore_word = ["?",".","!"]
all_words = [stem(w) for w in all_words if w not in ignore_word]
# remove duplicate and sort
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# print(len(xy), "patterns :", xy)
# print(len(tags), "tags:",tags)
# print(len(all_words), "unique stemmed words:", all_words)

# Create training data
X_train = []
y_train = []

for(pattern_sentence, tag) in xy:
    # X : bag of words for each pattern_sentence
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    
    # y : Pytorch CrossEntropyLoss needs only class labels
    label = tags.index(tag)
    y_train.append(label)

# Convert to numpy array
X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters
num_epochs = 1000
batch_size = 8
learning_rate = 1e-3
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)
# print(input_size,output_size)

class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train
    
    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
    
    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size,hidden_size,output_size).to(device)

# loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)

# train the model
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        # forward pass
        outputs = model(words)
        # uf y would be one hot, we must apply
        # labels = torch.max(labels,1)[1]
        loss = criterion(outputs,labels)
        
        # backward pass and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    if (epoch+1) % 100 == 0:
        print(f'Epoch [ {epoch + 1} / {num_epochs} ], Loss : {loss.item():.4f}')

print(f"final loss : {loss.item():.4f}")

data = {
    "model_state" : model.state_dict(),
    "input_size" : input_size,
    "hidden_size" : hidden_size,
    "output_size" : output_size,
    "all_words" : all_words,
    "tags" : tags
}

FILE = "data.pth"
torch.save(data,FILE)

print(f"training complete, file save to {FILE}")