from datetime import datetime
import openpyxl
import os
import tkinter
import pandas as pd
import datetime
days = []
ind_nv = []

# d=date de visite
# day contient les collones de la ligne de SLA qui egale a 1


def next_weekday(d, day):
    days_ahead_list = []
    dat = datetime.date(int(d[6:10]), int(d[3:5]), int(d[0:2]))
    if len(day) != 0:
        for sla in day:
            days_ahead = int(sla) - dat.weekday()  # le jour - date de visite
            if days_ahead <= 0:
                days_ahead += 7
            days_ahead_list.append(days_ahead)
        return dat + datetime.timedelta(min(days_ahead_list))
    else:
        return dat


# ne l'utilise pas
def next_weekday2(d, weekday1, weekday2):
    dat = datetime.date(int(d[6:10]), int(d[3:5]), int(d[0:2]))
    days_ahead1 = int(weekday1) - dat.weekday()
    if days_ahead1 <= 0:  # Target day already happened this week
        days_ahead1 += 7
    days_ahead2 = int(weekday2) - dat.weekday()
    if days_ahead2 <= 0:  # Target day already happened this week
        days_ahead2 += 7
    return dat + datetime.timedelta(min(days_ahead1, days_ahead2))


SLA = pd.read_csv("./input/SLA_Reference.csv", sep=';',
                  dtype="str", encoding="utf-8")
Order = pd.read_excel(r"./input/Ordre_passage.xlsx",
                      dtype="str")  # Passage_order.xlsx

contraintes_agences = pd.read_excel(r"./input/Contraintes agences.xlsx",
                                    dtype="str")

# ajouter collone Prenom
Order['Prenom'] = 'Passage CNSS'


def update_creneau_horaire_de_passage(ind):
    # si la ville se trouve dans contraintes_agences on donne a "Creneau horaire de passage" le creneau correspondant
    # sinon, on lui donne le Creneau par defaut
    today = datetime.date.today()
    ramadan_dernier_jour = datetime.date(2022, 5, 2)
    if(today < ramadan_dernier_jour):
        creneau_par_defaut = '09:00-17:00'
    else:
        creneau_par_defaut = '10:00-17:00'
    ville = Order['Ville'][ind]
    Order['Creneau horaire de passage'][ind] = creneau_par_defaut
    for ctr_ind in contraintes_agences.index:
        ville_contrainte = contraintes_agences['Localité'][ctr_ind]
        Creneau_contrainte = contraintes_agences['Créneau'][ctr_ind]
        if(ville == ville_contrainte):
            Order['Creneau horaire de passage'][ind] = Creneau_contrainte


for ind in Order.index:
    update_creneau_horaire_de_passage(ind)
    # pour chaque ligne de order on verifie si on a l'id ext dans SLA
    for sla_ind in SLA.index:
        if Order["Identifiant externe client"][ind] == SLA["Code ES"][sla_ind]:
            for column in SLA.columns:
                if SLA[column][sla_ind] == "1":  # on met toutes les colonnes qui egale a 1 dans days
                    days.append(column)
            Order["Date-visite"][ind] = next_weekday(  # on change date de visite
                Order["Date-visite"][ind], days).strftime("%d/%m/%Y")
            days = []
            count = 1
    if count == 0:
        ind_nv.append(ind)
    else:
        count = 0
for nv in ind_nv:  # si l'id ext de la ligne n'existe pas dans SLA, remplace par "Code ES non Existant"
    Order["Date-visite"][nv] = "Code ES non Existant"
Order.to_excel("./output/Ordre_passage.xlsx")
