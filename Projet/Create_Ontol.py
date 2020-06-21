from owlready2 import *

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
        range = [str]
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


    class Daira(Wilaya):
        pass

    class nomDaira(DataProperty,FunctionalProperty):
        domain = [Daira]
        range = [str]


    class communeDe(Daira >> Wilaya):
        pass

    #class wilayaDe()

    class estLocalise(Humain >> Localisation):
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


    class PCDomicile(Orientation):
        pass


    class Fiche(Thing):
        pass


    class patientConcerne(Fiche >> Patient):
        pass


    class medecinConcerne(Fiche >> Medecin):
        pass


    class DateFiche(Fiche >> datetime.date):
        pass


    class typeOrientation(Fiche >> Orientation):
        pass



onto.save("sortie.owl", format="ntriples")
