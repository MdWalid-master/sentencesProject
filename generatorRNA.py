
import re
import pandas as pd


#trasformation de la table associative sous forme d'un dictionnaire {'POS': [liste de mots]}
dicTableAssociative = {}
with open("data/TableAssociative.txt", "r", encoding="utf-8") as f:
    for line in f.readlines():
        lineContent = list(filter(('').__ne__,re.split("\t|\n",line)))
        dicTableAssociative[lineContent[0]] = lineContent[1:]


# trasformation de la table associative sous forme d'un dataFrame qui sera stocké sous forme d'un fichier CSV
dataframe = pd.concat({k: pd.Series(v) for k, v in dicTableAssociative.items()}, axis=1)
dataframe.to_csv("data/TableAssociativeDict.csv", sep='\t', encoding='utf-8', index=False)



