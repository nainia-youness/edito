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

num = 32548

nbr_digits = len(str(num))

result = str(num).zfill(6)


now = datetime.datetime.now()

current_time = now.strftime("%H:%M")


date = '15:00'
hour = int(date[0:2])
minute = int(date[3:5])


def is_Heure_passage_prevu_valid(row):

    hour = int(row[0:2])
    minute = int(row[3:5])
    now = datetime.datetime.now()
    heure_passage = now.replace(minute=minute, hour=hour)
    # calculer la diffrence entre now et heure_passage
    dif = heure_passage-now
    dif_days, dif_hours, dif_minutes = dif.days, dif.seconds // 3600, dif.seconds // 60 % 60
    time_dif = now.replace(minute=dif_minutes, hour=dif_hours)
    print(time_dif)
    # constant min_dif
    min_dif = now.replace(minute=5, hour=5)
    #
    if(time_dif > min_dif):
        return False
    else:
        return True


print(is_Heure_passage_prevu_valid('11:00'))
