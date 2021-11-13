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
            s = ''.join(re.findall(r'[^\d]*', "".join(f.readlines()).lower()))  # Suppression des numéros
            s = ' '.join(list(filter(('').__ne__, re.findall(r'\w*', s))))  # nous supprimons les caractères spéciaux

            def createModel(n_gramme, model):
                for i, j in groupby(sorted(n_gramme)):
                    if i not in model:
                        model[" ".join(i)] = len(list(j))
                    else:
                        model[" ".join(i)] += len(list(j))
                return dict(sorted(model.items(), key=lambda t: t[1], reverse=True))

            bigramme_model = createModel(ngrams(s.split(), 2), bigramme_model)
            treegramme_model = createModel(ngrams(s.split(), 3), treegramme_model)

    create_file_model(bigramme_model, "bi")
    create_file_model(treegramme_model, 'tree')


def generate_sentence():
    def get_model(fic):
        with open("model_" + fic + "_gramme.txt", "r", encoding="utf-8") as f:
            return f.readlines()

    def get_sentence(model, mot):
        sentence = ""
        for i in range(0, 5):
            for words in model:
                w = re.split(" |:", words)
                if mot == w[0]:
                    sentence += mot + " "
                    mot = w[1]
                    break
        return sentence

    print(get_sentence(get_model("bi"), "f"))
    print(get_sentence(get_model("tree"), "f"))


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
