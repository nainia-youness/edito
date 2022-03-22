#from tkinter import ttk, filedialog
#from tkinter import *
import pandas as pd
import numpy as np
from tkinter import *
# Create an instance of tkinter frame
win = Tk()

# Set the geometry of tkinter frame
win.geometry("700x350")

# Add a Label widget



frame=Frame(win)


label = Label(frame, text="Veillez entrez vos preference", font=('Georgia 13')) 
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



options_list = [
    [
        "Jan",
        "Feb"
    ],
    [
        "Jan",
        "Feb"
    ]
]

labels_list=[
    "Adresse expoediteur",
    "rows2"
]

variables=[]
for i in range(len(options_list)):
    var=generate_rows(frame,i,labels_list[i]+':',options_list[i])
    variables.append(var)



but=Button(frame, text="Suivant",command=lambda: my_show())

def my_show():
    print(variables[0].get())
    print(variables[1].get())
    frame.destroy()

but.grid(row = len(options_list)+1,column=0, columnspan = 2,pady=20,sticky=N+S+E+W)

frame.pack(pady=20)

win.mainloop()








b="""df_input = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                        columns=['a', 'b', 'c'])
df_input_canvas=df_input.columns

df_output = pd.DataFrame(columns=['c', 'd', 'e'])
expediteur = 'Eshop'
obj={'a': 5, 'c': 5, 'b': 5}
df['']
df['3rd_col'] = df['ID'].map(d)
for index, row in df_input.iterrows():
    row[0]=5

print(df_input.head())


print('head')
print(df_output.head())
"""