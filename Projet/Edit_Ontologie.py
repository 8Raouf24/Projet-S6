from owlready2 import *
import rdflib
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
        print(cpt, '-', str(i).split('.')[-1])
        cpt += 1
    return liste


def create_patient(ID,nom, prenom, age, sexe, maladiechronique, traitement, situationfam, dureederniervoyage,dureedepuisappsymp, daira, wilaya, symptomes):
    class_patient = list_class[9]
    P = class_patient()
    P.iri = ns+ str(ID)
    P.patientID = str(ID)
    P.Nom = nom
    P.Prenom.append(prenom)
    P.Age = age
    P.Sexe = sexe

    P.Traitement.append(traitement)
    P.SituationFamiliale.append(situationfam)
    P.DureeDepuisDernierVoyage.append(dureederniervoyage)
    P.DureeDepuisApparitionDesSymptomes.append(dureedepuisappsymp)



    requete = """
    prefix ns1: <http://sararaouf.org/onto.owl#> 
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    prefix xml: <http://www.w3.org/XML/1998/namespace> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
    SELECT     ?d ?w
    WHERE{
    ?d rdf:type ns1:Daira .
    ?d ns1:nomDaira ?nd .
    ?w rdf:type ns1:Wilaya .
    ?w ns1:nomWilaya ?wn .
    ?d ns1:communeDe ?w . 
    FILTER regex(?nd,"var1")  
    FILTER regex(?wn,"var2")
    }
    """.replace("var1", daira).replace("var2",wilaya)
    result = graph.query(requete)
    for i in result:
        P.estLocalise.append(onto.search(iri=i[0])[0])


    list_maladiechronique = maladiechronique.split(',')
    for j in list_maladiechronique:
        if (onto.search(iri="*" + maladiechronique) == []):
            class_mch = list_class[5]
            M = class_mch()
            M.iri = ns + j.replace(" ", "_")
            P.estMaladeDe.append(M)
        else:
            P.estMaladeDe.append(onto.search(iri="*" + j)[0])

    list_symptomes = symptomes.split(',')
    for j in list_symptomes:
        if (onto.search(iri="*" + j) == []):
            class_symp = list_class[11]
            S = class_symp()
            S.iri = ns + j.replace(" ", "_")

            P.aSymptomes.append(S)
        else:
            P.aSymptomes.append(onto.search(iri="*" + j)[0])


def create_medecin(ID,nom, prenom, age, sexe, spécialité):
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
        create_patient(patient[0], patient[1], patient[2], int(patient[3]), patient[4], patient[5], patient[6],
                       patient[7], int(patient[8]), int(patient[9]), patient[10], patient[11],patient[12])


def enrichissementwilaya(path):
    wilayas = pd.read_csv(path)
    for i in range(len(wilayas)):
        class_wilaya = list_class[13]
        W = class_wilaya()
        nom_wilaya = wilayas.iloc[i]['nom'].replace(" ", "_")
        W.iri = ns + "wilaya" + str(wilayas.iloc[i]['code'])
        W.nomWilaya = nom_wilaya
        code_wilaya = wilayas.iloc[i]['code']
        W.idWilaya = str(code_wilaya)


def enrichissementdaira(path):
    dairas = pd.read_csv(path)
    for i in range(len(dairas)):
        class_daira = list_class[0]
        D = class_daira()
        # Le if suivant est pour reglé le probleme des communes dont l'id commence par un 0
        if len(str(dairas.iloc[i]['code_postal'])) == 4:
            D.iri = ns + "0" + str(dairas.iloc[i]['code_postal'])
        else:
            D.iri = ns + str(dairas.iloc[i]['code_postal'])
        # print(D.iri)
        D.nomDaira = dairas.iloc[i]['nom'].replace(" ", "_")
        D.communeDe.append(onto.search(iri="*" + str(dairas.iloc[i]['wilaya_id']))[0])

def orientation(type_orientation,IDmedecin,IDpatient):
    patient = onto.search(iri=ns + IDpatient)[0]
    medecin = onto.search(iri=ns + IDmedecin)[0]

    if type_orientation == "Prise en charge a domicile":
        class_pec = list_class[8]
        pec = class_pec()
        patient.estConcernéParOrientation.append(pec)
        medecin.prescritOrientation.append(pec)

    if type_orientation == "Redirection vers hopital":
        class_hop = list_class[2]
        hop = class_hop()
        patient.estConcernéParOrientation.append(hop)
        medecin.prescritOrientation.append(hop)

    if type_orientation == "Prise de rendez-vous":
        class_rdv = list_class[10]
        rdv = class_rdv()
        patient.estConcernéParOrientation.append(rdv)
        medecin.prescritOrientation.append(rdv)


def créationfiche(IDpatient):
    requete = """
    prefix ns1: <http://sararaouf.org/onto.owl#>
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix xml: <http://www.w3.org/XML/1998/namespace>
    prefix xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT ?p  ?nom ?id ?age ?sexe ?dureevoyage ?dureesymp ?prenom ?maladiechronique ?traitement ?situationfam ?s ?ndaira  ?nwilaya
    WHERE{
    ?p rdf:type ns1:Patient .
    ?p ns1:patientID ?id .
    ?p ns1:Nom ?nom .
    ?p ns1:Age ?age .
    ?p ns1:Sexe ?sexe .
    ?p ns1:DureeDepuisDernierVoyage ?dureevoyage .
    ?p ns1:DureeDepuisApparitionDesSymptomes ?dureesymp .
    ?p ns1:Prenom ?prenom .
    ?p ns1:estMaladeDe ?maladiechronique .
    ?p ns1:Traitement ?traitement .
    ?p ns1:SituationFamiliale ?situationfam .
    ?p ns1:aSymptomes ?s .
    ?p ns1:estLocalise ?daira .
    ?daira ns1:communeDe ?wilaya .
    ?daira ns1:nomDaira ?ndaira .
    ?wilaya ns1:nomWilaya ?nwilaya .
    FILTER regex(?id , "^var")
    }
     """.replace("var", IDpatient)
    print(requete)
    result = graph.query(requete)
    for i in result:
        print(i)



    pass


owlready2.JAVA_EXE = "C:\\Program Files (x86)\\Common Files\\Oracle\\Java\\javapath\\java.exe"

onto = get_ontology("F:\Raouf\Licence\L3\Web sémantique\Projet\sortiefinal.owl").load()
ns = "http://sararaouf.org/onto.owl#"


graph = rdflib.Graph()
graph.parse("sortiefinal.owl", format="turtle")
#open("sortielib.rdf","w")
#graph.serialize("sortielib.rdf",format="turtle")




list_class = enum_class(onto)

#requete = """
# prefix ns1: <http://sararaouf.org/onto.owl#>
# prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# prefix xml: <http://www.w3.org/XML/1998/namespace>
# prefix xsd: <http://www.w3.org/2001/XMLSchema#>
# SELECT     ?p  ?nom ?prenom ?daira ?wilaya ?sexe ?age ?maladiechronique
# WHERE{
# ?p rdf:type ns1:Patient .
#
# }
# """
#result = graph.query(requete)
#for i in result:
#   print(i)
#   for j in i:
#       print(i)

#enrichissementdaira("communes.csv")
#enrichissementwilaya("wilaya.csv")
#fromcsvtordf("./test.csv")







onto.save("sortiefinal.owl", format="ntriples")


# onto.save("sortierdf.rdf",format="ntriples")
