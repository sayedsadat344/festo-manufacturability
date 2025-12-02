from SPARQLWrapper import SPARQLWrapper, JSON, POST, POSTDIRECTLY, TURTLE
from config import GRAPHDB_REPOSITORY, PREFIXES
import logging
import re

# Optional: configure logging
logger = logging.getLogger("sparql_client")
logger.setLevel(logging.INFO)


def detect_query_type(query: str) -> str:
    """Detects the SPARQL query type."""
    q = query.strip().lower()
    if q.startswith("select"):
        return "SELECT"
    if q.startswith("ask"):
        return "ASK"
    if q.startswith("construct"):
        return "CONSTRUCT"
    if q.startswith("describe"):
        return "DESCRIBE"
    if q.startswith("insert") or q.startswith("delete") or "insert" in q or "delete" in q:
        return "UPDATE"
    return "UNKNOWN"


def inject_prefixes(query: str) -> str:
    """Insert PREFIXES only if the user did not supply them."""
    if re.match(r"^\s*prefix", query, re.IGNORECASE):
        return query
    return PREFIXES + "\n" + query


def run_sparql(query: str, endpoint: str = None, timeout: int = 60):
    """
    Executes SELECT / ASK / CONSTRUCT / DESCRIBE queries.
    For UPDATE queries, use run_sparql_update().
    """
    endpoint = endpoint or GRAPHDB_REPOSITORY
    query_to_send = inject_prefixes(query)
    query_type = detect_query_type(query)

    if query_type == "UPDATE":
        # Redirect user to proper function
        raise RuntimeError(
            "Detected UPDATE query. Use run_sparql_update(query) instead.\n"
        )

    logger.info(f"Executing {query_type} query on {endpoint}")

    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(timeout)
    sparql.setQuery(query_to_send)

    try:
        results = sparql.query().convert()
        return results
    except Exception as e:
        # Extract GraphDB error info if present
        err_msg = str(e)
        match = re.search(r"Error ([\s\S]+)", err_msg)
        graphdb_error = match.group(1).strip() if match else err_msg

        raise RuntimeError(
            f"[SPARQL ERROR]\n"
            f"Endpoint: {endpoint}\n"
            f"Type: {query_type}\n"
            f"Reason: {graphdb_error}\n\n"
            f"--- Query Sent ---\n{query_to_send}\n"
        )


def run_sparql_update(query: str, endpoint: str = None, timeout: int = 60):
    """
    Executes INSERT/DELETE/MODIFY SPARQL UPDATE operations.
    """
    endpoint = endpoint or GRAPHDB_REPOSITORY
    query_to_send = inject_prefixes(query)

    logger.info(f"Executing UPDATE on {endpoint}")

    sparql = SPARQLWrapper(endpoint)
    sparql.setMethod(POSTDIRECTLY)   # required for UPDATE
    sparql.setQuery(query_to_send)
    sparql.setTimeout(timeout)

    try:
        response = sparql.query()
        return True
    except Exception as e:
        raise RuntimeError(
            f"[SPARQL UPDATE ERROR]\n"
            f"Endpoint: {endpoint}\n"
            f"Reason: {e}\n\n"
            f"--- Update Query ---\n{query_to_send}\n"
        )


# Convenience helpers ----------------------------------------------------------

def select(query: str, endpoint: str = None):
    return run_sparql(query, endpoint)


def ask(query: str, endpoint: str = None):
    return run_sparql(query, endpoint)


def construct(query: str, endpoint: str = None):
    endpoint = endpoint or GRAPHDB_REPOSITORY
    query_to_send = inject_prefixes(query)

    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(TURTLE)
    sparql.setQuery(query_to_send)

    try:
        return sparql.query().convert().decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"CONSTRUCT query failed: {e}\nQuery:\n{query_to_send}")
