import pprint

import pandas as pd
import pymongo
import json
import os


def import_csvfile(filepath1, filepath2,db_cm):
    cdir = os.path.dirname(__file__)
    file_res1 = os.path.join(cdir, filepath1)
    file_res2 = os.path.join(cdir, filepath2)
    data1 = pd.read_csv(file_res1)
    data2 = pd.read_csv(file_res2)
    data_json1 = json.loads(data1.to_json(orient='records'))
    data_json2 = json.loads(data2.to_json(orient='records'))
    db_cm.remove()
    db_cm.insert(data_json1)
    db_cm.insert(data_json2)


def nameSearch(name,db_cm):
    a = db_cm.find({"Proteinnames": {"$regex": ".*" + name + ".*"}},
                   {"_id": 0, "Entryname": 1, "Proteinnames": 1, "Organism": 1, "Genenames": 1, "Geneontology": 1,
                    "ECnumber": 1})
    # t=tuple()
    entries = []
    protNames = []
    organisms = []
    gene_names = []
    gene_ontology = []
    labeled = []
    for i in a:
        entries.append(i["Entryname"])
        protNames.append(i["Proteinnames"])
        organisms.append(i["Organism"])
        gene_names.append(i["Genenames"])
        gene_ontology.append(i["Geneontology"])
        if i["Geneontology"] is None and i["ECnumber"] is None:
            labeled.append("Unlabeled")
        else:
            labeled.append("Labeled")
    t = (entries, protNames, organisms, gene_names, gene_ontology, labeled)
    return t


def entrySearch(entry,db_cm):
    a = db_cm.find({"Entryname": entry},
                   {"_id": 0, "Entryname": 1, "Proteinnames": 1, "Organism": 1, "Genenames": 1, "Geneontology": 1,
                    "ECnumber": 1})
    # t = tuple()
    entries = []
    protNames = []
    organisms = []
    gene_names = []
    gene_ontology = []
    labeled = []
    for i in a:
        entries.append(i["Entryname"])
        protNames.append(i["Proteinnames"])
        organisms.append(i["Organism"])
        gene_names.append(i["Genenames"])
        gene_ontology.append(i["Geneontology"])
        if i["Geneontology"] is None and i["ECnumber"] is None:
            labeled.append("Unlabeled")
        else:
            labeled.append("Labeled")
    t = (entries, protNames, organisms, gene_names, gene_ontology, labeled)
    return t


def labelStat(db_cm):
    unlabeled = db_cm.find({'$and': [{'ECnumber': None}, {'Geneontology': None}]}).count()
    total = db_cm.find().count()
    labeled = total - unlabeled
    return [labeled, unlabeled, total]






"""
  db.list_collection_names()
  Protein = db.Protein
  pprint.pprint(Protein.find_one())
  
"""

"""
print(collection_name.list_collection_names())
collist = collection_name.list_collection_names()
if "Proteins" in collist:
    print("The collection exists.")

dblist = myclient.list_database_names()
if "mydatabase" in dblist:
    print("The database exists.")
    """
