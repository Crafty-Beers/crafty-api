import os
import json
import gspread
from scripts import *
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

load_dotenv()

# use creds to create a client to interact with the Google Drive API
scopes = ['https://spreadsheets.google.com/feeds']
json_creds = os.getenv("GS_CREDS")
creds_dict = json.loads(json_creds)
creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)

gc = gspread.authorize(creds)

sh = gc.open_by_key(os.getenv("GS_KEY"))
ws = sh.worksheet('Beer Database')
ws_vals = ws.get_all_values()
beer = pd.DataFrame(data=ws_vals[1:], columns=ws_vals[0])

example_request_body = {
    'experience': 'Beginner',
    'flavors': ['Hoppy', 'Roasty/Coffee'],
    'types': ['IPA', 'Wheat', 'Pale Ale', 'Porter'],
    'bitterness': 'Low',
    'alcohol_content': 'Low'
}

#print(get_best_beer(beer, example_request_body))

#print(get_available_beer_types(beer))
