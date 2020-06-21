from owlready2 import *
import pandas as pd



def ordonner_classe(ontol):
    d = {}
    for i in ontol.classes():
        d[i.name] = i
    d = sorted(d.items(), key=lambda x: x[0])

    L = []
    for i in range(len(d)):
        L.append(d[i][1])
    return L

def enum_class(onto):
    liste = ordonner_classe(onto)
    cpt = 0
    for i in liste:
        print(cpt,'-', str(i).split('.')[-1])
        cpt += 1
    return liste

def create_patient(nom , prenom , age , sexe , maladiechronique , traitement , situationfam , dureederniervoyage, dureedepuisappsymp , daira,wilaya, symptomes):
    class_patient = list_class[8]
    P = class_patient()
    P.Nom = nom
    P.Prenom.append(prenom)
    P.Age = age
    P.Sexe = sexe

    P.Traitement.append(traitement)
    P.SituationFamiliale.append(situationfam)
    P.DureeDepuisDernierVoyage.append(dureederniervoyage)
    P.DureeDepuisApparitionDesSymptomes.append(dureedepuisappsymp)
    if (onto.search(iri="*" + daira) == []):
        class_daira = list_class[0]
        D = class_daira()
        D.iri = ns + daira
        P.estLocalise.append(D)
    else:
        P.estLocalise.append(onto.search(iri="*" + daira)[0])

    if (onto.search(iri="*" + wilaya) == []):
        class_wilaya = list_class[12]
        D = class_wilaya()
        D.iri = ns + wilaya
        P.estLocalise.append(D)
    else:
        P.estLocalise.append(onto.search(iri="*" + daira)[0])

    list_maladiechronique = maladiechronique.split(',')
    for j in list_maladiechronique:
        if (onto.search(iri="*" + maladiechronique) == []):
            class_mch = list_class[0]
            M = class_mch()
            M.iri = ns + maladiechronique
            M.estMaladeDe.append(D)
        else:
            P.estMaladeDe.append(onto.search(iri="*" + daira)[0])

    list_symptomes = symptomes.split(',')
    for j in list_symptomes:
        if (onto.search(iri="*" + j) == []):
            class_symp = list_class[0]
            S = class_symp()
            S.iri = ns + j
            P.aSymptomes.append(S)
        else:
            P.aSymptomes.append(onto.search(iri="*" + j)[0])

def create_medecin(nom , prenom , age , sexe):
    class_medecin = list_class[5]
    M = class_medecin()
    M.Nom = nom
    M.Prenom.append(prenom)
    M.Age = age
    M.Sexe = sexe


def fromcsvtordf(path):
    patients = pd.read_csv(path)
    for i in range(len(patients)):
        patient = patients.iloc[i]
        create_patient(patient[0], patient[1], int(patient[2]), patient[3], patient[4], patient[5], patient[6],int(patient[7]), int(patient[8]), patient[9], patient[10], patient[11])


def enrichissementwilaya(path):
    wilayas = pd.read_csv(path)
    for i in range(len(wilayas)):
        class_wilaya = list_class[13]
        W = class_wilaya()
        nom_wilaya =  wilayas.iloc[i]['nom'].replace(" ","_")
        W.iri = ns + "wilaya" + str(wilayas.iloc[i]['code'])
        W.nomWilaya = nom_wilaya
        code_wilaya = wilayas.iloc[i]['code']
        W.idWilaya = str(code_wilaya)

def enrichissementdaira(path):
    dairas = pd.read_csv(path)
    for i in range(len(dairas)):
        class_daira = list_class[0]
        D = class_daira()
        #Le if suivant est pour reglé le probleme des communes dont l'id commence par un 0
        if len(str(dairas.iloc[i]['code_postal'])) == 4:
            D.iri = ns + "0"+ str(dairas.iloc[i]['code_postal'])
        else:
            D.iri = ns +   str(dairas.iloc[i]['code_postal'])
        #print(D.iri)
        D.nomDaira = dairas.iloc[i]['nom'].replace(" ","_")
        D.communeDe.append(onto.search(iri ="*"+str(dairas.iloc[i]['wilaya_id']))[0])

def enrichissementmaladies(path):
    maladies = pd.read_csv(path)
    for i in range(len(maladies)):
        class_MaladieChronique = list_class[7]
        M= class_MaladieChronique
        nom_maladies =maladies.iloc[i].replace(" ","_")
        M.iri = ns + "maladie" + str(maladies.iloc[i])
        M.nommaladie = nom_maladies

def enrichissementsymptomes(path):
    symptomes = pd.read_csv(path)
    for i in range(len(symptomes)):
        class_Symptomes = list_class[0]
        S= class_Symptomes
        nom_symptomes =symptomes.iloc[i].replace(" ","_")
        S.iri = ns + "symptome" + str(symptomes.iloc[i])
        S.nomsymptomes = nom_symptomes









onto = get_ontology("F:\Raouf\Licence\L3\Web sémantique\Projet\sortie.owl").load()
ns = "http://sararaouf.org/onto.owl#"

list_class = enum_class(onto)

#fromcsvtordf("./test.csv")
enrichissementwilaya("wilaya.csv")
enrichissementdaira("communes.csv")
enrichissementmaladies("maladie_chronique.csv")
enrichissementsymptomes("sym.csv")




#wilayas = pd.read_csv("wilaya.csv")
#for i in range(len(wilayas)):
#    print(wilayas.iloc[i]['nom'].replace(" ","_"))



#for i in onto.data_properties():
   #pass
 # print(i)
#
##create_patient("Cherif","Lena","21","Femme","","","Compliqué","15","25","BirKhadem",["Fievre","Toux"])
##create_patient("Djouadi","Mohamed","61","Homme","","","Marié","5","250","Adrar",["Fievre","Toux","Maux_de_tetes"])
#
#
#
#for i in onto.individuals():
#    pass
#    #print(i.iri)
#
#
#

onto.save("sortiefinal.owl", format="ntriples")





