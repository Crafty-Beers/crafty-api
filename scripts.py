import pandas as pd
import numpy as np

# MULTIPLIERS
EXPERIENCE_MULT = .15
FLAVOR_MULT = .15
TYPES_MULT = .25
BITTERNESS_MULT = .25
ALCOHOL_CONTENT_MULT = .20

def get_best_beer(beer_df, json_answers):
    '''
    Finds the single best beer from the database based on the user's given json_answers
    :param beer_df: pd.Dataframe of the Beer Database.csv
    :param json_answers: A JSON
    :return: a Dictionary containing information of the top beer
    '''

    beer_df['Score'] = 0

    # 1) Evaluate Experience
    # Possible Answers: Beginner, Intermediate, Advanced
    # If the person is not experienced, add points to beer with lower IBUs and vice

    # Rank beers on bitterness
    beer_df['Bitter Pct'] = beer_df['Bitterness (IBU)'].rank(method='min', pct=True)

    if json_answers['experience'] == 'Beginner':
        beer_df['Score'] = (1 - beer_df['Bitter Pct']) * 100 * EXPERIENCE_MULT
    elif json_answers['experience'] == 'Advanced':
        beer_df['Score'] = beer_df['Bitter Pct'] * 100 * EXPERIENCE_MULT
    elif json_answers['experience'] == 'Intermediate':
        median = beer_df['Bitter Pct'].median(axis=0)
        beer_df['Score'] = (1 - (abs(beer_df['Bitter Pct'] - median) * 2)) * 100 * EXPERIENCE_MULT

    # 2) Flavors
    # No solution yet
    # Temporary: Give every beer a .15
    beer_df['Score'] += 100 * FLAVOR_MULT

    # 3) Types of Beers
    # Possible Answers: A list of all the unique values in beer_df
    user_types = json_answers['types']
    beer_df['Score'] += beer_df['Beer Type'].isin(user_types) * 100 * TYPES_MULT

    # 4) Bittereness
    # Possible Answers: Low, Moderate, High

    if json_answers['bitterness'] == 'Low':
        beer_df['Score'] += (1 - beer_df['Bitter Pct']) * 100 * BITTERNESS_MULT
    elif json_answers['bitterness'] == 'High':
        beer_df['Score'] += beer_df['Bitter Pct'] * 100 * BITTERNESS_MULT
    elif json_answers['bitterness'] == 'Moderate':
        median = beer_df['Bitter Pct'].median(axis=0)
        beer_df['Score'] += (1 - (abs(beer_df['Bitter Pct'] - median) * 2)) * 100 * BITTERNESS_MULT

    # 5) Alcohol level
    # Possible Answers: Low, Moderate, High

    # Rank beers with most ABV
    beer_df['ABV Pct'] = beer_df['ABV'].rank(method='min', pct=True)

    if json_answers['alcohol_content'] == 'Low':
        beer_df['Score'] += (1 - beer_df['ABV Pct']) * 100 * ALCOHOL_CONTENT_MULT
    elif json_answers['alcohol_content'] == 'High':
        beer_df['Score'] += beer_df['ABV Pct'] * 100 * ALCOHOL_CONTENT_MULT
    elif json_answers['alcohol_content'] == 'Moderate':
        median = beer_df['ABV Pct'].median(axis=0)
        beer_df['Score'] += (1 - (abs(beer_df['ABV Pct'] - median) * 2)) * 100 * ALCOHOL_CONTENT_MULT

    #print(beer_df)

    # get the the top-scoring beer and package the output
    top_beer = beer_df.sort_values(by=['Score'], ascending=False).head(1)
    top_beer = top_beer.fillna("")
    top_beer_dict = top_beer.to_dict(orient='records')

    return top_beer_dict


def get_available_beer_types(beer_df):
    '''
    Gets all the available beer types in the dataset
    :param beer_df: a pd.Dataframe of all the beers
    :return: a list of beer types
    '''

    return beer_df['Beer Type'].unique().tolist()
