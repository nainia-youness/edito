from datetime import datetime
import os
import openpyxl
import pandas as pd
import datetime
days=[]
ind_nv=[]
def next_weekday(d, day):
    days_ahead_list = []
    dat = datetime.date(int(d[6:10]), int(d[3:5]), int(d[0:2]))
    if "J1" in day:
        dat=dat + datetime.timedelta(1)
        day.remove("J1")
    if "J2" in day:
        dat=dat + datetime.timedelta(2)
        day.remove("J2")
    if "J3" in day:
        dat=dat + datetime.timedelta(3)
        day.remove("J3")
    if len(day)!=0:
        for sla in day:
            print(sla)
            days_ahead = int(sla) - dat.weekday()
            if days_ahead <= 0: # Target day already happened this week
                days_ahead += 7
            days_ahead_list.append(days_ahead)
        return dat + datetime.timedelta(min(days_ahead_list))
    else:
        return dat


SLA=pd.read_csv("C:/Users/aboulfath/Desktop/SLM_Reference.csv", sep=';', dtype="str", encoding="ISO-8859-1")
Order=pd.read_excel (r"C:/Users/aboulfath/Desktop/slm_planif.xlsx",dtype="str")
Order["Date-visite"]=pd.to_datetime(Order["Date-visite"])
Order["Date-visite"]=Order["Date-visite"].dt.strftime("%d/%m/%Y")
count=0


for ind in Order.index:
    for sla_ind in SLA.index:
        if Order["Ville"][ind]==SLA["LOCALITE"][sla_ind]:#in you find one localite in sla = to ville in order
            for column in SLA.columns:
                if SLA[column][sla_ind]=="1":#see if one row in localite =="1"
                    days.append(column)
            print(Order["Date-visite"][ind])
            Order["Date-visite"][ind]=next_weekday(Order["Date-visite"][ind], days).strftime("%d/%m/%Y")
            days=[]
            count=1
    if count==0:
        ind_nv.append(ind)
    else:
        count=0
for nv in ind_nv:
    Order["Date-visite"][nv]="Code ES non Existant"
Order.to_excel("C:/Users/aboulfath/Desktop/Antsroute_file/Ordre_passage.xlsx")