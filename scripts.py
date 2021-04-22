import pandas as pd
import numpy as np

# MULTIPLIERS
EXPERIENCE_MULT = 0
FLAVOR_MULT = 0
TYPES_MULT = .50
BITTERNESS_MULT = .30
ALCOHOL_CONTENT_MULT = .20


def get_best_beer(beer_df, json_answers):
    '''
    Finds the single best beer from the database based on the user's given json_answers
    :param beer_df: pd.Dataframe of the Beer Database.csv
    :param json_answers: A JSON
    :return: a Dictionary containing information of the top beer
    '''

    beer_df['Score'] = 0


    #   1) Evaluate Experience
    #
    #   2) Flavors
    #      No solution yet, giving every beer .15
    #
    #   3) Types of Beers
    #      Possible Answers: A list of all the unique values in beer_df
    #
    #   4) Bittereness
    #      Possible Answers: Low, Moderate, High
    #
    #   5) Alcohol level
    #      Possible Answers: Low, Moderate, High

    type_split = json_answers['types'].split(",")

    evaluate_experience(beer_df, json_answers['experience'])
    evaluate_flavors(beer_df)
    evaluate_type(beer_df, type_split)
    evaluate_bitterness(beer_df, json_answers['bitterness'])
    evaluate_alcohol_level(beer_df, json_answers['alcohol_content'])

    print(beer_df.sort_values(by='Score', ascending=False))

    # Get the the top-scoring beer and package the output
    top_beer = beer_df.sort_values(by=['Score'], ascending=False).head(3)
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


def evaluate_experience(df, experience):
    # Rank beers on bitterness
    df["Bitterness (IBU)"] = df["Bitterness (IBU)"].astype(int)
    df['Bitter Pct'] = df['Bitterness (IBU)'].rank(method='min', pct=True)

    if experience == 'Beginner':
        df['Score'] += (1 - df['Bitter Pct']) * 100 * EXPERIENCE_MULT
    elif experience == 'Advanced':
        df['Score'] += df['Bitter Pct'] * 100 * EXPERIENCE_MULT
    elif experience == 'Intermediate':
        median = df['Bitter Pct'].median(axis=0)
        df['Score'] += (1 - (abs(df['Bitter Pct'] - median) * 2)) * 100 * EXPERIENCE_MULT


def evaluate_flavors(df):
    df['Score'] += 100 * FLAVOR_MULT


def evaluate_type(df, user_types):
    df['Score'] += df['Beer Type'].isin(user_types) * 100 * TYPES_MULT


def evaluate_bitterness(df, bitterness):
    if bitterness == 'Low':
        df['Score'] += (1 - df['Bitter Pct']) * 100 * BITTERNESS_MULT
    elif bitterness == 'High':
        df['Score'] += df['Bitter Pct'] * 100 * BITTERNESS_MULT
    elif bitterness == 'Moderate':
        median = df['Bitter Pct'].median(axis=0)
        df['Score'] += (1 - (abs(df['Bitter Pct'] - median) * 2)) * 100 * BITTERNESS_MULT


def evaluate_alcohol_level(df, alcLevel):
    # Rank beers with most ABV
    df["ABV"] = df["ABV"].astype(float)
    df['ABV Pct'] = df['ABV'].rank(method='min', pct=True)

    if alcLevel == 'Low':
        df['Score'] += (1 - df['ABV Pct']) * 100 * ALCOHOL_CONTENT_MULT
    elif alcLevel == 'High':
        df['Score'] += df['ABV Pct'] * 100 * ALCOHOL_CONTENT_MULT
    elif alcLevel == 'Moderate':
        median = df['ABV Pct'].median(axis=0)
        df['Score'] += (1 - (abs(df['ABV Pct'] - median) * 2)) * 100 * ALCOHOL_CONTENT_MULT
