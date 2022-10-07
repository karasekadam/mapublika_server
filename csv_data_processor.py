import pandas as pd
import numpy as np

df = pd.read_csv("uzemi_ciselniky.csv")
#print(df.to_string())

#def parse_file(path_to_file, value="hodnota", value_name="pocetdeti_txt", localization="", localization_code="0"):


def gib_header_print(path_to_file):
    #pd.DataFrame(np.random.randn(10, 4), columns=list('abcd')).to_csv(path_to_file, mode='w')
    #pd.read_csv(path_to_file, index_col=0, nrows=0).columns.tolist()
    print(df.columns)

if __name__ == '__main__':
    gib_header_print("uzemi_ciselniky.csv")