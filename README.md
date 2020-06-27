# Crafty API
### _The official, haphazardly-created API for Crafty_

## [Documentation](https://crafty-api.herokuapp.com/docs)

## /beer-rec/
Request: `https://crafty-api.herokuapp.com/beer-rec/`
Example Request Body (required):
```json
{
    "experience": "Intermediate",
    "flavors": ["Hoppy", "Roasty/Coffee"],
    "types": ["IPA", "Wheat", "Pale Ale", "Porter"],
    "bitterness": "Low",
    "alcohol_content": "Low"
}
```
Example Response Body:
```json
[
    {
        "Beer": "Bad Elmer's Porter",
        "Brewery": "Upland Brewing Co",
        "City": "Bloomington",
        "State": "IN",
        "Beer Type": "Porter",
        "ABV": 6.0,
        "Bitterness (IBU)": 20,
        "Malt": "Carafa special III, Chocolate malt, Crisp brown, Crisp dark crystal, Munich 20L, Pale wheat",
        "Served in": "Bottle, Drought",
        "Score": 71.36363636363636,
        "Bitter Pct": 0.45454545454545453,
        "ABV Pct": 0.7272727272727273
    }
]
```

## /available-types/
Request: `https://crafty-api.herokuapp.com/available-types/`
Example Response Body:
```json
[
  "Witbier",
  "IPA",
  "Pilsner",
  "Porter",
  "Pale Ale",
  "Blonde Ale",
  "Wheat Ale",
  "Red Ale"
]
```