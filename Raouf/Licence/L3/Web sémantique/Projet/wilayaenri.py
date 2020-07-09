import pandas as pd

wilayas = pd.read_csv("ressources/wilaya.csv")
f = open("htmlwil.txt","w")
for i in range(len(wilayas)):
    nom_wilaya = wilayas.iloc[i]['nom']
    f.write("<option value=\""+nom_wilaya+"\"> "+nom_wilaya+" </option>\n")