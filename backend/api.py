from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import bot
import response_models
import security


app = FastAPI()
app.state.limiter = security.limiter
app.add_middleware(security.SlowAPIMiddleware)
app.add_exception_handler(security.RateLimitExceeded, security._rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]

)


ragebaiter = bot.ModelAssistant("intents.json")

ragebaiter.parse_intents()
ragebaiter.prepare_data()
ragebaiter.train_model(8, 0.001, 300)
ragebaiter.save_model("ragebaiter-v1.pth", "dimensions.json")

idNumbM = 0
idNumbT = 0

def nextNumberM() -> int:
    global idNumbM
    idNumbM += 1
    return idNumbM

def nextNumberT() -> int:
    global idNumbT
    idNumbT += 1
    return idNumbT

@app.get("/")
def root():
    return {"message": "API running"}

@app.post("/message", response_model=response_models.messageResponse)
def request_message(data: response_models.messageCreate):
    return response_models.messageResponse(id=nextNumberM(), message=ragebaiter.proccess_message(data.message))

@app.post("/train/{epochs}", response_model=response_models.trainingResponse)
def request_training(data: response_models.trainingCreate, _: str = Depends(security.verify_api_key)):
    ragebaiter.parse_intents()
    ragebaiter.prepare_data()
    ragebaiter.train_model(8, 0.001, data.epochs)
    ragebaiter.save_model("ragebaiter-v1.pth", "dimensions.json")

    return response_models.trainingResponse(id=nextNumberT(), epochs=data.epochs)
