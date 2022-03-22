import pandas as pd

d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)

d_output = {'col1': [], 'col2': []}
df_output = pd.DataFrame(data=d_output)


#a=df['col1'].tolist()
#df_output['col1'] = a
#print(df_output.head())
for index, row in df.iterrows():
    if(len(row["col1"])):
        print('hot')
    else:
        print("eddd")
 #   print(row["col1"])
 