from flask import Flask, render_template,request,redirect
from edit_ontol import *

app = Flask(__name__)

onto = get_ontology("F:\Raouf\Licence\L3\Web sémantique\Projet\sortiefinal.owl").load()
ns = "http://sararaouf.org/onto.owl#"
dict_fiches=[]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consultation',methods =['GET','POST'])
def consultationform():
    if request.method =='POST':
        print(request.form['prenom'])
        create_patient(request.form['nom'],request.form['prenom'],int(request.form['age']),float(request.form['poids']),float(request.form['taille']),request.form['sexe'],request.form['maladies'],request.form['traitement'],request.form['situationfam'],int(request.form['dureevoyage']),int(request.form['dureesymp']),request.form['daira'],request.form['wilaya'],request.form['symptomes'])
        return redirect('/')
    else:
        return render_template('Inscription.html')

@app.route('/consultationsara',methods =['GET','POST'])
def consultationformsara():
    if request.method =='POST':
        print(request.form['prenom'])
        print(request.form['nom'])
        print(request.form['sexe'])
        print(request.form['age'])
        print(request.form['situation_familiale'])
        return redirect('/')
    else:
        return render_template('consultation.html')  


@app.route('/med')
def med():
    return render_template('med.html')


if __name__ == "__main__":
    app.run(debug=True)

 


