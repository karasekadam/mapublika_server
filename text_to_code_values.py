import pandas as pd

"""
get_index po zadání chtěné obce/okresu/kraje vrátí jeho kód
"""

def get_text(index, row, df):
    print(df.ix[row, index+1])
    

def get_index(wanted, path_to_file):
    df = pd.read_csv(path_to_file)
    for i in range(len(df)):
        if df.iloc[i, 1] == wanted: #obce
            return int(df.iloc[i, 0])
        if df.iloc[i, 8] == wanted:  #okresy
            return int(df.iloc[i, 7])
        if df.iloc[i, 10] == wanted:  #kraje
            return int(df.iloc[i, 9])


if __name__ == '__main__':
    get_index("Aš", "uzemi_ciselniky.csv")
    #"554499"