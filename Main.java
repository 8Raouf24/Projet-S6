package DOM;


import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;

import org.w3c.dom.*;




public class Main {
    private static Document outputDoc;

    //Fonction pour le parcous recursive ainsi que pour le traitement
    public static void Exploreur(String path) throws Exception {

        File currDir = new File(path);
        String[] List = currDir.list();
        Transformer tr = TransformerFactory.newInstance().newTransformer();

        //contient le nom du fichier ou du repertoire dans la boucle
        String mini_rep;

        for (String s : List) {
            mini_rep = path + File.separator + s;
            File mini_file = new File(mini_rep);

            String nomFichier = String.valueOf(mini_file);
            System.out.println(nomFichier);

            //vérification si repertoire , appel reccursif
            if (mini_file.isDirectory()) {
                System.out.println(mini_rep);
                Exploreur(mini_rep);

            } else //switch (String.valueOf(mini_file))
            {


                if (nomFichier.endsWith("M457.xml"))//case "./projet/M457.xml":
                {
                    Sortie(mini_file, "sortie2.xml", tr);
                    System.out.println("fichier M457 fini");
                }

                if (nomFichier.endsWith("M674.xml"))//case "./projet/M674.xml":
                {
                    Sortie(mini_file, "sortie1.xml", tr);
                    System.out.println("fichier M674 fini");
                }
                if (nomFichier.endsWith("poeme.txt")) {
                    Poeme(tr, mini_file);
                }
                if (nomFichier.endsWith("boitedialog.fxml")) {
                    FXML(tr, mini_file);
                    System.out.println("fxml fini");
                }
                if (nomFichier.endsWith("fiches.txt")) {
                    Fiche(mini_file,tr);
                    System.out.println("fiches finis");
                }
                if (nomFichier.endsWith("renault.html")) {
                    Renault(mini_file,tr);

                    System.out.println("renault fini");
                }


            }

        }
    }

    public static void Fiche(File input, Transformer tr) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();

        Document doc1  = builder.getDOMImplementation().createDocument(null, "FICHES", null);
        Document doc2  = builder.getDOMImplementation().createDocument(null, "FICHES", null);



        tr.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");

        BufferedReader inputDoc = new BufferedReader(new InputStreamReader(new FileInputStream(String.valueOf(input))));
        String ligne = inputDoc.readLine();

        Node root1 = doc1.getDocumentElement();
        Node root2 = doc2.getDocumentElement();

        doc1.setXmlStandalone(true);
        doc2.setXmlStandalone(true);

        Element langue1 = null;
        Element langue2 = null;

