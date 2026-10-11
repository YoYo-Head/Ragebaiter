from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import bot
import response_models
import security
from os.path import exists

dimensionsPath = "dimensions.json"
modelPath = "ragebaiter-v1.pth"

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

if exists(modelPath) and exists(dimensionsPath):
    ragebaiter.load_model(modelPath, dimensionsPath)
    print("Model has loaded!")

else:
    print("Training ragebaiter...")
    ragebaiter.parse_intents()
    ragebaiter.prepare_data()
    ragebaiter.train_model(8, 0.001, 300)
    print("Trained the model!")
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

@app.get("/api")
@security.limiter.limit("65/minute")
def root(request: security.Request):
    return {"message": "API running"}

@app.post("/api/message", response_model=response_models.messageResponse)
@security.limiter.limit("65/minute")
def request_message(data: response_models.messageCreate, request: security.Request):
    return response_models.messageResponse(id=nextNumberM(), message=ragebaiter.proccess_message(data.message))

@app.post("/api/train/{epochs}", response_model=response_models.trainingResponse)
@security.limiter.limit("1/minute")
def request_training(data: response_models.trainingCreate,  request: security.Request, _: str = Depends(security.verify_api_key)):
    ragebaiter.parse_intents()
    ragebaiter.prepare_data()
    ragebaiter.train_model(8, 0.001, data.epochs)
    ragebaiter.save_model("ragebaiter-v1.pth", "dimensions.json")

    return response_models.trainingResponse(id=nextNumberT(), epochs=data.epochs)
