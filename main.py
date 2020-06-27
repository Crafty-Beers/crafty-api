import os
import json
from fastapi import FastAPI
from scripts import get_available_beer_types, get_best_beer
import pandas as pd
from pydantic import BaseModel
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# use creds to create a client to interact with the Google Drive API
scopes = ['https://spreadsheets.google.com/feeds']
json_creds = os.getenv("GS_CREDS")
creds_dict = json.loads(json_creds)
creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)

load_dotenv()
app = FastAPI()


def get_beer_df(credentials):
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(os.getenv("GS_KEY"))
    ws = sh.worksheet('Beer Database')
    ws_vals = ws.get_all_values()
    beer_df = pd.DataFrame(data=ws_vals[1:], columns=ws_vals[0])

    return beer_df


class Answers(BaseModel):
    experience: str
    flavors: list
    types: list
    bitterness: str
    alcohol_content: str


@app.get("/beer-rec/")
def get_beer_recommendation(answers: Answers):
    try:
        beer_df = get_beer_df(creds)
        return get_best_beer(beer_df, answers.__dict__)
    except Exception as e:
        print(e)


@app.get("/available-types/")
def get_available_types():
    try:
        beer_df = get_beer_df(creds)
        return get_available_beer_types(beer_df)
    except Exception as e:
        print(e)
