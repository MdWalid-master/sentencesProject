import re
from os import listdir
from os.path import isfile, join
from os import walk
import re
from itertools import groupby
import json
from nltk import ngrams


def generate_model(liste_fichiers):
    bigramme_model = {}
    treegramme_model = {}

    def create_file_model(model, num):
        with open("model_" + num + "_gramme.txt", "w", encoding="utf-8") as f:
            for key, val in model.items():
                f.write(str(key) + ":" + str(val) + "\n")

    for path in liste_fichiers:
        with open(path, "r", encoding="utf-8") as f:
            s = "".join(
                list(filter(('').__ne__, re.findall(r"[^\d]", "".join(f.readlines())))))

            s = " ".join(
                list(filter(('').__ne__, re.findall(r"\w+’*,{0,1}\?*\.{0,1}\w*|\n", s))))

            def createModel(n_gramme, model):
                for i, j in groupby(sorted(n_gramme)):
                    gramms = " ".join(i)
                    if "\n" not in gramms:
                        if i not in model:
                            model[gramms] = len(list(j))
                        else:
                            model[gramms] += len(list(j))
                return dict(sorted(model.items(), key=lambda t: t[1], reverse=True))

            bigramme_model = createModel(ngrams(re.split(' ', s), 2), bigramme_model)
            treegramme_model = createModel(ngrams(re.split(' ', s), 3), treegramme_model)

    create_file_model(bigramme_model, "bi")
    create_file_model(treegramme_model, 'tree')


def generate_sentence():
    def get_model(fic):
        with open("model_" + fic + "_gramme.txt", "r", encoding="utf-8") as f:
            return f.readlines()

    def get_sentence_bigrams(model, mot, taille):
        sentence = ""
        for _ in range(0, taille):
            for words in model:
                w = re.split(" |:", words)

                if (len(re.findall((w[0] + " " + w[1]), sentence)) <= 1) and mot == w[0]:
                    sentence += mot + " "
                    mot = w[1]
                    break
        return sentence

    def get_sentence_treegrams(model, mot, taille):
        sentence= ""
        for _ in range(0, taille//2):
            for words in model:
                w = re.split(" |:", words)
                if (len(re.findall((w[0] + " " + w[1] + " " + w[2]), sentence)) <= 1) and mot == w[0]:
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
        print(get_sentence_bigrams(get_model("bi"), "de", i))

    # ------------- trigrams ----------------
    print("--------------- Pour treegrams ----------------------")
    for i in [5, 10, 15]:
        print(get_sentence_treegrams(get_model("tree"), "de", i))


if __name__ == '__main__':
    dic_path_fichiers = []

    for (repertoire, sousRepertoires, fichiers) in walk("MEGALITE_FR"):
        dic_path_fichiers.append({repertoire: fichiers})

    dic_path_fichiers = dic_path_fichiers[1:]

    path_fic = []
    for paths in dic_path_fichiers:
        for repertoire in paths:
            path_fic.extend([repertoire + "\\" + fic for fic in paths[repertoire][:2]])

    # generate_model(path_fic)
    generate_sentence()
