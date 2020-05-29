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

def create_patient(nom , prenom , age , sexe , maladiechronique , traitement , situationfam , dureederniervoyage, dureedepuisappsymp ,localisation , symptomes):
    class_patient = list_class[8]
    P = class_patient()
    P.Nom = nom
    P.Prenom = prenom
    P.Age = age
    P.Sexe = sexe
    P.MaladieChronique.append(maladiechronique)
    P.traitement.append(traitement)
    P.SituationFamiliale.append(situationfam)
    P.DureeDepuisDernierVoyage.append(dureederniervoyage)
    P.DureeDepuisApparitionDesSymptomes.append(dureedepuisappsymp)

    #Localisation



onto = get_ontology("F:\Raouf\Licence\L3\Web sémantique\Projet\sortie.owl").load()

list_class = enum_class(onto)

for i in onto.data_properties():
    print(i)

class_patient = list_class[8]
P = class_patient()
P.Nom = "Chiboub"
P.Prenom.append("Raouf")
P.Age = "20"

P = class_patient()
P.Nom = "Lasnami"
P.Prenom.append("Sara")
P.Age = "21"

class_

for i in onto.individuals():
    print(i)

list_test = onto.search(iri = "*Chiboub")
print(list_test)

onto.save("sortie2.owl", format="ntriples")






