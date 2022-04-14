from datetime import datetime
import openpyxl
import os
import tkinter
import pandas as pd
import datetime


Order = pd.read_excel(r"./input/Ordre_passage.xlsx",
                      dtype="str")  # Passage_order.xlsx

contraintes_agences = pd.read_excel(r"./input/Contraintes agences.xlsx",
                                    dtype="str")


def ajouter_colonne_prenom():
    Order['Prenom'] = 'Passage CNSS'


def update_creneau_horaire_de_passage(ind):
    for ind in Order.index:
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


ajouter_colonne_prenom()
update_creneau_horaire_de_passage()
Order.to_excel("./output/Ordre_passage.xlsx")
