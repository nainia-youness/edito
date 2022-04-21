from datetime import datetime

import pandas as pd
import glob

def is_hh_mm(t):
    try:
        t = pd.to_datetime(t)
        t = datetime.strptime('10:21', '%H:%M')
    except:
        return False
    else:
        return True


def is_d_m_yt(t):
    try:
        t = pd.to_datetime(t)
        t = datetime.strptime('01/01/2000', '%d/%m/%Y')
    except:
        return False
    else:
        return True


today = datetime.today().strftime('%d/%m/%Y')
valid_lines = pd.DataFrame()
rejected_lines = pd.DataFrame()
parasite_col = []
list_columns = ["Plaque d'immatriculation", "Agent", "Date de depart", "Date d'echeance", "Creneau horaire de passage", "Type d'intervention", "Heure de passage prevu", "Duree", "Type", "Duree maximale de transport",
                "Commentaires", "Identifiant externe", "Prenom", "Nom", "Mobile", "Telephone", "Courriel",
                "Adresse", "Latitude", "Longitude", "Competence", "Agent privilegie", "Poids", "Volume",
                "Référence de commande", "Hub", "Partner"]

#input
for file in glob.glob("input/Export-routes-du*.csv"):
    antsroute = pd.read_csv(file,sep=';', dtype="str", encoding="utf-8")

planif = pd.DataFrame(columns=list_columns)


# Si on a les colonnes "Identifiant externe client" et "Identifiant externe" dans antsroute
# =>on enleve "Identifiant externe" and change le nom de "Identifiant externe client" a "Identifiant externe"
if 'Identifiant externe client' in antsroute.columns:
    if 'Identifiant externe' in antsroute.columns:
        del antsroute["Identifiant externe"]
    antsroute = antsroute.rename(
        columns={'Identifiant externe client': 'Identifiant externe'})

# Ajoute dans planif toutes les colonnes qui existent sur antsroute
for p_col in list_columns:
    for ants_col in list(antsroute.columns):
        if p_col == ants_col:
            vals = antsroute[ants_col].tolist()
            planif[p_col] = vals


def is_hub_valid(index,row):
    global rejected_lines
    hub=row["Hub"]
    if(hub!="M2T"):
        row["rejection"] = "Hub n'est pas egale a M2T"
        rejected_lines = rejected_lines.append(row)
        return False
    return True

def remove_column_prenom(planif):
    if 'Prenom' in planif.columns:
        return planif.drop(columns=['Prenom'])

#def remove_first_row(planif):
#    return planif.drop([0])        

def ajouter_zeros_a_id_externe(index,row):
    if(len(row["Identifiant externe"]) != 6):
        row['Identifiant externe']=row['Identifiant externe'].zfill(6)


planif=remove_column_prenom(planif)
for index, row in planif.iterrows():
    if(not is_hub_valid(index,row)):
        continue
    ajouter_zeros_a_id_externe(index,row)
    if len(row["Identifiant externe"]) == 6:# si id ext est de 6 de longueur
        #filtre sur la date de depart et heure de passage
        if is_d_m_yt(row["Date de depart"]) == True and row["Date de depart"] >= today:
            if is_hh_mm(row['Heure de passage prevu']) == True:
                valid_lines = valid_lines.append(row)
            else:
                row["rejection"] = "heure de passage non conforme"
                rejected_lines = rejected_lines.append(row)
        else:
            row["rejection"] = "date de depart non conforme"
            rejected_lines = rejected_lines.append(row)
            if is_hh_mm(row['Heure de passage prevu']) != True:
                row["rejection"] = "heure de passage non conforme"
                rejected_lines = rejected_lines.append(row)
    else:
        #filtre sur l'identifiant externe
        row["rejection"] = "Identifiant externe non conforme"
        rejected_lines = rejected_lines.append(row)
        #filtre sur la date de depart et heure de passage
        if is_d_m_yt(row["Date de depart"]) != True or row["Date de depart"] < today:
            row["rejection"] = "date de depart non conforme"
            rejected_lines = rejected_lines.append(row)
            if is_hh_mm(row['Heure de passage prevu']) != True:
                row["rejection"] = "heure de passage non conforme"
                rejected_lines = rejected_lines.append(row)

planif_date = today = datetime.today().strftime('%d%m%Y')
nomination = "PLANIFICATION_CNSS_{}_{}".format(planif_date, len(valid_lines))


valid_lines.to_csv('output/{}.csv'.format(nomination), sep=";", index=False)
rejected_lines.to_csv('output/fichier_rejeté.csv', sep=";", index=False)