"""
Configuration file for the Manufacturability Reasoning System.
Contains:
- GraphDB endpoint
- Namespaces / PREFIXES for SPARQL queries
- Optional environment overrides
"""

import os

# ---------------------------------------------------------------------------
# GRAPHDB ENDPOINT
# ---------------------------------------------------------------------------

# Allow override via environment variable (useful for deployment)
GRAPHDB_REPOSITORY = os.getenv(
    "repoName",
    "repo_link"
)

# Basic validation
if not GRAPHDB_REPOSITORY.startswith("http://") and not GRAPHDB_REPOSITORY.startswith("https://"):
    raise ValueError(f"Invalid GRAPHDB_REPOSITORY URL: {GRAPHDB_REPOSITORY}")


# ---------------------------------------------------------------------------
# NAMESPACES
# ---------------------------------------------------------------------------

NS_EX = "http://example.org/mps#"
NS_RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
NS_RDFS = "http://www.w3.org/2000/01/rdf-schema#"
NS_OWL = "http://www.w3.org/2002/07/owl#"
NS_XSD = "http://www.w3.org/2001/XMLSchema#"


# ---------------------------------------------------------------------------
# PREFIX BLOCK FOR SPARQL QUERIES
# ---------------------------------------------------------------------------

PREFIXES = f"""
PREFIX ex: <{NS_EX}>
PREFIX rdf: <{NS_RDF}>
PREFIX rdfs: <{NS_RDFS}>
PREFIX owl: <{NS_OWL}>
PREFIX xsd: <{NS_XSD}>
"""


# ---------------------------------------------------------------------------
# OPTIONAL: CLASS NAMES FOR THE DOMAIN ONTOLOGY
# These help the reasoning engine understand the domain.
# ---------------------------------------------------------------------------

CLASS_PROCESS_RECIPE = f"{NS_EX}ProcessRecipe"
CLASS_PROCESS_STEP = f"{NS_EX}ProcessStep"
CLASS_MECHATRONIC_UNIT = f"{NS_EX}MechatronicUnit"
CLASS_SKILL = f"{NS_EX}Skill"
CLASS_IO_SIGNAL = f"{NS_EX}IOSignal"

# Relation properties
PROP_PERFORMED_BY = f"{NS_EX}performedBy"
PROP_NEXT_STEP = f"{NS_EX}nextStep"
PROP_SENDS_IO = f"{NS_EX}sendsIO"
PROP_WAITS_FOR_IO = f"{NS_EX}waitsForIO"
PROP_CONTROLS_IO = f"{NS_EX}controlsIO"
PROP_RECEIVES_IO = f"{NS_EX}receivesIO"

