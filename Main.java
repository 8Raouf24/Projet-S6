package DOM;


import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.File;
import java.io.IOException;
import java.util.Scanner;

import org.w3c.dom.*;
import org.xml.sax.EntityResolver;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;



public class Main
{


    //Fonction pour le parcous recursive ainsi que pour le traitement
    public static void Exploreur(String path) throws Exception{

        File currDir = new File(path);
        String[] List =currDir.list();
        Transformer tr = TransformerFactory.newInstance().newTransformer();

        //contient le nom du fichier ou du repertoire dans la boucle
        String mini_rep ;

        for (int i = 0 ; i<List.length;i++){
            mini_rep = path + File.separator+List[i];
            File mini_file = new File(mini_rep);

            String nomFichier = String.valueOf(mini_file);
            System.out.println(nomFichier);

            //vérification si repertoire , appel reccursif
            if (mini_file.isDirectory()){
                System.out.println(mini_rep);
                Exploreur(mini_rep);

            }
            else //switch (String.valueOf(mini_file))
            {


                if(nomFichier.endsWith("M457.xml"))//case "./projet/M457.xml":
                {
                    Sortie(mini_file, "sortie2.xml", tr);
                    System.out.println("fichier M457 fini");
                }

                if(nomFichier.endsWith("M674.xml"))//case "./projet/M674.xml":
                {
                    Sortie(mini_file, "sortie1.xml", tr);
                    System.out.println("fichier M674 fini");
                }
                if(nomFichier.endsWith("poeme.txt"))
                {
                    Poeme(tr,mini_file);
                }




            }

        }
    }

    public static void Sortie(File input, String output, Transformer tr) throws Exception{
        //Fonction pour gérer les deux fichiers M674 et M457

        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        //Pour regler le probleme de la DTD inexistante
        factory.setFeature("http://apache.org/xml/features/nonvalidating/load-dtd-grammar", false);
        factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);

        DocumentBuilder builder = factory.newDocumentBuilder();

        //Fichier d'entrée , parseur
        Document inputDoc = builder.parse(input);
        //Fichier de sortie
        Document outputDoc = builder.newDocument();


        //on extrait la balise racine pour extraire ses éléments
        Element root = inputDoc.getDocumentElement();

        //On crée la balise racine de notre fichier de sortie
        Element rootOutput = outputDoc.createElement("TEI_S");
        outputDoc.appendChild(rootOutput);

        //On crée la balise qui a le nom de notre fichier d'entrée
        Element nomFile = outputDoc.createElement(input.getName());
        rootOutput.appendChild(nomFile);



        // On récupere le contenu de la balise p
        NodeList childs = root.getElementsByTagName("p");
        for (int i =0;i<childs.getLength();i++) {
            NodeList sousnodes = childs.item(i).getChildNodes();

            for (int j = 0; j < sousnodes.getLength(); j++) {
                if (sousnodes.item(j).getNodeName() == "#text" && sousnodes.item(j).getNodeValue().replace("\n", "").trim().length() > 0) {
                    Element texte = outputDoc.createElement("texte");
                    //System.out.println(sousnodes.item(j).getNodeValue().replace("\n", ""))
                    texte.appendChild(outputDoc.createTextNode(sousnodes.item(j).getNodeValue().replace("\n", "")));
                    nomFile.appendChild(texte);
                }
            }
        }
            //Pour écrire dans notre fichier de sortie sortie.xml
            DOMSource source = new DOMSource(outputDoc);
            StreamResult sortie = new StreamResult(new File(output));

            tr.setOutputProperty(OutputKeys.INDENT,"yes");
            tr.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
            tr.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, "dom.dtd");
            outputDoc.setXmlStandalone(true);
            tr.transform(source,sortie);
    }

    public static void Poeme(Transformer tr, File mini_file) throws Exception
    {
        //Fonction pour gérer le fichier poeme

        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        //Pour regler le probleme de la DTD inexistante
        factory.setFeature("http://apache.org/xml/features/nonvalidating/load-dtd-grammar", true);
        factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", true);

        DOMImplementation domimp = factory.newDocumentBuilder().getDOMImplementation();

        Document Output = domimp.createDocument(null, null, null);

        Element rootOutput = Output.createElement("poema");
        Output.appendChild(rootOutput);

        Scanner scan = new Scanner(mini_file);

        Element titre = Output.createElement("titulo");
        titre.appendChild(Output.createTextNode(scan.nextLine()));
        rootOutput.appendChild(titre);

        Element strophe = Output.createElement("estrofa");


        while(scan.hasNextLine()){
            String s = scan.nextLine();
            if (!(s.trim().length() > 0)){
                if (strophe.getChildNodes().getLength() > 0){
                    rootOutput.appendChild(strophe);
                }
                strophe = Output.createElement("estrofa");
            } else {
                Element verso = Output.createElement("verso");
                verso.appendChild(Output.createTextNode(s));
                strophe.appendChild(verso);
            }
        }
        DOMSource source = new DOMSource(Output);
        StreamResult sortie = new StreamResult(new File("neruda.xml"));
        Output.setXmlStandalone(true);

        tr.setOutputProperty(OutputKeys.INDENT,"yes");
        tr.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
        tr.setOutputProperty(OutputKeys.DOCTYPE_SYSTEM, "neruda.dtd");
        Output.setXmlStandalone(true);
        tr.transform(source,sortie);

        System.out.println("poeme fini");






    }


    public static void main(String[] argv)throws IOException, Exception {
        if (argv.length !=0)
            try {
                String dir = argv[0];
                Exploreur(dir);

            }
            catch (Exception e)
            {
                System.out.println("ERROR : le répertoire spécifié n'existe pas");
            }
        else {
            System.out.println("Attention , veuillez spécifiez le chemin du répertoire a traiter");
        }

    }


}