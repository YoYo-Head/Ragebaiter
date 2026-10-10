## Ragebaiter

# What it is and how it works
Ragebaiter is a chatterbox that combines the use of classification and a neural network to try annoy the user. 
It's for people who are either egoistic, or just want to waste some time :). Currently, the frontend and backend 
are working, with the backend being able to train the bot, save it's data and load data. It is also able to 
tokenize and lemmatize the intents (which has my different classifications) and process messages, giving a 
response back. FastAPI for my backend also works fine, allowing for the frontend to pass user messages and fetch 
bot responses. I've also tried my best to design the frontend.

# How to run
There are two ways where you can run this project:

**1. Directly on API**
To run on the API, you can simply go to the directory `/backend` via the terminal and run the command `python main.py`. 
After the the terminal prints out: 
> INFO:     Application startup complete.
you can then open up your preferred browser and type in `localhost:8000/docs`. After that, press the drop down
for messages, and write your message in the json area provided. Once done, press `execute`. Beneath that button,
if it shows *status code 200*, you can read the json data below it to see the response!

**2. Through the Frontend**
To use the frontend interface, follow option 1. After that, make sure you have the `Live Server` VS Code extension.
Once ready, right click `index.html` from the `/frontend` directory. Once it loads, it should automatically open up
a browser that loads the html code. After that, you can use the webpage to interact with the bot!

# Where my training data is
My trainig data can be located in the file `intents.json` in the `/backend` directory. While alot of it I made myself,
I did use AI to generate some data for me to use.