import pandas as pd
from owlready2 import *
import  Edit_Ontologie as eo


#df = pd.DataFrame({'Nom':['Djebara','Benzeid'],'Prenom':['Ghiles','Houda'],'Age':[69,14],'Sexe':['Homme','Femme'],'MaladieChronique':['Khchanat rass','Tension arterielle'],'Traitement':['Soukout','Antidepresseurs'],'Situation familiale':['Divorcé','Divorcé'],'Durée depuis dernier voyage ':[1,154],'Durée depuis apparition des symptomes':[25487,457],'Daira':['Azefoun','Draria'],'Wilaya':['Tizi_Ouzou','Alger'],'Symptomes':['Fievre,Toux','Migraine,Fievre']})
#print(df)
#df.to_csv(r'./test.csv',index=False,header=True)

onto = get_ontology("F:\Raouf\Licence\L3\Web sémantique\Projet\sortie.owl").load()
ns = "http://sararaouf.org/onto.owl#"

patients = pd.read_csv("./test.csv")



for i in range(2):
    patient = patients.iloc[i]
    eo.create_patient(patient[0],patient[1],int(patient[2]),patient[3],patient[4],patient[5],patient[6],int(patient[7]),int(patient[8]),patient[9],patient[10],patient[11])

onto.save("sortiefinal.owl", format="ntriples")