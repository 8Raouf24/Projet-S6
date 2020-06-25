from owlready2 import *
import rdflib
import pandas as pd

#On inovque cette fonction afin de pouvoir ordonner les classes de notre ontologie dans une liste afin de pouvoir instancier les classes directement
def ordonner_classe(ontol):
    d = {}
    for i in ontol.classes():
        d[i.name] = i
    d = sorted(d.items(), key=lambda x: x[0])

    L = []
    for i in range(len(d)):
        L.append(d[i][1])
    return L

#Fonction pour pouvoir énumerer les classes de notre ontologie et nous les afficher
def enum_class(onto):
    liste = ordonner_classe(onto)
    cpt = 0
    for i in liste:
        print(cpt, '-', str(i).split('.')[-1])
        cpt += 1
    return liste

#Cette fonction nous permet de créer un patient dans notre ontologie
def create_patient(ID,nom, prenom, age, sexe, maladiechronique, traitement, situationfam, dureederniervoyage,dureedepuisappsymp, daira, wilaya, symptomes):
    #On recupere la classe "Patient" de notre liste
    class_patient = list_class[9]
    #On instancie un objet de la classe
    P = class_patient()
    #On remplace l'iri donné par owlready par notre propre iri
    P.iri = ns+"patient"+ str(ID)

    #A partir de la on va instancier les valeurs des attributs de notre objet patient
    P.patientID = str(ID)
    P.Nom = nom
    P.Prenom.append(prenom)
    P.Age = age
    P.Sexe = sexe

    P.Traitement.append(traitement)
    P.SituationFamiliale.append(situationfam)
    P.DureeDepuisDernierVoyage.append(dureederniervoyage)
    P.DureeDepuisApparitionDesSymptomes.append(dureedepuisappsymp)


    #On utilise une requete sparql afin de trouver la daira et wilaya de notre patient et lié notre patient a eux via une relation "estLocalise"
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
        print(i)
        P.estLocalise.append(onto.search(iri=i[0])[0])

    #Au lieu d'utiliser une requete sparql , on utilise la fonction search de owlready afin de pouvoir trouver les maladies chroniques de patient existante dans notre base rdf pour les lier , et si il n'existe pas on le crée puis on les lie
    list_maladiechronique = maladiechronique.split(',')
    for j in list_maladiechronique:
        if (onto.search(iri="*" + maladiechronique) == []):
            class_mch = list_class[5]
            M = class_mch()
            M.iri = ns + j.replace(" ", "_")
            P.estMaladeDe.append(M)
        else:
            P.estMaladeDe.append(onto.search(iri="*" + j)[0])

    #Meme procede que les maladies chroniques pour les symptomes
    list_symptomes = symptomes.split(',')
    for j in list_symptomes:
        if (onto.search(iri="*" + j) == []):
            class_symp = list_class[11]
            S = class_symp()
            S.iri = ns + j.replace(" ", "_")

            P.aSymptomes.append(S)
        else:
            P.aSymptomes.append(onto.search(iri="*" + j)[0])

#Cette fonction quant a elle nous permets de créer un objet medecin dans notre base rdf
def create_medecin(ID,nom, prenom, sexe):
    class_medecin = list_class[6]
    M = class_medecin()
    M.iri = ns +"medecin"+ str(ID)
    M.medecinID = ID
    M.Nom = nom
    M.Prenom.append(prenom)
    M.Sexe = sexe

#Cette fonction nous permets de traduire un fichier csv et l'inserer dans notre base rdf
def fromcsvtordf(path):
    patients = pd.read_csv(path)
    for i in range(len(patients)):
        patient = patients.iloc[i]
        create_patient(patient[0], patient[1], patient[2], int(patient[3]), patient[4], patient[5], patient[6],
                       patient[7], int(patient[8]), int(patient[9]), patient[10], patient[11],patient[12])

#Cette fonction nous a permit d'enrichir notre base rdf en insérant les wilayas quand on  a pu trouvé dans un fichier csv qu'un saint samaritain nous a donné
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

#Meme chose pour les dairas , sauf qu'en plus de ca , on lie les Dairas a leur Wilayas respectives
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
        D.communeDe.append(onto.search(iri="*" +"wilaya"+ str(dairas.iloc[i]['wilaya_id']))[0])

#Cette fonction nous permets de relié l'orientation donné par un medecin sur un patient donné
def orientation(type_orientation,IDmedecin,IDpatient):
    patient = onto.search(iri=ns + "patient" + str(IDpatient))[0]
    medecin = onto.search(iri=ns + "medecin" + str(IDmedecin))[0]

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


#Cette fonction nous permets de créer une fiche pour un patient en recoltant ses informations via une requete sparql
def créationfiche(IDpatient):
    list_info = []
    list_symp = []
    list_malad = []
    list_med = []
    requete = """
    prefix ns1: <http://sararaouf.org/onto.owl#>
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix xml: <http://www.w3.org/XML/1998/namespace>
    prefix xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT  ?id ?nom  ?age ?sexe ?dureevoyage ?dureesymp ?prenom  ?traitement ?situationfam  ?ndaira  ?nwilaya ?s ?maladiechronique ?orientation ?idmed ?nommed
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
    ?p ns1:estConcernéParOrientation ?orientation .
    ?m ns1:prescritOrientation ?orientation .
    ?m ns1:medecinID ?idmed .
    ?m ns1:Nom ?nommed .
    FILTER regex(?id , "^var")
    }
     """.replace("var", IDpatient)
    result = graph.query(requete)

    #Ici on receuille les infos fixes du patient ( pourquoi fixe ?car un patient peut avoir plusieurs symptomes / maladie chronique et donc le résultat de  la requete sparql sera sur plusieurs lignes)
    for i in range(11):
        list_info.append( list(result)[0][i])

    #Donc on utilise cette fonction pour receuillir les maladies chroniques
    for i in result:
        if str(i[12]).split('#')[1] not in list_malad:
            list_malad.append(str(i[12]).split('#')[1])

    #Et celle la pour les symptomes
    for i in result:
        if str(i[11]).split('#')[1] not in list_malad:
            list_symp.append(str(i[11]).split('#')[1])

    for i in range(13,16):
        list_med.append(list(result)[0][i])








onto = get_ontology("F:\Raouf\Licence\L3\Web sémantique\Projet\sortiefinal.owl").load()
ns = "http://sararaouf.org/onto.owl#"

#pour ce qui est de rdf
graph = rdflib.Graph()
graph.parse("sortiefinal.owl", format="turtle")
open("sortielib.rdf","w")
graph.serialize("sortielib.rdf",format="turtle")

list_class = enum_class(onto)


#enrichissementwilaya("wilaya.csv")
#enrichissementdaira("communes.csv")
#fromcsvtordf("./test.csv")
#
#
#
#create_medecin('0002',"Bakir","Djamal","Homme")
#orientation("Prise en charge a domicile","0002",1)
créationfiche("1")

#pour invoquer le raisonneur



owlready2.JAVA_EXE = "C:\\Program Files (x86)\\Common Files\\Oracle\\Java\\javapath\\java.exe"
#sync_reasoner()

onto.save("sortiefinal.owl", format="ntriples")


# onto.save("sortierdf.rdf",format="ntriples")
