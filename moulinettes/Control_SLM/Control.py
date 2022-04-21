import pandas as pd


Order = pd.read_excel(r"./input/Ordre_passage.xlsx",
                      dtype="str")


def retrouver_les_colis_supprimés():
    global Order
    nouveau_order=Order.copy()
    for index,row in nouveau_order.iterrows():
        colis_regroupe=row['Colis-regroupés']
        if(colis_regroupe!='aucun'):
            ids = colis_regroupe.split("/")
            for id in ids:
                nouveau_order['Id'][index]=id
                Order=Order.append([row],ignore_index=True)
    Order=Order.drop(columns=['Colis-regroupés'])


retrouver_les_colis_supprimés()
Order.to_excel("./output/Ordre_passage.xlsx",index=False)