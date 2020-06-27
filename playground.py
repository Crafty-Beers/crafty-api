from scripts import *

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

beer = pd.read_csv('Beer Database.csv')

example_request_body = {
    'experience': 'Beginner',
    'flavors': ['Hoppy', 'Roasty/Coffee'],
    'types': ['IPA', 'Wheat', 'Pale Ale', 'Porter'],
    'bitterness': 'Low',
    'alcohol_content': 'Low'
}

print(get_best_beer(beer, example_request_body))

print(get_available_beer_types(beer))
