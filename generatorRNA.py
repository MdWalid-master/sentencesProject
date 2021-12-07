import re
import pandas as pd
from scipy.spatial.distance import cosine


# trasformation de la table associative sous forme d'un dictionnaire {'POS': [liste de mots]}
def function_get_table_associative_csv():
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
            l = list(filter(('').__ne__, re.split(" |,|\[|\]|\t|\n", line)))
            dic_embedding[l[0]] = l[1:]

    data_embedding = pd.DataFrame(dic_embedding).astype('float64')
    # data_embedding.to_csv("data/embeddingsDict.csv", sep='\t', encoding='utf-8', index=False)

    return data_embedding


def get_words_templates():
    with open("data/templates_basiques", "r", encoding="utf-8") as f:
        for line in f.readlines():
            return re.findall(r"\w+", "".join(re.findall(r'\*\w+/', line)))


query = 'tristesse'
words = get_words_templates()
# table_associative = function_get_table_associative_csv()
embbeding = function_get_embbeding()

# col = table_associative[words[0]].dropna()
# print(col)

col = embbeding[['impatience', 'tristesses', 'tristesse']]
print(cosine(col[["tristesse", "impatience"]],col["tristesse"])),

