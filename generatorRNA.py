import operator
import re
import pandas as pd
from operator import itemgetter
from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean, pdist, squareform

"""
    1- Récuprer convenablement les templates 
    2- Intégrer les modèles 
    3- Replacer convenablement les mots dans leurs phrases adéqute
"""


# trasformation de la table associative sous forme d'un dictionnaire {'POS': [liste de mots]}
def function_get_table_associative():
    dicTableAssociative = {}
    with open("data/TableAssociative.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            lineContent = list(filter(('').__ne__, re.split("\t|\n", line)))
            dicTableAssociative[lineContent[0]] = lineContent[1:]

    # trasformation de la table associative sous forme d'un dataFrame qui sera stocké sous forme d'un fichier CSV
    dataframe = pd.concat({k: pd.Series(v) for k, v in dicTableAssociative.items()}, axis=1)

    # dataframe.to_csv("data/TableAssociativeDict.csv", sep='\t', encoding='utf-8', index=False)
    return dataframe


# Récupérer les embbeding sous forme d'un datafram
def function_get_embbeding():
    dic_embedding = {}
    with open("data/embeddings-Fr.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            words = list(filter(('').__ne__, re.split(" |,|\[|\]|\t|\n", line)))
            dic_embedding[words[0]] = words[1:]

    data_embedding = pd.DataFrame(dic_embedding).astype('float64')
    # data_embedding.to_csv("data/embeddingsDict.csv", sep='\t', encoding='utf-8', index=False)

    return data_embedding


# Décomposer les mots eloigner
def get_words_templates():
    with open("data/templates_basiques_2.txt", "r", encoding="utf-8") as f:
        templates = []
        for line in f.readlines():
            pos = []
            for sentence in re.findall(r'\*\w+/*\w*', line):
                words = re.findall(r"\w+", sentence)
                pos.append((words[0], words[1]))

            templates.append(pos)

        return templates


def set_replace_pos_in_template(optimal, templates):
    with open("data/templates_basiques_2.txt", "r", encoding="utf-8") as f:
        text = "".join(re.split(r"/\w*", "".join(f.readlines())))
        for i in range(0, len(optimal)):
            for j in range(0, len(optimal[i])):
                text = text.replace("*" + templates[i][j][0], "(" + optimal[i][j] + ")")

        text = text.replace("\n", "\t" + query + "\n")
        print(text)

        with open("data/Resultat.txt", "w", encoding="utf-8") as f:
            f.write(text)
        f.close()


def get_best_words(query, table_associative, embbeding, templates):
    optimal_template_word = []

    for template in templates:      # Pour chaque phrase du template
        query_data = embbeding[query]   # Récupérer le vecteur de la query
        words_optimal = []

        for pos in template:
            tag_words = table_associative[pos[0]].dropna()  # Récupérer les mots du tags dans la table associative
            word_max_distance = pos[1]  # S'éloigner de ce mot
            best_word = {}              # Dictionnaire contenant
            dic = {}

            for word in tag_words:  # Pour chaque mot
                # Si le mot est un vecteur dans embedding et les mots max aussi

                if word in embbeding.columns and word_max_distance in embbeding.columns \
                        and word != word_max_distance and word != query and word not in words_optimal:

                    min_val = euclidean(embbeding[word], query_data)  # Calculer la distance par rapport au query
                    max_val = euclidean(embbeding[word], embbeding[word_max_distance])

                    if min_val < max_val:
                        best_word[word] = max_val - min_val

                    # if max_val < min_val:
                    #     best_word[word] = min_val

            # -------------------------- Refaire cette partie ---------------------------- for for
            if len(words_optimal) != 0:
                for optimal_word in words_optimal:
                    for word_key in best_word.items():
                        if word_key[0] in dic:
                            dic[word_key[0]] += euclidean(embbeding[word_key[0]], embbeding[optimal_word])
                        else:
                            dic[word_key[0]] = euclidean(embbeding[word_key[0]], embbeding[optimal_word])
                if dic:
                    words_optimal.append(min(dic.items(), key=operator.itemgetter(1))[0])
            else:
                if best_word:
                    words_optimal.append(max(best_word.items(), key=operator.itemgetter(1))[0])

        optimal_template_word.append(words_optimal)

    return optimal_template_word


def with_model():
    pass


if __name__ == '__main__':
    query = 'tristesse'

    # Récupérer les pos de chaque phrase du template sous form [[('tag' : mot),('tag' : mot)],[]
    templates = get_words_templates()
    embbeding = function_get_embbeding()  # Récupérer les vecteurs de mots dans embedding

    if query not in embbeding.columns:
        raise Exception("La query n'existe pas !")

    table_associative = function_get_table_associative()  # Récupérer la table associative

    print("words templates : ", templates)

    optimal = get_best_words(query=query, embbeding=embbeding,
                             table_associative=table_associative, templates=templates)

    print(optimal)
    set_replace_pos_in_template(optimal=optimal, templates=templates, query=query)
