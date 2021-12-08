import operator
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
table_associative = function_get_table_associative_csv()
embbeding = function_get_embbeding()

col = table_associative[(table_associative[words[0]] != query) & (table_associative[words[1]] != query)]
col = col[words]

# col = table_associative[[words]]
# col = col.drop(col.index[col[words[0]] == query], inplace = True)
# col = col.drop(col.index[col[words[1]] == query], inplace = True)
# col = col.reset_index()
# col = col[col[words[0]] != query]
# col = col[col[words[1]] != query]

query_data = embbeding[[query]]

#print(col)

best_word = {}
for c in col[words[0]].dropna() :
    if c in embbeding.columns :
        word_vector =  embbeding[[c]]
        val_cosine = 1 - cosine(word_vector,query_data)
        best_word[c] = val_cosine


word_optimal = max(best_word.items(), key=operator.itemgetter(1))
best_word.clear()
print("Best word for "+words[0]+" is "+str(word_optimal))

for c in col[words[1]].dropna() :
    if c in embbeding.columns :
        word_vector =  embbeding[[c]]
        val_cosine = 1 - cosine(word_vector,query_data)
        best_word[c] = val_cosine


word_optimal = max(best_word.items(), key=operator.itemgetter(1))
best_word.clear()
print("Best word for "+words[1]+" is "+str(word_optimal))


