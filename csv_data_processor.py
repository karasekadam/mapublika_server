import pandas as pd
import numpy as np


def to_json():
    # load and preprocess data
    ciselnik_df = pd.read_csv("uzemi_ciselniky.csv")
    ciselnik_df = ciselnik_df.dropna(how="all")
    ciselnik_df.drop(
        ciselnik_df.columns.difference(["Kod-obec", "kod-kraj", "kod-okres"]),
        axis=1, inplace=True)
    data_df = pd.read_csv("sldb2021_pocetdeti.csv")
    data_df = data_df.dropna(how="all")
    data_df.drop(
        data_df.columns.difference(["hodnota", "pocetdeti_txt", "uzemi_kod"]),
        axis=1, inplace=True)
    data_df.rename(columns={"uzemi_kod": "Kod-obec"}, inplace=True)

    # process data
    merged_df = pd.merge(data_df, ciselnik_df, how="inner", on="Kod-obec")

    grouped_by_kraj = merged_df.groupby(["kod-kraj", "pocetdeti_txt"]).sum()
    grouped_by_kraj_celkem = merged_df.groupby(["kod-kraj"]).sum()

    grouped_by_okres = merged_df.groupby(["kod-okres", "pocetdeti_txt"]).sum()
    grouped_by_okres_celkem = merged_df.groupby(["kod-okres"]).sum()

    json = {"kraje": {}, "okresy": {}, "obce": {}}

    kraje = grouped_by_kraj.index.values
    for kraj_hodnota in kraje:
        kraj = kraj_hodnota[0]
        kategorie = kraj_hodnota[1]
        celkovy_pocet = grouped_by_kraj_celkem.loc[kraj, "hodnota"] / 2
        koeficient = 1000 / celkovy_pocet
        pocet_v_kategorii = grouped_by_kraj.loc[kraj_hodnota, "hodnota"]
        if kraj in json["kraje"]:
            json["kraje"][kraj][kategorie] = pocet_v_kategorii * koeficient
        else:
            json["kraje"][kraj] = {}
            json["kraje"][kraj][kategorie] = pocet_v_kategorii * koeficient

    okresy = grouped_by_okres.index.values
    for okres_hodnota in okresy:
        okres = okres_hodnota[0]
        kategorie = okres_hodnota[1]
        celkovy_pocet = grouped_by_okres_celkem.loc[okres, "hodnota"] / 2
        koeficient = 1000 / celkovy_pocet
        pocet_v_kategorii = grouped_by_okres.loc[okres_hodnota, "hodnota"]
        if okres in json["okresy"]:
            json["okresy"][okres][kategorie] = pocet_v_kategorii * koeficient
        else:
            json["okresy"][okres] = {}
            json["okresy"][okres][kategorie] = pocet_v_kategorii * koeficient

    return json


def get_areas_by_id(location_type: str, data: DataFrame):
    data.rename(columns={"uzemi_kod": location_type})
    ciselnik_df = pd.read_csv("uzemi_ciselniky.csv")
    ciselnik_df = ciselnik_df.dropna(how="all")
    ciselnik_df.drop(
        ciselnik_df.columns.difference(["Kod-obec", "kod-kraj", "kod-okres"]),
        axis=1, inplace=True)

    return pd.merge(data, ciselnik_df, how="inner", on=location_type)