        Element Fiche1 = null;
        Element Fiche2 = null;
        ArrayList<Node> Noeuds = new ArrayList<>();
        boolean contient_RF = false;
        int cpt = 0;
        do {
            if (ligne.endsWith("BE")) {
                Noeuds.clear();
                Fiche1 = doc1.createElement("FICHE");
                Fiche2 = doc2.createElement("FICHE");

                Fiche1.setAttribute("id", ++cpt + "");
                Fiche2.setAttribute("id", cpt + "");

                Node n1 = doc1.createElement("BE");
                Node n2 = doc2.createElement("BE");

                Node txt1 = doc1.createTextNode(ligne.replace("BE", ""));
                Node txt2 = doc2.createTextNode(ligne.replace("BE", ""));

                n1.appendChild(txt1);
                n2.appendChild(txt2);

                Fiche1.appendChild(n1);
                Fiche2.appendChild(n2);

                root1.appendChild(Fiche1);
                root2.appendChild(Fiche2);

                langue1 = null;
                langue2 = null;
            } else if (ligne.startsWith("AR") || ligne.startsWith("FR")) {
                langue1 = doc1.createElement("Langue");
                langue2 = doc2.createElement("Langue");

                langue1.setAttribute("id", ligne.substring(0, 2));
                langue2.setAttribute("id", ligne.substring(0, 2));

                for(int n=0;n<Noeuds.size();n++) {
                    Node item=doc1.createElement(Noeuds.get(n).getNodeName());
                    Node txt=doc1.createTextNode(Noeuds.get(n).getChildNodes().item(0).getNodeValue());
                    item.appendChild(txt);

                    langue1.appendChild(item);
                    //System.out.println("#"+n.getTextContent());
                }

                Fiche1.appendChild(langue1);
                Fiche2.appendChild(langue2);

                contient_RF = false;
            } else if (langue1 == null || langue2 == null) {
                String Nom_B = ligne.substring(ligne.length() - 2);

                Node n1 = doc1.createElement(Nom_B);
                Node n2 = doc2.createElement(Nom_B);

                Node txt1 = doc1.createTextNode(ligne.substring(ligne.length() - 2) + " : " + ligne.substring(0, ligne.length() - 2));
                Node txt2 = doc2.createTextNode(ligne.substring(ligne.length() - 2) + " : " + ligne.substring(0, ligne.length() - 2));

                n1.appendChild(txt1);
                n2.appendChild(txt2);


                Fiche2.appendChild(n2);

                if (Nom_B.equals("TY") || Nom_B.equals("AU"))
                    Fiche1.appendChild(n1);
                else
                    Noeuds.add(n1);
            } else if (!ligne.matches("\\s*")) {
                if (ligne.contains("RF :")) {
                    ligne = ligne.replace("RF :", "");
                    String prefix = "", prefix_sub;
                    while (ligne.lastIndexOf(':') > 0 && ligne.substring(ligne.lastIndexOf(':') + 1).matches("\\s*")) {
                        prefix_sub = ligne.substring(ligne.lastIndexOf(':') - 3, ligne.lastIndexOf(':') + 1);
                        prefix += prefix_sub + " ";
                        ligne = ligne.replace(prefix_sub, "");
                    }
                    Node n1 = doc1.createElement("RF");
                    Node n2 = doc2.createElement("RF");


                    Node txt1 = doc1.createTextNode("RF | " + prefix + ligne);
                    Node txt2 = doc2.createTextNode("RF | " + prefix + ligne);

                    n1.appendChild(txt1);
                    n2.appendChild(txt2);

                    langue1.appendChild(n1);
                    langue2.appendChild(n2);

                    contient_RF = true;
                } else {
                    String prefix = "", prefix_sub;
                    while (ligne.lastIndexOf(':') > 0 && ligne.substring(ligne.lastIndexOf(':') + 1).matches("[\\s]*")) {
                        prefix_sub = ligne.substring(ligne.lastIndexOf(':') - 3, ligne.lastIndexOf(':') + 1);
                        prefix += prefix_sub + " ";
                        ligne = ligne.replace(prefix_sub, "");
                    }
                    if (contient_RF) {
                        Node n1 = doc1.createElement("RF");
                        Node n2 = doc2.createElement("RF");

                        Node txt1 = doc1.createTextNode("RF | " + prefix + ligne);
                        Node txt2 = doc2.createTextNode("RF | " + prefix + ligne);

                        n1.appendChild(txt1);
                        n2.appendChild(txt2);

                        langue1.appendChild(n1);
                        langue2.appendChild(n2);
                    } else {
                        Node n1 = doc1.createElement(prefix.substring(0, 2));
                        Node n2 = doc2.createElement(prefix.substring(0, 2));

                        Node txt1 = doc1.createTextNode(prefix + ligne);
                        Node txt2 = doc2.createTextNode(prefix + ligne);

                        n1.appendChild(txt1);
                        n2.appendChild(txt2);

                        langue1.appendChild(n1);
                        langue2.appendChild(n2);
                    }
                }
            }
            ligne = inputDoc.readLine();
        } while (ligne != null);
        inputDoc.close();
        DOMSource source1 = new DOMSource(doc1);
        DOMSource source2 = new DOMSource(doc2);

        StreamResult sortie1 = new StreamResult(new File("fiches1.xml"));
        StreamResult sortie2 = new StreamResult(new File("fiches2.xml"));

        tr.setOutputProperty(OutputKeys.VERSION, "1.0");
        tr.setOutputProperty(OutputKeys.INDENT,"yes");
        tr.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
        tr.setOutputProperty(OutputKeys.DOCTYPE_PUBLIC,"");


