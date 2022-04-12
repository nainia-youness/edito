from datetime import datetime

import pandas as pd


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
antsroute = pd.read_csv("./input/fichier_export.csv",
                        sep=';', dtype="str", encoding="utf-8")


# pas utiliser
reference = pd.read_csv("./input/ES_Reference.csv",
                        sep=';', dtype="str", encoding='ISO-8859-1')

# planif vide avec columns list column
planif = pd.DataFrame(columns=list_columns)
# missing_col=colonnes qu'on a dans planif mais pas dans antsroute
# pas utilisé
missing_col = planif.columns.difference(antsroute.columns).tolist()
# parasite_col=les colonnes qu'on a dans antsroute mais pas dans planif
# pas utilisé
parasite_col = antsroute.columns.difference(planif.columns).tolist()


# Si on a les colonnes "Identifiant externe client" et "Identifiant externe" dans antsroute
# =>on enleve "Identifiant externe" and change le nom de "Identifiant externe client" a "Identifiant externe"
if 'Identifiant externe client' in antsroute.columns:
    if 'Identifiant externe' in antsroute.columns:
        del antsroute["Identifiant externe"]
    antsroute = antsroute.rename(
        columns={'Identifiant externe client': 'Identifiant externe'})


# les colonnes qu'on a dans planif mais pas dans antsroute
# pas utilisé
parasite_col = planif.columns.difference(antsroute.columns).tolist()

# Ajoute dans planif toutes les colonnes qui existent sur antsroute
for p_col in list_columns:
    for ants_col in list(antsroute.columns):
        if p_col == ants_col:
            vals = antsroute[ants_col].tolist()
            planif[p_col] = vals


def add_zeros_to_identifiant_externe(index, row):
    row['Identifiant externe'] = str(row['Identifiant externe']).zfill(6)


def is_Heure_passage_prevu_valid(index, row):
    hour = int(row['Heure de passage prevu'][0:2])
    minute = int(row['Heure de passage prevu'][3:5])
    now = datetime.datetime.now()
    heure_passage = now.replace(minute=minute, hour=hour)
    # calculer la diffrence entre now et heure_passage
    dif = heure_passage-now
    dif_days, dif_hours, dif_minutes = dif.days, dif.seconds // 3600, dif.seconds // 60 % 60
    time_dif = now.replace(minute=dif_minutes, hour=dif_hours)
    # constant min_dif
    min_dif = now.replace(minute=5, hour=5)
    #
    if(time_dif > min_dif):
        return False
    else:
        return True


for index, row in planif.iterrows():
    #add_zeros_to_identifiant_externe(index, row)
    if len(row["Identifiant externe"]) == 6:  # si id ext est de 6 de longueur
        if is_d_m_yt(row["Date de depart"]) == True and row["Date de depart"] >= today:
            if is_hh_mm(row['Heure de passage prevu']) == True and is_Heure_passage_prevu_valid(index, row):
                valid_lines = valid_lines.append(row)
            else:
                row["rejection"] = "heure de passage non conforme"
                rejected_lines = rejected_lines.append(row)
        else:
            # ne fait rien avec cette information
            row["rejection"] = "date de depart non conforme"
            rejected_lines = rejected_lines.append(row)
            if is_hh_mm(row['Heure de passage prevu']) != True:
                row["rejection"] = "heure de passage non conforme"
                rejected_lines = rejected_lines.append(row)
    else:
        row["rejection"] = "Identifiant externe non conforme"
        rejected_lines = rejected_lines.append(row)
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
