import os
from tkinter.filedialog import askopenfile
from tkinter import ttk, filedialog
from datetime import datetime
from tkinter import filedialog
import traceback
import pandas as pd
from tkinter import *

output_canvas = ["Type du colis", "Adresse d'expédition",
          "Nom du client final", "Email du client final",
          "Téléphone du client final", "Ville du client final",
          "Code Postal du client final", "Adresse du Client Final",
          "Modèle du colis", "Poids Colis en KG", "Valeur du produit à assurer en DH", 
          "Méthode contre remboursement", "Montant contre remboursement en DH", 
          "Référence Externe","Type du retour documentaire N°1", 
          "Référence du retour documentaire N°1","Type du retour documentaire N°2", 
          "Référence du retour documentaire N°2", "Nature", "commentaires"]

output_file_df = pd.DataFrame(columns=output_canvas)


# Create an instance of tkinter frame
win = Tk()
win.title("Moulinette")
# Set the geometry of tkinter frame
win.geometry("700x350")
win.minsize(400,350)


def format_tel(tel):
    return "0"+tel[len(tel)-9:len(tel)]

def change_phone_number_format(input_file_df):
    input_file_df.iloc[:, 2] = input_file_df.iloc[:, 2].apply(format_tel)

def get_output_file_name(selected_folder_path):
    now = datetime.now()
    creation_time = now.strftime("%Y%m%d_%H%M")
    output_file_path="{}/fichier_import_{}.xlsx".format(str(selected_folder_path),creation_time)
    return output_file_path

def update_output_file(output_file_df,input_file_df,variables):
    adresse_expedition=variables[0]
    modele_colis=variables[1]
    input_canvas=input_file_df.columns
    for index, _ in input_file_df.iterrows():
        #Type du colis
        output_file_df.loc[index,output_canvas[0]] = "Colis" 
        #Adresse d'expédition
        output_file_df.loc[index,output_canvas[1]] = adresse_expedition
        #Nom du client final
        output_file_df.loc[index,output_canvas[2]] = input_file_df.loc[index, input_canvas[1]]
        #Email du client final
        output_file_df.loc[index,output_canvas[3]] = ""
        #Téléphone du client final
        output_file_df.loc[index,output_canvas[4]] = input_file_df.loc[index, input_canvas[2]]
        #Ville du client final
        output_file_df.loc[index,output_canvas[5]] = input_file_df.loc[index, input_canvas[3]]
        #Code Postal du client final
        output_file_df.loc[index,output_canvas[6]] = ""
        #Adresse du Client Final
        output_file_df.loc[index,output_canvas[7]] = "00 "+input_file_df.loc[index, input_canvas[5]]
        #Modèle du colis
        output_file_df.loc[index,output_canvas[8]] = modele_colis
        #Poids Colis en KG
        output_file_df.loc[index,output_canvas[9]] = "2.5"
        #Valeur du produit à assurer en DH
        output_file_df.loc[index,output_canvas[10]] = input_file_df.loc[index, input_canvas[13]]
        #Méthode contre remboursement
        if(input_file_df.loc[index, input_canvas[8]]!='0'):
            output_file_df.loc[index,output_canvas[11]]='Espèces'
        else:
            output_file_df.loc[index,output_canvas[11]]='Aucun'
        #Montant contre remboursement en DH
        output_file_df.loc[index,output_canvas[12]] = input_file_df.loc[index, input_canvas[8]]
        #Référence Externe
        output_file_df.loc[index,output_canvas[13]] = input_file_df.loc[index, input_canvas[10]]
        #Type du retour documentaire N°1
        output_file_df.loc[index,output_canvas[14]] = "BL/Contrat (Physique)"
        #Référence du retour documentaire N°1
        output_file_df.loc[index,output_canvas[15]] = "inwi12"
        #Type du retour documentaire N°2
        output_file_df.loc[index,output_canvas[16]] = "Carte d'identité (Digital)"
        #Référence du retour documentaire N°2
        output_file_df.loc[index,output_canvas[17]] = "inwi1"
        #Nature
        output_file_df.loc[index,output_canvas[18]] = input_file_df.loc[index,input_canvas[0]]
        #commentaire
        output_file_df.loc[index,output_canvas[19]] = input_file_df.loc[index,input_canvas[18]]



def open_file(variables):
    Label(win, text="Veuillez ne pas fermer l'interface jusqu'à terminaison de l'exécution",font=('Aerial 11')).pack()

    file = filedialog.askopenfile(mode='r', filetypes=[('Excel Files', '*.xlsx')])
    if file:
        filepath = os.path.abspath(file.name)
        try:

            Label(win, text="The File is located at : {}".format(str(filepath)), font=('Aerial 11')).pack()

            input_file_df = pd.read_excel(str(filepath), dtype="str")
            change_phone_number_format(input_file_df)

            update_output_file(output_file_df,input_file_df,variables)

            selected_folder = filedialog.askdirectory() #select the folder where you put the output file 
            selected_folder_path = os.path.abspath(selected_folder)

            output_file_path=get_output_file_name(selected_folder_path)

            Label(win, text="The Folder selected is : {}".format(str(selected_folder_path)), font=('Aerial 11')).pack()
            output_file_df.to_excel(output_file_path, index=False)
            Label(win, text="La conversion est terminée",font=('Aerial 11')).pack()

        except Exception:
            selected_folder = filedialog.askdirectory()
            selected_folder_path = os.path.abspath(selected_folder)

            #write the error in a log file
            with open(str(selected_folder_path)+"/log.txt", "w") as log:
                traceback.print_exc(file=log)
            pass


def show_page_2(variables):
    # Add a Label widget
    label = Label(win, text="Veuillez cliquer sur le bouton pour choisir le fichier", font=('Georgia 13'))
    label.pack(pady=10)

    # Create a Button
    ttk.Button(win, text="Browse", command=open_file(variables)).pack(pady=20) #when you click on the button, open_file() is executed


def show_page_1(win):
    
    options_list = [
        [
            "E-shop",#default
            "Sntl supply chain"
        ],
        [
            "(10.0 * 10.0 * 10.0)",#default
            "(15.0 * 124.0 * 20.0)",
            "(15.0 * 5.0 * 5.0)"
        ]
    ]

    labels_list=[
        "Adresses d’expéditions",
        "Modèles de colis"
    ]

    frame=Frame(win)
    label = Label(frame, text="Veuillez entrer vos preference", font=('Georgia 13')) 
    label.grid(row = 0, column = 0,columnspan = 2,pady=30,sticky=N)

    def generate_rows(frame,row_index,label,options):
        l1 = Label(frame, text = label,font=('Georgia 13'))
        l1.grid(row = row_index+1, column = 0, sticky = W, pady = 10)

        #dropdown
        clicked = StringVar(frame)
        clicked.set(options[0])
        w1 = OptionMenu(frame, clicked, *options)
        w1.grid(row = row_index+1, column = 1, padx=30)
        return clicked
    variables=[]
    for i in range(len(options_list)):
        var=generate_rows(frame,i,labels_list[i]+':',options_list[i])
        variables.append(var)



    but=Button(frame, text="Suivant",command=lambda: destroy_page())

    def destroy_page():
        frame.destroy()
        show_page_2([var.get() for var in variables])

    but.grid(row = len(options_list)+1,column=0, columnspan = 2,pady=20,sticky=N+S+E+W)

    frame.pack(pady=20)


show_page_1(win)
win.mainloop()
