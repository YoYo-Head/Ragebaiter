from pydantic import BaseModel

class messageCreate(BaseModel):
    message: str

class messageResponse(messageCreate):
    id: int

    class Config:
        from_attributes = True

class trainingCreate(BaseModel):
    epochs: int

class trainingResponse(trainingCreate):
    id: int

    class Config:
        from_attributes = True
     