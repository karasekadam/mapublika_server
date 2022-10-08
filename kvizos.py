import pandas as pd
import json
import os


def get_average(json_file):
    """
    fce vraci slovnik s kraji a okresy a pro kazdy z nich slovnik s moznymi hodnotami zaznamu k nim prumer na vsechny kraje/okresy
    """
    with open(json_file, 'r') as json_file:
        data = json.loads(json_file.read())
    options = {"kraje": {}, "okresy": {}}
    for uzemi in data:
        for cast, hodnoty_dic in data[uzemi].items():
            for hodnota, pocet in hodnoty_dic.items():
                if hodnota not in options[uzemi].keys():
                    options[uzemi][hodnota] = 0
                options[uzemi][hodnota] += int(pocet)
        if uzemi == "kraje":
            for hodnota, pocet in options[uzemi].items():
                options[uzemi][hodnota] = options[uzemi][hodnota]//14
        else:
            for hodnota, pocet in options[uzemi].items():
                options[uzemi][hodnota] = options[uzemi][hodnota]//76
    return options


def rozdil_prumeru(json_file_org, kod_uzemi):
    """
    Fce dostane kod kraje/okresy, vrati ciselny rozdil hodnoty oproti prumeru
    """
    with open(json_file_org, 'r') as json_file:
        data = json.loads(json_file.read())
    uzemi = "kraje" if (len(kod_uzemi) == 5) else "okresy"
    options_uzemi = data[uzemi][kod_uzemi]
    final = get_average(json_file_org)
    for hodnota, pocet in options_uzemi.items():
        final[uzemi][hodnota] = int(pocet) - int(final[uzemi][hodnota])
    return final[uzemi]

def make_final_jason(json_file, kod_uzemi):
    final = generuj_otazky_prumer(json_file, kod_uzemi)
    return final

def generuj_otazky_prumer(json_file, kod_uzemi):
    final_dict = {}
    q_start = "Je váš " + ("kraj" if len(kod_uzemi) == 5 else "okres") + " nadprůměrný v hodnotě " + (json_file[9:-5])
    rozdily = rozdil_prumeru(json_file, kod_uzemi)
    for option, value in rozdily.items():
        question = q_start + " a možnosti " + option + " ?"
        answer = ("Ano" if (value > 0) else "Ne")
        final_dict[question] = answer

    q_start = "Je váš " + ("kraj" if len(kod_uzemi) == 5 else "okres") + " podprůměrný v hodnotě " + (json_file[9:-5])
    rozdily = rozdil_prumeru(json_file, kod_uzemi)
    for option, value in rozdily.items():
        question = q_start + " a možnosti " + option + " ?"
        answer = ("Ano" if (value < 0) else "Ne")
        final_dict[question] = answer
    return final_dict

"""  
def generuj_otazky_ktery_kraj(json_file, kod_uzemi):
    final_dict = {}
    q_start = "Který "+ ("kraj" if len(kod_uzemi) == 5 else "okres") + " má nejvyšší hodnotu " + (json_file.toString()[6:])
    rozdily = rozdil_prumeru(json_file, kod_uzemi)
    for option, value in rozdily:
        question = q_start + " a možnosti " + option + " ?"
        answer = ("Ano" if (value > 0) else "Ne")
        final_dict[question] = answer

    q_start = "Který "+ ("kraj" if len(kod_uzemi) == 5 else "okres") + " má nejnižšší hodnotu " + (json_file.toString()[6:])
    for option, value in rozdily:
        question = q_start + " a možnosti " + option + " ?"
        answer = ("Ano" if (value > 0) else "Ne")
        final_dict[question] = answer
    return final_dict
""" 


"""
def find_maximum(json_file):

    with open(json_file, 'r') as json_file:
        data = json.loads(json_file.read())
    options = {"kraje": {}, "okresy": {}}
    for uzemi in data:
        for cast, hodnoty_dic in data[uzemi].items():
            if options[uzemi].empty():
                options[uzemi] = fill_empty_dict(options[uzemi], cast, hodnoty_dic)
            
            for hodnota, pocet in hodnoty_dic.items():
                if hodnota not in options[uzemi].keys():
                    options[uzemi][hodnota] = 0
                options[uzemi][hodnota] += int(pocet)

def fill_empty_dict(cast, hodnoty_dic):
    
    #naplni dictionary s maximalnimi hodnotami prvni hodnotami - vytvori sablonu
    
    template = hodnoty_dic.copy()
    for key, max_value in template.items():
        template[key] = [cast, max_value]
    return template

""" 

def run_datasets(kod_okres, kod_kraj):
    path = "public_datasets"
    dir_list = os.listdir(path)
    final_json = {}
    for dataset in dir_list:
        final_json.update(make_final_jason(path + "/" + dataset, kod_okres))
        final_json.update(make_final_jason(path + "/" + dataset, kod_kraj))
    return final_json
   








if __name__ == '__main__':
    run_datasets("CZ0806", "CZ032")
    #make_final_jason("public_pocetDeti.json", "CZ0806")

    
