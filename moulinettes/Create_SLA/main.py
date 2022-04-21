import pandas as pd


SLA = pd.read_excel(r"input/SLA-v2.xlsx",
                    dtype="str")

list_columns = ['LOCALITE', '0', '1', '2', '3', '4', '5']
SLA_reference = pd.DataFrame(columns=list_columns)


for index in SLA.index:
    row = {
        'LOCALITE': SLA['Localisation'][index],
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0
    }
    SLA_reference = SLA_reference.append(row, ignore_index=True)
    days = SLA['Nouveau SLA'][index]
    if 'Lundi' in days:
        SLA_reference['0'][index] = 1
    if 'Mardi' in days:
        SLA_reference['1'][index] = 1
    if 'Mercredi' in days:
        SLA_reference['2'][index] = 1
    if 'Jeudi' in days:
        SLA_reference['3'][index] = 1
    if 'Vendredi' in days:
        SLA_reference['4'][index] = 1
    if 'Samedi' in days:
        SLA_reference['5'][index] = 1


SLA_reference.to_csv('output/SLA_reference.csv', sep=";",
                     index=False, encoding="ISO-8859-1")
