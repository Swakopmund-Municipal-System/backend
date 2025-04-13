# from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def foo():
    return {"Hello": "Nigga"}

@app.get("/weather/{location}")
def GetWeatherForLocation(location):
    return {"Location": location}

@app.get("/tide/{location}")
def GetTideForecast(location):
    return {"Location": location}


