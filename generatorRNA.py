import re
import pandas as pd
import numpy as np


def function_get_embbeding():
    dic_embedding = {}
    with open("data/embeddings-Fr.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            l = re.findall("-*\w+\.*\d*e*-*\+*\d*", line)
            dic_embedding[l[0]] = l[1:]

    data_embedding = pd.DataFrame(dic_embedding).astype('float64')
    data_embedding.to_csv("data/embeddingsDict.csv", sep='\t', encoding='utf-8', index=False)

    return data_embedding
