import operator
import re
import pandas as pd
from operator import itemgetter
from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean, pdist, squareform


# trasformation de la table associative sous forme d'un dataframe {'POS': [liste de mots]}
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


# trasformation des embeddings sous forme d'un dataframe {'mot': [vecteur]}
def function_get_embbeding():
    dic_embedding = {}
    with open("data/embeddings-Fr.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            words = list(filter(('').__ne__, re.split(" |,|\[|\]|\t|\n", line)))
            dic_embedding[words[0]] = words[1:]

    data_embedding = pd.DataFrame(dic_embedding).astype('float64')
    # data_embedding.to_csv("data/embeddingsDict.csv", sep='\t', encoding='utf-8', index=False)

    return data_embedding


# Extraire les Theme des templates
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

# Replacer les mot génerer (TA) par la POS approprié
def set_replace_pos_in_template(optimal, templates, query):
    with open("data/templates_basiques_2.txt", "r", encoding="utf-8") as f:
        text = "".join(re.split(r"/\w*", "".join(f.readlines())))
        for i in range(0, len(optimal)):
            for j in range(0, len(optimal[i])):
                text = text.replace("*" + templates[i][j][0], "(" + optimal[i][j] + ")", 1)

        text = text.replace("\n", "\t" + query + "\n")
        print(text)

        #sauvegarde des phrases generées dans un fichier txt
        with open("data/Resultat.txt", "a", encoding="utf-8") as f:
            f.write(text)
        f.close()

# Géneration de l'ensemble des mots optimaux (TA) pour chaque phrase
def get_best_words(query, table_associative, embbeding, templates):
    optimal_template_word = [] #liste des mots optimaux

    for template in templates:      # Pour chaque phrase du template
        query_data = embbeding[query]   # Récupérer le vecteur de la query
        words_optimal = []

        for pos in template:
            tag_words = table_associative[pos[0]].dropna()  # Récupérer les mots du tags (POS) dans la table associative (dataframe)
            word_max_distance = pos[1]  # S'éloigner de ce mot (theme)
            best_word = {}
            dic = {}

            #print(word_max_distance, " et :", word_max_distance in embbeding.columns)

            for word in tag_words:  # Pour chaque mot

                # Si le mot est un vecteur dans embedding et les mots max aussi
                if word in embbeding.columns and word != word_max_distance and word not in words_optimal and word != query:

                    """ gynécologie n'est pas present dans les embedding 
                    le cas ou la query est amour ainsi que le theme en prend pas en cosideration le fait que le mot à generer il faut qu'il soit loin du theme """
                    if (word_max_distance == "gynécologie") or (word_max_distance == query):
                        best_word[word] = cosine(embbeding[word],query_data)  # Calculer la distance par rapport au query

                    elif word_max_distance in embbeding.columns :

                        min_val = cosine(embbeding[word], query_data)  # Calculer la distance par rapport au query
                        max_val = cosine(embbeding[word], embbeding[word_max_distance]) # Calculer la distance par rapport au theme

                        if min_val < max_val:
                            best_word[word] = max_val - min_val


            if len(words_optimal) != 0: #afin de calculer la distance du TA a generer avec les TA deja generer
                for optimal_word in words_optimal:
                    for word_key in best_word.items():
                        if word_key[0] in dic:
                            dic[word_key[0]] += cosine(embbeding[word_key[0]], embbeding[optimal_word])
                        else:
                            dic[word_key[0]] = cosine(embbeding[word_key[0]], embbeding[optimal_word])
                if dic:
                    words_optimal.append(min(dic.items(), key=operator.itemgetter(1))[0])
            else: #dans le cas ou c'est le premier TA a generer
                if best_word:
                    words_optimal.append(max(best_word.items(), key=operator.itemgetter(1))[0])

        optimal_template_word.append(words_optimal) #ajouter le TA generer dans la liste des mots optimaux

    return optimal_template_word



if __name__ == '__main__':
    query = ['amour','tristesse', 'joie', 'haine', 'bleu']

    # Récupérer les pos de chaque phrase du template sous form [[('tag' : mot),('tag' : mot)],[]
    templates = get_words_templates()
    embbeding = function_get_embbeding()  # Récupérer les vecteurs de mots dans embedding

    table_associative = function_get_table_associative()  # Récupérer la table associative

    #print("words templates : ", templates)
    for q in query:
        if q not in embbeding.columns:
            raise Exception("La query n'existe pas !")

        optimal = get_best_words(query=q, embbeding=embbeding,
                                 table_associative=table_associative, templates=templates)

        print(optimal)
        set_replace_pos_in_template(optimal=optimal, templates=templates, query=q)
