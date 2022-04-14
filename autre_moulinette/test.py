from datetime import datetime
import sys
import pandas as pd
import datetime
d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)

d_output = {'col11': [5, 5], 'col22': [6, 6]}
df_output = pd.DataFrame(data=d_output)


# a=df['col1'].tolist()
# df_output['col1'] = a
# print(df_output.head())
# for index, row in df.iterrows():
#    if(len(row["col1"])):
#        print('hot')
#    else:
#        print("eddd")

# for column in df.columns:
#    print(column)
#   print(row["col1"])

# print(datetime.timedelta(1))

# for ind in df.index:
#    print(df['col1'][ind])


temps_acheminements = pd.read_excel(
    r"moulinettes/SLM/input/temps_d'acheminements.xlsx", dtype="str")

date_visite = '30/03/2022'

d = datetime.date(int(date_visite[6:10]), int(date_visite[3:5]), int(
    date_visite[0:2]))
print(d+datetime.timedelta(1))
print(d.weekday())
# for i in temps_acheminements.index:
#    print(temps_acheminements["Localisation associées"][i])
