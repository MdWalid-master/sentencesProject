import operator
import re
import pandas as pd
from operator import itemgetter
from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean


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


def function_get_embbeding():
    dic_embedding = {}
    with open("data/embeddings-Fr.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            words = list(filter(('').__ne__, re.split(" |,|\[|\]|\t|\n", line)))
            dic_embedding[words[0]] = words[1:]

    data_embedding = pd.DataFrame(dic_embedding).astype('float64')
    # data_embedding.to_csv("data/embeddingsDict.csv", sep='\t', encoding='utf-8', index=False)

    return data_embedding


def get_words_templates():
    with open("data/templates_basiques.txt", "r", encoding="utf-8") as f:
        templates = []
        for line in f.readlines():
            pos = []
            for sentence in re.findall(r'\*\w+/*\w*', line):
                words = re.findall(r"\w+", sentence)
                pos.append((words[0], words[1]))

            templates.append(pos)

        return templates


def set_replace_pos_in_template(optimal, templates):
    with open("data/templates_basiques.txt", "r", encoding="utf-8") as f:
        text = "".join(re.split(r"/\w*", "".join(f.readlines())))
        for i in range(0, len(optimal)):
            for j in range(0, len(optimal[i])):
                text = text.replace("*" + templates[i][j][0], "(" + optimal[i][j][0] + ")")

        print(text)


def get_best_words(query, table_associative, embbeding, templates):
    optimal_template_word = []
    for template in templates:  # Pour chaque phrase du template
        query_data = embbeding[query]  # Récupérer le vecteur de la query
        words_optimal = []
        print("template")
        for pos in template:
            tag_words = table_associative[pos[0]].dropna()  # Récupérer les mots du tags dans la table associative
            word_max_distance = pos[1]  # S'éloigner de ce mot
            best_word = {}  # Dictionnaire contenant

            for word in tag_words:  # Pour chaque mot
                # Si le mot est un vecteur dans embedding et les mots max aussi
                if word in embbeding.columns and word_max_distance in embbeding.columns \
                        and word != word_max_distance and word != query:

                    """
                        - cosine : Consinus
                            * Produit des mots incohérents pour tristesse
                            * Produit des mots cohérents pour fidelité
                            * 1 - cosine pour la similarité
                            * cosine pour la distance

                        - euclidean : Distance euclidienne
                            * Produit des mots cohérent
                    """

                    min_val_cosine = euclidean(embbeding[word], query_data)  # Calculer la distance par rapport au query
                    max_val_cosine = euclidean(embbeding[word], embbeding[word_max_distance])

                    # -------------------------- Refaire cette partie ----------------------------
                    for last_optimal_word in words_optimal:
                        min_val_cosine = abs(min_val_cosine - euclidean(embbeding[word], embbeding[last_optimal_word]))

                    best_word[word] = max_val_cosine - min_val_cosine
                    # -----------------------------------------------------------------------------

            words_optimal.append(max(best_word.items(), key=operator.itemgetter(1))[0])

        optimal_template_word.append(words_optimal)

    return optimal_template_word


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
    # set_replace_pos_in_template(optimal=optimal, templates=templates)
