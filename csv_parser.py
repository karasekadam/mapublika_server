from typing import List, Set, Any, Optional

import pandas as pd
from flask import request, Blueprint, app

# from app import __name__
from pandas import DataFrame
from werkzeug.datastructures import FileStorage

file_saver = Blueprint('file_saver', __name__)


# value=string nazev sloupce,
# value_name=jmeno te veci(když prazdny soucet na uzemni jednotku),
# localization=nazev uzemni jednotky (kraj, obec atd),
# typ_uzemni jednotky ,
def read_csv(file_storage: FileStorage, value_code,
             value_name, localization,
             localization_type):
    df: Optional[DataFrame] = pd.read_csv(file_storage, sep=',')
    to_stay: List[str] = [value_code, value_name, localization, localization_type]
    df.drop(df.columns.difference(to_stay), axis=1, inplace=True)


    per_thousand = []

    abs_values = df.where(df[value_code].isnull())
    abs_values = dict(zip(abs_values[localization], abs_values[value_name]))

    df = df.dropna()

    for index, row in df.iterrows():
        if row[value_code] is not None:
            per_thousand.append(compute_per_thousand(abs_values.get(row[localization]), row[value_name]))

    df["per_thousand"] = per_thousand

    return


def compute_per_thousand(abs, val):
    return (1000 / abs) * val






def count_per_thousand(df: DataFrame, ):
    per_thousand: List[float] = []






