import torch
import torch.nn as nn
import torch.nn.functional as f
from torch.utils.data import DataLoader, TensorDataset
from torch import optim

import nltk
import numpy as np

import os
import json
import random

nltk.download("punkt_tab")


class Model(nn.Module):

    
    def __init__(self, input_size, output_size, h1=300, h2=150, h3=75):
        super(Model, self).__init__()

        self.fc1 = nn.Linear(input_size, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.fc3 = nn.Linear(h2, h3)
        self.out = nn.Linear(h3, output_size)
        self.relu = nn.ReLU()
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
        self.intents_responses = {}

        self.function_mappings = function_mappings

        self.X = None
        self.y = None

    @staticmethod
    def tokenize_and_lemmatize(text):
        lemmatizer = nltk.WordNetLemmatizer()

        # breaks down the text into basic words in a list (also makes sure base words (excl words in different times) are only in the list once)
        words = nltk.word_tokenize(text)
        words = [lemmatizer.lemmatize(word.lower()) for word in words] 

        return words

    def bag_of_words(self, words):
        return [1 if word in words else 0 for word in self.vocabulary] # turns into 1s and 0s for word positioning

    def parse_intents(self):

        if os.path.exists(self.intents_path):

            with open(self.intents_path, "r") as f:
                intentsData = json.load(f)

            # sees if our intents data is up to date /w json data. if not, it appends their data to python
            for intent in intentsData["intents"]:
                if intent["tag"] not in self.intents:
                    self.intents.append(intent["tag"])
                    self.intents_responses[intent["tag"]] = intent["responses"]

                for pattern in intent["patterns"]:
                    pattern_words = self.tokenize_and_lemmatize(pattern)
                    self.vocabulary.extend(pattern_words)
                    self.documents.append((pattern_words, intent["tag"]))

                self.vocabulary = sorted(set(self.vocabulary))

    def prepare_data(self):
        bags = []
        indices = []

        for document in self.documents:
            words = document[0]
            bag = self.bag_of_words(words)

            intents_index = self.intents.index(document[1])

            bags.append(bag)
            indices.append(intents_index)

        self.X = np.array(bags)
        self.y = np.array(indices)

    # trains model, also capturing losses
    def train_model(self, batch_size, lr, epochs):
        X_tensor = torch.tensor(self.X, dtype=torch.float32)
        y_tensor = torch.tensor(self.y, dtype=torch.long)

        dataset = TensorDataset(X_tensor, y_tensor)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        self.model = Model(self.X.shape[1], len(self.intents))

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr)

        for epoch in range(epochs):
            running_loss = 0

            for batch_X, batch_y in loader:
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                running_loss += loss

            print(f"Epoch {epoch + 1} - Loss: {running_loss / len(loader):.4f}")

    # Dumps model data (e.g.: weights) into json file
    def save_model(self, model_path, dimensions_path):
        torch.save({"model_state_dict": self.model.state_dict(),
                    "vocabulary": self.vocabulary,
                    "intents": self.intents,
                    "intents_responses": self.intents_responses
                    }, model_path)

        with open(dimensions_path, "w") as f:
            json.dump({ "input size": self.X.shape[1], "output_size": len(self.intents) }, f)

    # Loads model data to model
    def load_model(self, model_path, dimensions_path):
        checkpoint = torch.load(model_path, map_location="cpu", weights_only=True)

        self.vocabulary = checkpoint["vocabulary"]
        self.intents = checkpoint["intents"]
        self.intents_responses  = checkpoint["intents_responses"]

        with open(dimensions_path, "r") as f:
            dimensions = json.load(f)

        self.model = Model(dimensions["input_size"], dimensions["output_size"])

        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.eval()

    # Gets message and tokenises, and then goes thru model, then returns response
    def proccess_message(self, input_message):
        words = self.tokenize_and_lemmatize(input_message)
        bag = self.bag_of_words(words)

        bag_tensor = torch.tensor([bag], dtype=torch.float32)

        self.model.eval()

        with torch.no_grad():
            predictions = self.model(bag_tensor)

        predicted_class_index = torch.argmax(predictions, dim=1).item()
        predicted_intent = self.intents[predicted_class_index]

        if self.function_mappings:
            if predicted_intent in self.function_mappings:
                self.function_mappings[predicted_intent]()

        if self.intents_responses[predicted_intent]:
            return random.choice(self.intents_responses[predicted_intent])
        else:
            return None

if __name__ == "__main__":

    ragebaiter = ModelAssistant("intents.json")
    ragebaiter.parse_intents()
    ragebaiter.prepare_data()
    ragebaiter.train_model(8, 0.001, 300)

    ragebaiter.save_model("ragebaiter-v1.pth", "dimensions.json")

    while True:
        message = input("Message here: ")

        if message == "/quit":
            break

        print(ragebaiter.proccess_message(message))