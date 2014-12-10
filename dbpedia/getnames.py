#!/usr/bin/env python

from SPARQLWrapper import SPARQLWrapper, JSON
import sys


def query_dbpedia(query):
    """Makes SPARQL query against dbpedia."""
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        return results['results']['bindings']
    except ValueError:
        return None


def get_count(ont_class):
    """Returns count of 'ont_class' names from dbpedia."""
    results = query_dbpedia("""
        SELECT COUNT(?n) AS ?c WHERE {
            ?p a <http://dbpedia.org/ontology/""" + ont_class + """> .
            ?p foaf:name ?n .
        }
    """)
    return int(results[0]['c']['value'])


def dump(ont_class, limit=1000, offset=0):
    """Dumps 'limit' names of 'ont_class' objects from 'offset'."""
    results = query_dbpedia("""
        SELECT ?n, ?s WHERE {
            ?p a <http://dbpedia.org/ontology/""" + ont_class + """> .
            ?p prov:wasDerivedFrom ?s .
            ?p foaf:name ?n .
        } LIMIT """ + str(limit) + ' OFFSET ' + str(offset)
    )
    if results:
        res = set()
        for result in results:
            tmp = result['n']['value'].split(',')
            out = tmp[0].strip()
            if len(tmp) > 1:
                out = tmp[1][1:].strip() + ' ' + tmp[0].strip()
            out += '\t' + result['s']['value']
            res.add(out.replace('"', ''))
        for result in sorted(res):
            print(result.encode('utf-8'))
    else:
        sys.stderr.write('Error in offset: ' + str(offset) + '\n')


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        sys.stderr.write(arg + ': ' + str(get_count(arg)) + '\n')
        for offset in range(0, get_count(arg), 10000):
            if offset % 100000 == 0:
                sys.stderr.write('Offset: ' + str(offset) + '\n')
            dump(arg, 10000, offset)

# vi:set et sts=4 sw=4 ts=4:
