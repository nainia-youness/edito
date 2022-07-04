from __future__ import print_function
from mailmerge import MailMerge #pip install docx-mailmerge
from datetime import date
from docx2pdf import convert
import os
import pandas as pd
from datetime import datetime


template_sac = "input/BL_SAC.docx"
template_cab="input/BL_CAB.docx"
template_sac_cab="input/BL_SAC_CAB.docx"

es_parametres=pd.read_excel('input/ES_parametres.xlsx')  
input= pd.read_excel('input/fichier_input.xlsx')  
canvas_import_columns=["Type du colis","Adresse d'expédition","Adresse de livraison",
"Modèle du colis","Poids colis en KG","Valeur du produit à assurer en DH","Méthode contre remboursement",
"Montant contre remboursement en DH","Type du retour documentaire N°1","Référence du retour documentaire N°1",
"Type du retour documentaire N°2","Référence du retour documentaire N°2","Référence Externe",
"Code Barre","Nature","Commentaires"]
canvas_import = pd.DataFrame(columns=canvas_import_columns)


today = datetime.today().strftime('%d%m%Y_%H%M%S')
sac_data=[]
cab_data=[]
sac_cab_data=[]

def write_pdf(is_sac,is_cab,code_externe,agence,ville,adresse,telephone,quantite_sac,quantite_cab,date_bl):
    
    template=''
    if(is_sac and not is_cab):
        template=template_sac
    elif(is_cab and not is_sac):
        template=template_cab
    elif(is_cab and is_sac):
        template=template_sac_cab

    document = MailMerge(template)

    if(is_cab and is_sac):
        document.merge(
            agence=str(agence),
            ville=str(ville),
            adresse=str(adresse),
            destinataire=str(code_externe),
            telephone=str(telephone),
            date=str(date_bl),
            quantite_sac=str(quantite_sac),
            quantite_cab=str(quantite_cab)
        )
    else:
        quantite=0
        if(quantite_sac!=0):
            quantite=quantite_sac
        else:
            quantite=quantite_cab
        document.merge(
            agence=str(agence),
            ville=str(ville),
            adresse=str(adresse),
            destinataire=str(code_externe),
            telephone=str(telephone),
            date=str(date_bl),
            quantite=str(quantite)
        )

    
    
    bl_filename='output/BL_{0}_{1}'.format(code_externe,today)
    document.write(bl_filename+'.docx')
    convert(bl_filename+'.docx', bl_filename+'.pdf')
    if os.path.isfile(bl_filename+'.docx'):
        os.remove(bl_filename+'.docx')


def find_parametres(code_externe):
    for index, row in es_parametres.iterrows():
        if(row['Code externe']==code_externe):
            return row['Nom'],row['Ville'],row['Adresse'],row['Téléphone'],row['Agence']

def add_row_canvas_import_df(is_sac,is_cab,code_externe):
    global canvas_import
    added_row = {"Type du colis":'Colis',"Adresse d'expédition":'PLF NORD SLM',"Adresse de livraison":code_externe,
    "Modèle du colis":'( 20.0 * 20.0 * 20.0 )',"Poids colis en KG":2,"Valeur du produit à assurer en DH":'',
    "Méthode contre remboursement":'Aucun',
    "Montant contre remboursement en DH":'',"Type du retour documentaire N°1":'Bon de livraison (Physique)',
    "Type du retour documentaire N°2":'',"Référence du retour documentaire N°2":'',
    "Code Barre":'',"Nature":'',"Commentaires":''}
    if(is_sac and not is_cab):
        added_row['Référence du retour documentaire N°1']='CNSS KIT ALIMENTATION (SAC)'
        added_row["Référence Externe"]='CNSS KIT ALIMENTATION (SAC)'
    elif(is_cab and not is_sac):
        added_row['Référence du retour documentaire N°1']='CNSS KIT ALIMENTATION (CAB)'
        added_row["Référence Externe"]='CNSS KIT ALIMENTATION (CAB)'
    elif(is_cab and is_sac):
        added_row['Référence du retour documentaire N°1']='CNSS KIT ALIMENTATION (CAB/SAC)'
        added_row["Référence Externe"]='CNSS KIT ALIMENTATION (CAB/SAC)'
    canvas_import = pd.concat([canvas_import, pd.DataFrame.from_records([added_row])])



for index, row in input.iterrows():
    date_bl=row['Date']
    is_sac,is_cab=False,False
    quantite_sac=int(row['Quantité SAC'])
    quantite_cab=int(row['Quantité CAB'])
    if(quantite_sac!=0):
        is_sac=True
    if(quantite_cab!=0):
        is_cab=True
    
    code_externe=row['Code externe']
    nom,ville,adresse,telephone,agence=find_parametres(code_externe)
    add_row_canvas_import_df(is_sac,is_cab,code_externe)
    
    write_pdf(is_sac,is_cab,code_externe,agence,ville,adresse,telephone,quantite_sac,quantite_cab,date_bl)


canvas_import.to_excel('output/canvas_import_'+today+'.xlsx', index=False)