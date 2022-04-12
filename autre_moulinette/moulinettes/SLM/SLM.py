from datetime import datetime
import os
import openpyxl
import pandas as pd
import datetime
days = []
ind_nv = []
# dans days on a tout les colonnes du SLA qui ont une valeur de "1" dans cette ligne
# d = la date de visite
# d(date visite)=     day=[]


def next_weekday(d, day):
    days_ahead_list = []
    dat = datetime.date(int(d[6:10]), int(d[3:5]), int(
        d[0:2]))  # transforme la date de string a Date
    if "J1" in day:  # si on a la collone J1 =="1"
        dat = dat + datetime.timedelta(1)  # ajoute 1 jour a la date
        day.remove("J1")
    if "J2" in day:
        dat = dat + datetime.timedelta(2)
        day.remove("J2")
    if "J3" in day:
        dat = dat + datetime.timedelta(3)
        day.remove("J3")
    if len(day) != 0:  # il reste d'autre colonnes qui egale a "1"
        for sla in day:
            print(sla)
            days_ahead = int(sla) - dat.weekday()  # 0
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            days_ahead_list.append(days_ahead)
        return dat + datetime.timedelta(min(days_ahead_list))
    else:
        return dat


SLA = pd.read_csv("./input/SLM_Reference.csv", sep=';',
                  dtype="str", encoding="ISO-8859-1")
Order = pd.read_excel(r"./input/slm_planif.xlsx", dtype="str")

# change le format de la date dans order
Order["Date-visite"] = pd.to_datetime(Order["Date-visite"])
Order["Date-visite"] = Order["Date-visite"].dt.strftime("%d/%m/%Y")

count = 0


for ind in Order.index:
    for sla_ind in SLA.index:
        # pour chaque ligne , si la ville est dans notre SLA localite
        if Order["Ville"][ind] == SLA["LOCALITE"][sla_ind]:
            for column in SLA.columns:  # parcour tout les collones du SLA de la ligne
                if SLA[column][sla_ind] == "1":  # si l'un est egale a 1
                    # dans days on a tout les colonnes du SLA qui ont une valeur de "1" dans cette ligne
                    days.append(column)
            print(Order["Date-visite"][ind])
            Order["Date-visite"][ind] = next_weekday(
                Order["Date-visite"][ind], days).strftime("%d/%m/%Y")
            days = []
            count = 1
    if count == 0:
        # ind inv on a les indices des lignes de order ou il y'a aucune ville dans le SLA"localite"
        ind_nv.append(ind)
    else:
        count = 0
for nv in ind_nv:
    Order["Date-visite"][nv] = "Code ES non Existant"

Order.to_excel("./output/Ordre_passage.xlsx")
