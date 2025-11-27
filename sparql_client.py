from SPARQLWrapper import SPARQLWrapper, JSON
from config import GRAPHDB_REPOSITORY, PREFIX

def run_sparql(query, endpoint=None):
    endpoint = endpoint or GRAPHDB_REPOSITORY
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(PREFIX + "\n" + query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
    except Exception as e:
        raise RuntimeError(f"SPARQL query failed: {e}\nQuery:\n{query}")
    return results
