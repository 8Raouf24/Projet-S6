from owlready2 import *
import rdflib


default_world.set_backend(filename="file_back3.sqlite3", exclusive=False)

onto = get_ontology("http://sararaouf.org/onto.owl")
Url = "http://sararaouf.oms/Covid_ont#"

with onto:
    # Class and Data Property
    class Humain(Thing):
        pass


    class Sexe(DataProperty, FunctionalProperty):
        range = [str]
        domain = [Humain]


    class Age(DataProperty, FunctionalProperty):
        range = [int]
        domain = [Humain]


    class Nom(DataProperty, FunctionalProperty):
        range = [str]
        domain = [Humain]


    class Prenom(DataProperty):
        range = [str]
        domain = [Humain]


    class Patient(Humain):
        pass


    class patientID(DataProperty, FunctionalProperty):  # Unicité a questionner
        range = [str]
        domain = [Patient]
        pass


    class TrancheAge(Patient >> str):
        pass


    class MaladieChronique(Thing):
        pass

    class nomMaladie(MaladieChronique >> str):
        pass

    class estMaladeDe(Patient >> MaladieChronique):
        pass




    class Traitement(Patient >> str):
        pass


    class SituationFamiliale(Patient >> str):
        pass


    class DureeDepuisDernierVoyage(Patient >> int):  # Jour
        pass


    class DureeDepuisApparitionDesSymptomes(Patient >> int):  # Jour
        pass


    class Medecin(Humain):
        pass


    class medecinID(DataProperty, FunctionalProperty):
        domain = [Medecin]
        range = [str]
        pass

    class medecinSpecialité(DataProperty, FunctionalProperty):
        domain = [Medecin]
        range = [str]
        pass

    class Spécialité(Thing):
        pass

    class Localisation(Thing):
        pass


    class Wilaya(Localisation):
        pass


    class nomWilaya(DataProperty,FunctionalProperty):
        domain = [Wilaya]
        range = [str]

    class idWilaya(DataProperty,FunctionalProperty):
        domain = [Wilaya]
        range = [str]
        pass


    class Daira(Localisation):
        pass


    AllDisjoint([Daira, Wilaya])

    class nomDaira(DataProperty,FunctionalProperty):
        domain = [Daira]
        range = [str]


    class communeDe(Daira >> Wilaya):
        pass



    class estLocalise(Thing >> Localisation):
        pass


    class Symptomes(Thing):
        pass


    class SymptomesCovid(Symptomes):
        pass


    class aSymptomes(Patient >> Symptomes):
        pass


    class Orientation(Thing):
        pass


    class Hopital(Orientation):
        pass


    class RDV(Orientation):
        pass

    class dateRDV(RDV >> str):
        pass

    #Prise en charge
    class PCDomicile(Orientation):
        pass

    class nomOrientation(Orientation >> str):
        pass

    class Fiche(Thing):
        pass


    class patientConcerne(Fiche >> Patient):
        pass


    class medecinConcerne(Fiche >> Medecin):
        pass





    class estConcernéParOrientation(Patient >> Orientation):
        pass

    class prescritOrientation(Medecin >> Orientation):
        pass



onto.save("sortie.owl", format="ntriples")





