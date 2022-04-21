from datetime import datetime
from multiprocessing.reduction import duplicate
import os
import openpyxl
import pandas as pd
import datetime
# dans days on a tout les colonnes du SLA qui ont une valeur de "1" dans cette ligne
# d = la date de visite
# d(date visite)=     day=[]


def next_weekday(d, day):
    days_ahead_list = []
    dat = string_to_date(d)
    if len(day) != 0:
        for sla in day:
            days_ahead = int(sla) - dat.weekday()  # le jour - date de visite
            if days_ahead <= 0:
                days_ahead += 7
            days_ahead_list.append(days_ahead)
        return dat + datetime.timedelta(min(days_ahead_list))
    else:
        return dat


def string_to_date(d):
    return datetime.date(int(d[6:10]), int(d[3:5]), int(d[0:2]))


def date_to_string(d):
    return d.strftime("%d/%m/%Y")


# inputs
SLA = pd.read_csv("./input/SLA_Reference.csv", sep=';',
                  dtype="str", encoding="ISO-8859-1")
Order = pd.read_excel(r"./input/slm_planif.xlsx",
                      dtype="str")

temps_acheminements = pd.read_excel(
    r"./input/temps_d'acheminements.xlsx", dtype="str")

contraintes_agences = pd.read_excel(r"./input/Contraintes agences.xlsx",
                                    dtype="str")


# change le format de la date dans order
Order["Date-visite"] = pd.to_datetime(Order["Date-visite"])
Order["Date-visite"] = Order["Date-visite"].dt.strftime("%d/%m/%Y")


def update_creneau_horaire_de_passage():
    for ind in Order.index:
        # si la ville se trouve dans contraintes_agences on donne a "Creneau horaire de passage" le creneau correspondant
        # sinon, on lui donne le Creneau par defaut
        today = datetime.date.today()
        ramadan_dernier_jour = datetime.date(2022, 5, 2)
        if(today < ramadan_dernier_jour):
            creneau_par_defaut = '09:00-17:00'  # creneau de ramadan
        else:
            creneau_par_defaut = '10:00-17:00'
        ville = Order['Ville'][ind]
        Order['Creneau horaire de passage'][ind] = creneau_par_defaut
        for ctr_ind in contraintes_agences.index:
            ville_contrainte = contraintes_agences['Localité'][ctr_ind]
            Creneau_contrainte = contraintes_agences['Créneau'][ctr_ind]
            if(ville == ville_contrainte):
                Order['Creneau horaire de passage'][ind] = Creneau_contrainte

def ajouter_jours_sans_dimanche(date_visite,jours_a_ajouter,nbr_jours):
    result=jours_a_ajouter
    for i in range(nbr_jours):
        result+=datetime.timedelta(1)
        if((date_visite+jours_a_ajouter).weekday() == 6):
            # si le jour tombe sur samedi, il faut mettre lundi a la place
            result += datetime.timedelta(1)
    return result


def ajouter_temps_acheminements():
    for i in Order.index:
        for j in temps_acheminements.index:
            # si on trouve la ville dans le fichier "temps d'acheminement" on doit ajouter le nombre de jour
            # correspondant a la date de visite
            if Order["Ville"][i] == temps_acheminements["Localisation associées"][j]:
                date_visite = string_to_date(Order["Date-visite"][i])
                jours_a_ajouter = datetime.timedelta(0)
                if(temps_acheminements["J+1"][j] == '1'):
                    jours_a_ajouter=ajouter_jours_sans_dimanche(date_visite,jours_a_ajouter,1)

                if(temps_acheminements["J+2"][j] == '1'):
                    jours_a_ajouter=ajouter_jours_sans_dimanche(date_visite,jours_a_ajouter,2)

                if(temps_acheminements["J+3"][j] == '1'):
                    jours_a_ajouter=ajouter_jours_sans_dimanche(date_visite,jours_a_ajouter,3)

                Order["Date-visite"][i] = date_to_string(
                    date_visite+jours_a_ajouter)


def ajouter_SLA():
    days = []
    ind_nv = []
    count = 0
    for ind in Order.index:
        for sla_ind in SLA.index:
            # pour chaque ligne , si la ville est dans notre SLA localite
            if Order["Ville"][ind] == SLA["LOCALITE"][sla_ind]:
                for column in SLA.columns:  # parcour tout les collones du SLA de la ligne
                    if SLA[column][sla_ind] == "1":  # si l'un est egale a 1
                        # dans days on a tout les colonnes du SLA qui ont une valeur de "1" dans cette ligne
                        days.append(column)
                Order["Date-visite"][ind] = date_to_string(next_weekday(
                    Order["Date-visite"][ind], days))
                days = []
                count = 1
        if count == 0:
            # ind inv on a les indices des lignes de order ou il y'a aucune ville dans le SLA "localite"
            ind_nv.append(ind)
        else:
            count = 0
    for nv in ind_nv:
        Order["Date-visite"][nv] = "Code ES non Existant"

def supprimer_colis_repete():
    global Order
    Order.loc[:,'Colis-regroupés'] = 'aucun'
    cols=list(Order.columns)
    cols.remove('Id')
    duplicated_rows=Order.loc[Order.duplicated(subset=cols), :]
    Order=Order.drop_duplicates(subset=cols)
    for ind1 in Order.index:
        colis_regroupe=''
        for ind2 in duplicated_rows.index:
            if(is_rows_equal(ind1,ind2,duplicated_rows,cols)):
                colis_regroupe+=duplicated_rows['Id'][ind2]+'/'
        if(colis_regroupe!=''):
            if(colis_regroupe[-1]=='/'):
                colis_regroupe=colis_regroupe[:-1]
            Order['Colis-regroupés'][ind1]=colis_regroupe

def is_rows_equal(ind1,ind2,duplicated_rows,cols):
    is_equal=True
    for column in cols:
        value1=Order[column][ind1]
        value2=duplicated_rows[column][ind2]
        if((pd.isnull(value1) and not pd.isnull(value2)) or (pd.isnull(value2) and not pd.isnull(value1))):
            is_equal=False
        if(not pd.isnull(value1) and not pd.isnull(value2)):
            if(Order[column][ind1]!=duplicated_rows[column][ind2]):
                is_equal=False
    return is_equal


supprimer_colis_repete()
ajouter_temps_acheminements()
update_creneau_horaire_de_passage()
ajouter_SLA()
Order.to_excel("./output/Ordre_passage.xlsx",index=False)
