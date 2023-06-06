# Import packages
import re
import pandas as pd
import Levenshtein as lev
from numpy import nan
from jellyfish import metaphone

def load_watchlist():
    # Read data
    df = pd.read_excel("ConList.xlsx", skiprows=1)

    # Insert concatenated names
    df.insert(
        0, "FULL_NAME",
        df[["Name 1", "Name 2", "Name 3", "Name 4", "Name 5", "Name 6"]].fillna("").agg(" ".join, axis=1)
    )
        
    return df

def transform_name(name):
    if type(name)==str:
        std_name = re.sub(r"[^a-zA-Z]+", " ", name).upper().strip()
        return std_name if len(std_name)>0 else None
    
def transform_name_metaphone(std_name):
    try:
        return metaphone(std_name)
    
    except:
        return None
    
def calc_ratio(s1, s2):
    try:
        return lev.ratio(s1, s2)

    except:
        return nan