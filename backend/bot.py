import torch
import torch.nn as nn
import torch.nn.functional as f
import pandas as pd
import matplotlib.pyplot as plt
import nltk

nltk.download("wordnet")

class Model(nn.Module):

    
    def __init__(self, input_size, output_size, h1=300, h2=150, h3=75):
        super(Model, self).__init__()

        self.fc1 = nn.Linear(input_size, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.fc3 = nn.Linear(h2, h3)
        self.out = nn.Linear(h3, output_size)
        self.relu = nn.ReLU
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)

        x = self.relu(self.fc2(x))
        x = self.dropout(x)

        x = self.relu(self.fc3(x))
        x = self.dropout(x)

        x = self.out(x)

        return x

class ModelAssistant:
    def __init__(self, intents_path, function_mappings = None):
        self.model = None
        self.intents_path = intents_path

        self.documents = []
        self.vocabulary = []
        self.intents = []
        self.intents_responses = []

        self.function_mappings = function_mappings

        self.X = None
        self.y = None

    @staticmethod
    def tokenize_and_lemmatize(text):
        lemmatizer = nltk.WordNetLemmatizer()

        words = nltk.word_tokenize(text)
        words = [lemmatizer.lemmatize(word.lower()) for word in words]

        return words



ragebaiter = ModelAssistant("intents.json")
print(ragebaiter.tokenize_and_lemmatize("I am a wizard!"))












