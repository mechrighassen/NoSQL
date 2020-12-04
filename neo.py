import pandas as pd
import numpy as np
import csv
from neo4j import GraphDatabase


def strToListInt(s):
  if s==-1 :
    return [-1]
  return [int(x) for x in s[:-1].replace('IPR','').split(';')]


def adaptCsv(csvFile):
    data = pd.read_csv(csvFile)
    data['Crossreference'] = data['Crossreference'].fillna(value=-1)
    data['Crossreference'] = data['Crossreference'].map(strToListInt)
    data.to_csv('dataUnreviewedNeo.csv', index=False, quoting=csv.QUOTE_NONE, escapechar='\\', sep='%')

#adaptCsv('Ressources_unreviewed.csv')

def createGraph():
    graphdb = GraphDatabase.driver(uri='bolt://localhost:7687', auth=("neo4j", "test"))
    session = graphdb.session()
    import_data = 'LOAD CSV WITH HEADERS FROM \"file:///dataUnreviewedNeo.csv\" as l FIELDTERMINATOR \'%' \
                  '\' CREATE (prot:Prot{entryName:l.Entryname, entry:l.Entry,  status:l.Status, ' \
                   'proteinNames:l.Proteinnames, geneNames:l.Genenames, organism:l.Organism, length:toInteger(l.Length), ' \
                  'ecNumber:l.ECnumber, geneotology:l.Geneontology, crossreference:l.Crossreference}); '
    session.run(import_data)

#createGraph()

def createRelationships():
    graphdb = GraphDatabase.driver(uri='bolt://localhost:7687', auth=("neo4j", "test"))
    session = graphdb.session()
    request='match (m1:Prot) match (m2:Prot) where algo.similarity.jaccard(apoc.convert.fromJsonList(m1.crossreference), apoc.convert.fromJsonList(m2.crossreference))>0.6 and m1.entryName>m2.entryName and apoc.convert.fromJsonList(m1.crossreference)<>[-1] and apoc.convert.fromJsonList(m2.crossreference)<>[-1] create (m1)-[p:Sim]->(m2)  set p.sim=algo.similarity.jaccard(apoc.convert.fromJsonList(m1.crossreference), apoc.convert.fromJsonList(m2.crossreference))'
    session.run(request)

#createRelationships()

def getNodeByEntryName0(entry):
    graphdb = GraphDatabase.driver(uri='bolt://localhost:7687', auth=("neo4j", "test"))
    session = graphdb.session()
    nodes = session.run('MATCH (m:Prot)-[:Sim]-(n:Prot) where m.entry=\"' + entry + '\" return m, n')
    results=[]
    for node in nodes:
        results.append([(node[0]['entry'],node[0]['entryName']),(node[1]['entry'],node[1]['entryName']),('','')])
    return results
#getNodeByEntryName0('AROC_SULIN')


def getNodeByEntryName1(proteinNames):
    graphdb = GraphDatabase.driver(uri='bolt://localhost:7687', auth=("neo4j", "test"))
    session = graphdb.session()
    nodes = session.run('MATCH (m1:Prot)-[:Sim]-(m2:Prot)-[:Sim]-(m3:Prot) where m1.proteinNames=\"' + proteinNames + '\" return m1, m2, m3')
    results=[]
    for node in nodes:
        results.append([
            (node[0]['entry'], node[0]['entryName']), (node[1]['entry'], node[1]['entryName']), (node[2]['entry'],
                       node[2]['entryName'])])
    return results

#getNodeByEntryName1('CAP8_ADEB2')


def getNodeByEntry0(entry):
    graphdb = GraphDatabase.driver(uri='bolt://localhost:7687', auth=("neo4j", "test"))
    session = graphdb.session()
    nodes = session.run('MATCH (m:Prot)-[:Sim]-(n:Prot) where m.entry=\"' + entry + '\" return m, n')
    results = []
    for node in nodes:
        results.append([(node[0]['entry'], node[0]['entryName']), (node[1]['entry'], node[1]['entryName']),('','')])
    return results

#getNodeByEntry0('O50304')


def getNodeByEntry1(proteinNames):
    graphdb = GraphDatabase.driver(uri='bolt://localhost:7687', auth=("neo4j", "test"))
    session = graphdb.session()
    nodes = session.run('MATCH (m1:Prot)-[:Sim]-(m2:Prot)-[:Sim]-(m3:Prot) where m1.proteinNames=\"' + proteinNames + '\" return m1, m2, m3')
    results = []
    for node in nodes:
        results.append([
            (node[0]['entry'], node[0]['entryName']), (node[1]['entry'], node[1]['entryName']), (node[2]['entry'],
                                                                                                 node[2]['entryName'])])
    return results
#getNodeByEntry1('O50304')


def getIsolatedNodes():
    graphdb = GraphDatabase.driver(uri='bolt://localhost:7687', auth=("neo4j", "test"))
    session = graphdb.session()
    nodes=session.run('MATCH (m:Prot) where not (m:Prot)-[:Sim]-() return m')
    results = []
    for node in nodes:
        results.append([(node[0]['entry'], node[0]['entryName']), ('',''), ('', '')])
    return results

#getIsolatedNodes()

def getIsolatedNodesCount():
    graphdb = GraphDatabase.driver(uri='bolt://localhost:7687', auth=("neo4j", "test"))
    session = graphdb.session()
    nodes = session.run('MATCH (m:Prot) where not (m:Prot)-[:Sim]-() return count(m)')
    results = []
    for node in nodes:
        results.append([(node[0]['entry'], node[0]['entryName']), ('', ''), ('', '')])
    return results

def getNeighbors(entryName):
    graphdb = GraphDatabase.driver(uri='bolt://localhost:7687', auth=("neo4j", "test"))
    session = graphdb.session()
    nodes = session.run('MATCH (m:Prot)-[r:Sim]-(n:Prot) where m.entryName=\"' + entryName + '\" return m, n')
    results = []
    for node in nodes:
        results.append(node[1]['entryName'])
    return results

def label(entryName):
    sim = 0
    typ = ''
    result = ''
    graphdb = GraphDatabase.driver(uri='bolt://localhost:7687', auth=("neo4j", "test"))
    session = graphdb.session()
    nodes = session.run('MATCH (m:Prot)where m.entryName=\"' + entryName + '\" return m')
    results = []
    for node in nodes:
        #print(node[0]['ecNumber'],node[0]['geneontology'],node[0]['entryName'])
        if(node[0]['ecNumber']!=None):
            typ='ecNumber :'
            result=node[0]['ecNumber']
            return typ+result
        if (node[0]['geneotology'] != None):
            typ = 'geneotology :'
            result = node[0]['geneotology']
            return typ + result

    graphdb = GraphDatabase.driver(uri='bolt://localhost:7687', auth=("neo4j", "test"))
    session = graphdb.session()
    nodes = session.run('MATCH (m:Prot)-[r:Sim]-(n:Prot) where m.entryName=\"' + entryName + '\" return m, n, r')
    for node in nodes:
        results.append(node[1]['entryName'])
       #print(results)
        if(node[2]['sim']>sim and (node[1]['geneotology'] != None  or node[1]['ecNumber'] != None)):
            sim=node[2]['sim']
            if(node[1]['geneotology'] != None):
                typ = 'geneotology :'
                result = node[1]['geneotology']
            if (node[1]['ecNumber'] != None):
                typ = 'ecNumber :'
                result = node[1]['ecNumber']
    if(typ=='' and result==''):
        return 'there is no label for this node'
    else:
        return typ+result