        tr.transform(source1,sortie1);
        tr.transform(source2,sortie2);




    }
    public static void Renault (File input,Transformer tr)throws Exception{
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setFeature("http://apache.org/xml/features/nonvalidating/load-dtd-grammar", false);
        factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document inputDoc = builder.parse(input);
        DOMImplementation domimp = builder.getDOMImplementation();
        Document outputDoc = domimp.createDocument(null, null, null);
        outputDoc.setXmlStandalone(true);

        Element root = inputDoc.getDocumentElement();
        Element rootOutput = outputDoc.createElement("Concessionnaires");

        Element body = (Element) root.getElementsByTagName("body").item(0);
        NodeList divs = body.getElementsByTagName("div");

        Element div = (Element) body.getElementsByTagName("p").item(0);

        for (int i = 0; i < divs.getLength(); i++){
            Element d = (Element) divs.item(i);
            if (d.getAttribute("class").equals("post-single"))
                div = d;
        }

        NodeList ps = div.getElementsByTagName("p");
        for (int i = 1; i < ps.getLength(); i++){
            String s = getStr(ps.item(i)).replaceAll("\n", " ");
            String name = s.split("Adresse :")[0], r1 = s.split("Adresse :")[1];
            String addr = r1.split("Tél :")[0], r2 = r1.split("Tél :")[1];
            String tel = "";
            if (r2.indexOf("Fax :") == -1) tel = r2;
            else {
                tel = r2.split("Fax :")[0];
            }
            Element nameEl = outputDoc.createElement("Nom");
            nameEl.appendChild(outputDoc.createTextNode(name.trim()));
            Element addrEl = outputDoc.createElement("Adresse");
            addrEl.appendChild(outputDoc.createTextNode(addr.trim()));
            Element telEl = outputDoc.createElement("Num_téléphone");
            telEl.appendChild(outputDoc.createTextNode(tel.trim()));

            rootOutput.appendChild(nameEl);
            rootOutput.appendChild(addrEl);
            rootOutput.appendChild(telEl);
        }

        outputDoc.appendChild(rootOutput);


        DOMSource source = new DOMSource(outputDoc);
        StreamResult sortie = new StreamResult(new File("renault.xml"));

        tr.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
        tr.setOutputProperty(OutputKeys.DOCTYPE_PUBLIC,"");
        tr.setOutputProperty(OutputKeys.INDENT, "yes");
        tr.transform(source, sortie);
    }

    public static String getStr(Node node){
        String s = "";
        return recGetText(node, s);
    }
    public static String recGetText(Node node, String s){
        NodeList nodeList = node.getChildNodes();

        for (int i = 0; i < nodeList.getLength(); i++){
            Node currentNode = nodeList.item(i);
            if (currentNode.getNodeName().equals("#text")) s = s + currentNode.getNodeValue().trim() + " ";
            if (currentNode.getNodeName().charAt(0) != '#'){
                s = recGetText(currentNode, s);
            }
        }

        return s;
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
                if (sousnodes.item(j).getNodeName().equals("#text") && sousnodes.item(j).getNodeValue().replace("\n", "").trim().length() > 0) {
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
        tr.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
        Output.setXmlStandalone(true);
        tr.transform(source,sortie);

        System.out.println("poeme fini");
    }

    public static void FXML(Transformer tr,File mini_file) throws Exception{
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document inputDoc = builder.parse(mini_file);
        DOMImplementation domimp = builder.getDOMImplementation();
        Document outputDoc = domimp.createDocument(null, null, null);
        outputDoc.setXmlStandalone(true);

        //Fichier d'entrée , parseur

        //Fichier de sortie


        Element rootOutput = outputDoc.createElement("Racine");


        outputDoc.appendChild(rootOutput);

        rootOutput.setAttribute("xmlns:fx","http://javafx.com/fxml");


        Recursivite_FXML(inputDoc.getDocumentElement(),outputDoc);




        DOMSource source = new DOMSource(outputDoc);
        StreamResult sortie = new StreamResult(new File("javafx.xml"));


        tr.setOutputProperty(OutputKeys.INDENT,"yes");
        tr.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
        tr.setOutputProperty(OutputKeys.VERSION, "1.0");
        tr.setOutputProperty(OutputKeys.DOCTYPE_PUBLIC,"");

        tr.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");

        tr.transform(source,sortie);




    }

    //Fonction récurssive pour parcourir les elements ayant des attributs du fichiel fxml
    private static void Recursivite_FXML(Node node, Document outputDoc) {
        if(node.hasAttributes()) {
            NamedNodeMap nom = node.getAttributes();

            int alength=nom.getLength();
            for(int i=0;i<alength;i++) {
                Attr attr=(Attr) nom.item(i);

                Element element = outputDoc.createElement("texte");

                element.setAttribute(attr.getName(), "x");

                Node txt=outputDoc.createTextNode(attr.getValue());
                element.appendChild(txt);

                outputDoc.getDocumentElement().appendChild(element);
            }
        }

        NodeList nl=node.getChildNodes();
        int length=nl.getLength();
        for(int i=0;i<length;i++)
            Recursivite_FXML(nl.item(i),outputDoc);
    }


    public static void main(String[] argv)throws Exception {
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
