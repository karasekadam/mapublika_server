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
             value_occur, localization,
             localization_type):
    df: Optional[DataFrame] = pd.read_csv(file_storage, sep=',')
    to_stay: List[str] = [value_code, value_occur, localization,
                          localization_type]

    df.drop(df.columns.difference(to_stay), axis=1, inplace=True)
    df = get_areas_by_id(localization_type, localization, df)
    print(df)

    # per_thousand = []
    #
    # abs_values = df.where(df[value_code].isnull())
    # abs_values = dict(zip(abs_values[localization], abs_values[value_occur]))
    #
    # df = df.dropna()

    # for index, row in df.iterrows():
    #     if row[value_code] is not None:
    #         per_thousand.append(
    #             compute_per_thousand(abs_values.get(row[localization]),
    #                                  row[value_occur]))
    #
    # df["per_thousand"] = per_thousand

    return str(to_json(df, value_code,
                       value_occur, localization,
                       localization_type))


def get_areas_by_id(location_type: str, localization, data: DataFrame):
    data.rename(columns={localization: location_type}, inplace=True)
    ciselnik_df = pd.read_csv("uzemi_ciselniky.csv")
    ciselnik_df = ciselnik_df.dropna(how="all")
    ciselnik_df.drop(
        ciselnik_df.columns.difference(["Kod-obec", "kod-kraj",
                                        "kod-okres", "Nazev-obec",
                                        "Nazev-okres", "Nazev-kraj"]),
        axis=1, inplace=True)

    return pd.merge(data, ciselnik_df, on=location_type)


def compute_per_thousand(abs, val):
    return (1000 / abs) * val


def to_json(df: DataFrame, value_code,
            value_occur, localization,
            localization_type):
    grouped_by_kraj = df.groupby(["kod-kraj", value_code]).sum()
    grouped_by_kraj_celkem = df.groupby(["kod-kraj"]).sum()

    grouped_by_okres = df.groupby(["kod-okres", value_code]).sum()
    grouped_by_okres_celkem = df.groupby(["kod-okres"]).sum()

    json = {"kraje": {}, "okresy": {}, "obce": {}}

    kraje = grouped_by_kraj.index.values
    for kraj_hodnota in kraje:
        kraj = kraj_hodnota[0]
        kategorie = kraj_hodnota[1]
        celkovy_pocet = grouped_by_kraj_celkem.loc[kraj, value_occur] / 2
        koeficient = 1000 / celkovy_pocet
        pocet_v_kategorii = grouped_by_kraj.loc[kraj_hodnota, value_occur]
        if kraj in json["kraje"]:
            json["kraje"][kraj][kategorie] = str(
                int(pocet_v_kategorii * koeficient))
        else:
            json["kraje"][kraj] = {}
            json["kraje"][kraj][kategorie] = str(
                int(pocet_v_kategorii * koeficient))

    okresy = grouped_by_okres.index.values
    for okres_hodnota in okresy:
        okres = okres_hodnota[0]
        kategorie = okres_hodnota[1]
        celkovy_pocet = grouped_by_okres_celkem.loc[okres, value_occur] / 2
        koeficient = 1000 / celkovy_pocet
        pocet_v_kategorii = grouped_by_okres.loc[okres_hodnota, value_occur]
        if okres in json["okresy"]:
            json["okresy"][okres][kategorie] = str(
                int(pocet_v_kategorii * koeficient))
        else:
            json["okresy"][okres] = {}
            json["okresy"][okres][kategorie] = str(
                int(pocet_v_kategorii * koeficient))

    return json


json = read_csv("sldb2021_pocetdeti.csv", "pocetdeti_txt", "hodnota", "uzemi_kod", "Kod-obec")
with open("public_pocetDeti.json", "w") as outfile:
    outfile.write(json)

json = read_csv("sldb2021_vek5_pohlavi.csv", "pohlavi_txt", "hodnota", "uzemi_kod", "Kod-obec")
with open("public_pohlavi.json", "w") as outfile:
    outfile.write(json)

json = read_csv("sldb2021_stav.csv", "stav_txt", "hodnota", "uzemi_kod", "Kod-obec")
with open("sample_rodinnyStav.json", "w") as outfile:
    outfile.write(json)
