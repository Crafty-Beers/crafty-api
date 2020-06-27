from fastapi import FastAPI
from scripts import get_available_beer_types, get_best_beer
import pandas as pd
from pydantic import BaseModel

app = FastAPI()
beer_df = pd.read_csv('Beer Database.csv')


class Answers(BaseModel):
    experience: str
    flavors: list
    types: list
    bitterness: str
    alcohol_content: str


@app.get("/beer-rec/")
def get_beer_recommendation(answers: Answers):
    try:
        return get_best_beer(beer_df, answers.__dict__)
    except Exception as e:
        print(e)


@app.get("/available-types/")
def get_available_types():
    try:
        return get_available_beer_types(beer_df)
    except Exception as e:
        print(e)
