from datetime import datetime
import openpyxl
import os
import tkinter
import pandas as pd
import datetime
import glob

#Ordre de passage (1)
for file in glob.glob("input/Ordre de passage*.xlsx"):
    Order = pd.read_excel(file,dtype="str")  # Passage_order.xlsx

contraintes_agences = pd.read_excel(r"./input/Contraintes agences.xlsx",
                                    dtype="str")


def ajouter_colonne_prenom():
    Order.insert(5, column='Prenom', value='Passage CNSS')


def string_to_date(d):
    return datetime.date(int(d[6:10]), int(d[3:5]), int(d[0:2]))


def date_to_string(d):
    return d.strftime("%d/%m/%Y")


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

def assurer_dimande_day_off(ind):
    date_visite = string_to_date(Order['Date-visite'][ind])
    if(date_visite.weekday() == 6):
        Order["Date-visite"][ind] = date_to_string(
            date_visite+datetime.timedelta(1))


ajouter_colonne_prenom()
for ind in Order.index:
    assurer_dimande_day_off(ind)
    update_creneau_horaire_de_passage(ind)

Order.to_excel("./output/Ordre_passage.xlsx",index=False)
