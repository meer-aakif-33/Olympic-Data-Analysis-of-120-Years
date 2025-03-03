import pandas as pd


def preprocess(df, region_df):

    df = df[df['Season'] == 'Summer']   

# Merge on 'NOC' column while keeping only relevant columns
    df = df.merge(region_df[['NOC', 'region']], on='NOC', how='left')

    df.drop_duplicates(inplace=True)

    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df