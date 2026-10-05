from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import bot
import response_models
import security


app = FastAPI()
app.add_middleware(security.SlowAPIMiddleware)
app.add_exception_handler(security.RateLimitExceeded, security._rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]

)


ragebaiter = bot.ModelAssistant("intents.json")

ragebaiter.parse_intents()
ragebaiter.prepare_data()
ragebaiter.train_model(8, 0.001, 300)
ragebaiter.save_model("ragebaiter-v1.pth", "dimensions.json")


@app.get("/")
def root():
    return {"message": "API running"}

@app.post("/message")
def request_message(message: str):
    response = ragebaiter.proccess_message(message)

    return {"response": response}

@app.post("/train/{epochs}")
def request_training(epochs: int, _: str = Depends(security.verify_api_key)):
    ragebaiter.train_model(8, 0.001, epochs)
    ragebaiter.save_model("ragebaiter-v1.pth", "dimensions.json")

    return {"success": "True"}
