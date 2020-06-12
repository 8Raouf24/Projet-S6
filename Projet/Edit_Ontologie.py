from owlready2 import *



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
    P.MaladieChronique.append(maladiechronique)
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




onto = get_ontology("F:\Raouf\Licence\L3\Web sémantique\Projet\sortie.owl").load()
ns = "http://sararaouf.org/onto.owl#"

list_class = enum_class(onto)
#
#for i in onto.data_properties():
#    pass
#    #print(i)
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
##onto.save("sortiefinal.owl", format="ntriples")






