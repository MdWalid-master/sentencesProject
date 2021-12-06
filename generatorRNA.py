
import re


#trasformation de la table associative sous forme d'un dictionnaire {'POS': [liste de mots]}
dicTableAssociative = {}
with open("data/TableAssociative.txt", "r", encoding="utf-8") as f:
    for line in f.readlines():
        lineContent = list(filter(('').__ne__,re.split("\t|\n",line)))
        dicTableAssociative[lineContent[0]] = lineContent[1:]

with open("data/TableAssociativeDict.txt", "w", encoding="utf-8") as f:
    f.write(str(dicTableAssociative))