#projet web sem

entete= [u'nom', u'commune',u'wilaya', u'symptomes', u'maladie', u'traitement', u'age', u'sexe']
#valeurs=[[u'zoubida',u'hydra', u'alger', u'fatigue, maux de tete', u'diabete', u'insuline', u'20', u'femme'], [u'ahmed',u'ain turk',u'oran',u' toux seche, maux de tete',u' Hypertension', u'propanolol',u' 49',u' homme'],[u'mourad',u'ben aknoun',u'alger',u' vomissements, courbatures',u' asthme', u'ventoline',u'26 ',u' homme'],[u'sofiane' ,u'chrea',u'blida',u'ecoulement nazale, fatigue',u' cancer des poumons', u'chimiotherapie',u' 49',u' homme'],[u'lynda' ,u'bab ezzouar',u'alger',u'frissons, nausées',u' colon', u'debridat',u' 22',u' femme'],[u'adel' ,u'treat',u'annaba',u' diharée',u' anemie', u'fer',u' 34',u' homme'],[u'houda' ,u'toudja',u'bejaia',u' fievre, maux de gorge',u' alergie', u'corticoides',u' 25',u' femme'],[u'samy' ,u'el khroub',u'constanrine',u' vomissements',u' aucune', u'aucu,',u' 9',u' homme'],[u'yasmine' ,u'azzefoun',u'tizi ouzou',u' fievre, ecoulement nazal',u' autisme', u'aucun',u' 15',u' femme'],[u'fatiha' ,u'hacine',u'mascara',u' fievre',u' cancer du sein', u'chimiotherapie',u' 42',u' femme'], [u'aghiles' ,u'tigzirt',u'tizi ouzou',u' vomissements',u' otite', u'amoxicilline',u' 31',u' homme'],[u'hamza' ,u'draria',u'alger',u' toux seche',u'vitiligo ', u'puvathérapie',u' 22',u' homme'], [u'khadidja' ,u'adrar',u'adrar',u' palpitations',u' aucune', u'aucun',u' 60',u' femme'],[u'mohamed' ,u'zenata',u'tlemecen',u' paleur,vertige',u'diabete ', u'insuline',u' 24',u' homme'], [u'amel' ,u'cherchel',u'tipaza',u' nodule',u' aucune', u'aucun',u' 18',u' femme'],[u'mohamed' ,u'zenata',u'tlemecen',u' paleur,vertige',u'diabete ', u'insuline',u' 22',u' homme'], [u'boualem' ,u'djanet',u'illizi',u' toux seche',u' insuffisance renale', u'kayexalate',u' 75',u' homme'], [u'yacine' ,u'sedrata',u'souk ahras',u' Gynécomastie',u' cancer de la prostate', u'chimiotherapie',u' 56',u' homme'],[u'ghania' ,u'staoueli',u'alger',u' fatigue, maux de tete',u' cholesterol', u'lescol',u' 47',u' femme'], [u'djamel' ,u'hanif',u'bouira',u' Tuméfaction',u' aucune', u'aucun',u' 38',u' homme'],[u'sara',u'ben aknoun', u'alger', u'rage de dents', u'anxiete', u'veratran', u'28', u'femme']]
f= open('fichier_patients.csv', 'w')
ligneEntete = ";".join(entete) + "\n"
f.write(ligneEntete)
for valeur in valeurs:
     ligne = ";".join(valeur) + "\n"
     f.write(ligne)

f.close()

a= [u'nom', u'commune',u'wilaya', u'specialite']
#b=[[u'Dr mesbah',u'draria',u'alger',u'cardiologue'],[u'Dr bourahla',u'chrea',u'blida',u'genraliste'],[u'Dr boukhari',u'draria',u'alger',u'generaliste'],[u'Dr arrouf',u'hanif',u'bouira',u'rhumathologue'],[u'Dr nessah',u'azzefoun',u'tizi ouzou',u'generaliste'],[u'Dr nasri',u'cherchel',u'tipaza',u'dermatologue'],[u'Dr sekkal',u'ben aknoun',u'alger',u'dentiste'],[u'Dr ammour',u'adrar',u'adrar',u'cardiologue'],[u'Dr miramar',u'el khroub',u'constantine',u'infectiologue'],[u'Dr berrak',u'hacine',u'mascara',u'generaliste'],[u'Dr cherif',u'toudja',u'bejaia',u'infectiologue'],[u'Dr ait yahia',u'zenata',u'tlemcen',u'cancerologue'],[u'Dr slimani',u'djanet',u'illizi',u'generaliste'],[u'Dr said',u'sedrata',u'souk ahras',u'endocrinologue'],[u'Dr said',u'ain turk',u'oran',u'infectiologue'],[u'Dr ramdani',u'treat',u'annaba',u'infectiologue'],[u'Dr kellal',u'bab ezzouar',u'alger',u'infectiologue'],[u'Dr chettouh',u'kaous',u'jijel',u'neurologue']]
f= open('fichier_medecins.csv', 'w')
ligneEntete = ";".join(a) + "\n"
f.write(ligneEntete)
for valeur in b:
     ligne = ";".join(valeur) + "\n"
     f.write(ligne)
     
     
f.close()