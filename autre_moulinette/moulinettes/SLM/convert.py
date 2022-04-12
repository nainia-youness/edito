import pandas as pd

# excel to csv
read_file = pd.read_excel('input/SLM_Reference.xlsx')
read_file.to_csv('input/SLM_Referenceeee.csv',
                 index=None, header=True, delimiter=';')

# csv to excel
# read_file = pd.read_csv(r'input/SLM_Reference.csv',
#                        delimiter=';')
#read_file.to_excel(r'input/SLM_Reference.xlsx', index=False)
