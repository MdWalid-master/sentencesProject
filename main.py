import re
from os import listdir
from os.path import isfile, join
from os import walk
import re
from itertools import groupby
import json
from nltk import ngrams


def generate_model(liste_fichiers):
    # Les modèles sont des dictionnaire où chaque clé et le n_gramme et valeur le nombre d'occurence de ce dernier 
    bigramme_model = {}
    treegramme_model = {}

    def create_file_model(model, num):
        """
        - Cette méthode va permettre d'enregistrer les modèles dans leur fichier correspodant
        - model_bi_gramme.txt   : ML-2
        - model_tree_gramme.txt : ML-3
        """

        with open("model_" + num + "_gramme.txt", "w", encoding="utf-8") as f:
            for key, val in model.items():
                f.write(str(key) + ":" + str(val) + "\n")

    # Pour chaque fichier 
    for path in liste_fichiers:
        with open(path, "r", encoding="utf-8") as f:
            """Récupération du contenu du fichier et supprimer les caractère numérique, un caractère suivi d'un point 
            et les mot Chapitre et les numéros latin"""
            s = "".join(
                list(filter(('').__ne__, re.split(r"\d| \w\. |Chapitre| [XVI]+ ", "".join(f.readlines())))))

            # Garder que les mot alphabétique, ', ?, ., virgule et \n
            s = " ".join(
                list(filter(('').__ne__, re.findall(r"\w+’*,{0,1}\?*\.{0,1}\w*|\n", s))))

            def createModel(n_gramme, model):
                """groupby permet de regrouper les ngramme : [(n_gramme_1, [n_gramme_1, ..., n_gramme_1]), (n_gramme_2,
                [n_gramme_2, ..., n_gramme_2]), ..]"""
                for i, j in groupby(sorted(n_gramme)):
                    gramms = " ".join(i)
                    if "\n" not in gramms:  # Ne pas garder les n_grammes contenant le \n
                        """Si le n_gramme existe dans le modèle alors incrémenter le nombre d'occurences sinon l'ajouter
                         dans le dictionnaire"""
                        if i not in model:
                            model[gramms] = len(list(j))
                        else:
                            model[gramms] += len(list(j))

                # Retourner le modèle et le trier par ordre décroissant par rapport aux occurences
                return dict(sorted(model.items(), key=lambda t: t[1], reverse=True))

            """            
            - Nous générons les n_grammes avec la bibliothèque nltk qui possède la méthode ngrams, la méthode possède
             deux argements : 
                * Une liste de mots et le n_gramme résultant : 1 pour un-gramme, 2 pour bi-gramme, etc.
            """
            bigramme_model = createModel(ngrams(re.split(' ', s), 2), bigramme_model)
            treegramme_model = createModel(ngrams(re.split(' ', s), 3), treegramme_model)

    # Création des fichiers pour chaque modèle
    create_file_model(bigramme_model, "bi")
    create_file_model(treegramme_model, 'tree')


def generate_sentence():
    # Récupération des modèle à partir de leurs fichiers correspodant
    def get_model(fic):
        with open("model_" + fic + "_gramme.txt", "r", encoding="utf-8") as f:
            return f.readlines()

    # Génération des phrases avec ML-2
    def get_sentence_bigrams(model, mot, taille):
        sentence = ""  # La phrase généré

        # Nous bouclons par rapport à la taille de la phrase que nous souhaitons généré 
        for _ in range(0, taille):
            for words in model:
                w = re.split(" |:", words)  # w : [mot_1, mot_2, :occurence]

                """                
                - La première condition permet d'éviter qu'une expression se répète indéfiniment durant la génération 
                de la phrase 
                - Cherche le premier bigramme contenant le mot pour déterminser son suivant
                """
                if (len(re.findall((w[0] + " " + w[1]), sentence)) <= 0) and mot == w[0]:
                    sentence += mot + " "
                    mot = w[1]
                    # Une fois trouvé, nous arretons la recherche du mot numéro i et nous passons au suivant
                    break
        return sentence

    # Génération des phrases avec ML-3
    def get_sentence_treegrams(model, mot, taille):
        sentence = ""
        # Nous bouclons par rapport à la taille de la phrase que nous souhaitons généré 
        for _ in range(0, taille // 2):
            for words in model:
                w = re.split(" |:", words)  # w : [mot_1, mot_2, mot_3, :occurence]

                """             
                - La première condition permet d'éviter qu'une expression se répète indéfiniment durant la génération
                de la phrase.
                - Cherche le premier trigramme contenant le mot pour récupérer les deux mots suivants
                """
                if (len(re.findall((w[0] + " " + w[1] + " " + w[2]), sentence)) <= 0) and mot == w[0]:
                    sentence += mot + " " + w[1] + " "
                    mot = w[2]
                    break
        if taille % 2 != 0:
            return sentence + mot
        else:
            return sentence

    # ------------- bigrams -----------------
    print("--------------- Pour bigrams ----------------------")
    for i in [5, 10, 15]:
        print(get_sentence_bigrams(get_model("bi"), "Histoire", i))     # <-- Écrire mot début de phrase ici (bigramme)

    # ------------- trigrams ----------------
    print("--------------- Pour trigrams ----------------------")
    for i in [5, 10, 15]:
        print(get_sentence_treegrams(get_model("tree"), "Ville", i))    # <-- Écrire mot début de phrase ici (trigramme)


if __name__ == '__main__':
    dic_path_fichiers = []

    for (repertoire, sousRepertoires, fichiers) in walk("MEGALITE_FR"):
        dic_path_fichiers.append({repertoire: fichiers})

    dic_path_fichiers = dic_path_fichiers[1:]

    path_fic = []  # Cette variable va contenir les liens vers tous les fichiers du corpus
    for paths in dic_path_fichiers:
        for repertoire in paths:
            path_fic.extend(
                [repertoire + "\\" + fic for fic in paths[repertoire][:20]])  # 20 fichiers pour chaque sous dossier

    """    
        - Pour 20 fichiers de chaque sous dossier nous avons obtenu : 
            * 4882010 de bigrammes 
            * 12699110 de trigrammes
    """

    #generate_model(path_fic)
    generate_sentence()
