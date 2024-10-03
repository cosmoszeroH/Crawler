import os
import pandas as pd


# Create directory to store data
def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# Create csv file to store data from pandas's dataframe
def create_csv_file(df, name, dir=r'./'):
    df.to_csv(dir + "/" + name + ".csv", index_label="No.")