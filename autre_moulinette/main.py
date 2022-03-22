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
list_columns = ["Plaque d'immatriculation", "Agent", "Date de depart", "Date d'echeance", "Creneau horaire de passage"
    , "Type d'intervention", "Heure de passage prevu", "Duree", "Type", "Duree maximale de transport",
                "Commentaires", "Identifiant externe", "Prenom", "Nom", "Mobile", "Telephone", "Courriel",
                "Adresse", "Latitude", "Longitude", "Competence", "Agent privilegie", "Poids", "Volume",
                "Référence de commande", "Hub", "Partner"]
antsroute = pd.read_csv("C:/Users/aboulfath/Desktop/fichier_export.csv", sep=';', dtype="str", encoding="utf-8")

#reference never used
reference=pd.read_csv("C:/Users/aboulfath/Desktop/ES_Reference.csv",sep=';', dtype="str",encoding='ISO-8859-1')

planif = pd.DataFrame(columns=list_columns)
#missing colmuns= columns we need to add to antsroute file
missing_col = planif.columns.difference(antsroute.columns).tolist()
#parasite columns= columns we need to remove from antsroute file
parasite_col = antsroute.columns.difference(planif.columns).tolist()

# if we have both "Identifiant externe client" and "Identifiant externe"
#then remove Identifiant externe and rename "Identifiant externe client" to "Identifiant externe"
if 'Identifiant externe client' in antsroute.columns:
    if 'Identifiant externe' in antsroute.columns:
        del antsroute["Identifiant externe"]
    antsroute = antsroute.rename(columns={'Identifiant externe client': 'Identifiant externe'})


#change parasite_col ??????
parasite_col = planif.columns.difference(antsroute.columns).tolist()


#insert in planif all columns that exist in antsroute
for p_col in list_columns:
    for ants_col in list(antsroute.columns):
        if p_col == ants_col:
            vals = antsroute[ants_col].tolist()
            planif[p_col] = vals



for index, row in planif.iterrows():
        if len(row["Identifiant externe"])==6:#???????
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
valid_lines.to_csv('C:/Users/aboulfath/Desktop/CNSS_Control/{}.csv'.format(nomination), sep=";", index=False)
rejected_lines.to_csv('C:/Users/aboulfath/Desktop/CNSS_Control/fichier_rejeté.csv', sep=";", index=False)