"""
Enhanced rule-based NL -> SPARQL converter tuned to the provided TTLs.
Recognizes actions/keywords and generates SPARQL templates for:
- Recipes and steps (performedBy, nextStep, sendsIO, waitsForIO)
- Components of certain RDF classes
- Skills and IO signals
- Commands available for actuators
- Sensors that create datapoints
- Relations between units (feeds)
"""

import re

# SPARQL PREFIX declarations for your ontology
PREFIXES = """PREFIX ex: <http://example.org/mps#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""

# Mapping of simple verbs/keywords to ontology properties or commands
ACTION_KEYWORDS = {
    'feed': 'feeds',
    'transfer': 'transfer',  # synonym for pick/place
    'vacuum': 'vacuum',
    'pick': 'transfer',
    'place': 'transfer',
    'retract': 'retract',
    'to_mgz': 'to_mgz',
    'to_next': 'to_next',
    'start_step': 'startStep',
    'wait_for': 'waitsForIO',
    'send_signal': 'sendsIO'
}

# Extract words from NL input
def extract_keywords(text):
    text = text.lower()
    words = re.findall(r"\w+", text)
    return words

def nl_to_sparql(user_input):
    """
    Returns a dict:
    - intent: guessed high-level intent
    - sparql: generated SPARQL query string
    - reason: explanation
    """
    tokens = extract_keywords(user_input)
    intent = None
    reason = ""

    # --- VACUUM RELATED ---
    if any(t in tokens for t in ['vacuum', 'suck', 'vacuumunit', 'vacuum_unit', 'vacuumvalve']):
        intent = 'vacuum_check'
        sparql = PREFIXES + """SELECT ?component ?type WHERE {
    ?component rdf:type ?type .
    FILTER(?type IN (ex:VacuumUnit, ex:Valve, ex:VacuumSensor))
} LIMIT 50"""
        reason = "Check for vacuum-related components (VacuumUnit, Valve, VacuumSensor)."
        return {'intent': intent, 'sparql': sparql, 'reason': reason}

    # --- FEED / TRANSFER ---
    if any(t in tokens for t in ['feed', 'feeds', 'feeding', 'transfer', 'pick', 'place']):
        intent = 'feed_check'
        sparql = PREFIXES + """SELECT ?feeder ?transfer WHERE {
    ?feeder rdf:type ex:MechatronicUnit .
    ?transfer rdf:type ex:MechatronicUnit .
    ?feeder ex:feeds ?transfer .
    OPTIONAL { ?feeder ex:hasPart ?p . ?p rdf:type ex:Magazine . }
    OPTIONAL { ?feeder ex:hasPart ?p2 . ?p2 rdf:type ex:FeederPusher . }
} LIMIT 50"""
        reason = "Check MechatronicUnit feeding relations and parts (Magazine, FeederPusher)."
        return {'intent': intent, 'sparql': sparql, 'reason': reason}

    # --- COMMANDS (retract, to_next, etc.) ---
    command_matches = [k for k in ACTION_KEYWORDS.keys() if k in tokens]
    if command_matches:
        cmd = command_matches[0]
        intent = 'command_check'
        sparql = PREFIXES + f"""SELECT ?cmd ?actuator WHERE {{
    ?cmd ex:commandOf ?actuator .
    FILTER(regex(str(?cmd), "{cmd}", "i"))
}} LIMIT 50"""
        reason = f"Check for command '{cmd}' and its associated actuator."
        return {'intent': intent, 'sparql': sparql, 'reason': reason}

    # --- RECIPE / STEP QUERIES ---
    if 'step' in tokens or 'recipe' in tokens:
        intent = 'recipe_step_query'
        filters = []
        for t in tokens:
            if t.startswith('unit'):  # e.g., "unitX"
                filters.append(f"?step ex:performedBy ex:{t}")
            if t.startswith('signal'):  # e.g., "signalY"
                filters.append(f"?step ex:sendsIO ex:{t}")
        filter_clause = " . ".join(filters) if filters else ""
        sparql = PREFIXES + f"""SELECT ?step ?unit WHERE {{
    ?step rdf:type ex:ProcessStep .
    ?step ex:partOf ?recipe .
    {filter_clause}
}} LIMIT 50"""
        reason = "Query steps in a recipe, optionally filtered by performing unit or IO signal."
        return {'intent': intent, 'sparql': sparql, 'reason': reason}

    # --- SENSOR / DATAPOINT / SKILL IO ---
    if any(t in tokens for t in ['sensor', 'signal', 'empty', 'pos_e', 'pos_r']):
        intent = 'sensor_io_check'
        sparql = PREFIXES + """SELECT ?sensor ?io ?skill WHERE {
    ?sensor rdf:type ex:Sensor .
    OPTIONAL { ?sensor ex:creates ?io }
    OPTIONAL {
        ?skill rdf:type ex:Skill .
        ?skill ex:controlsIO ?io .
        ?skill ex:receivesIO ?io .
    }
} LIMIT 100"""
        reason = "List sensors, IO signals they create, and skills controlling/receiving them."
        return {'intent': intent, 'sparql': sparql, 'reason': reason}

    # --- FALLBACK: List main components, units, skills, and types ---
    intent = 'list_components'
    sparql = PREFIXES + """SELECT ?component ?type WHERE {
    ?component rdf:type ?type .
    FILTER(?type IN (ex:MechatronicUnit, ex:Magazine, ex:FeederPusher, ex:TransferArm, ex:VacuumUnit,
                     ex:Valve, ex:Sensor, ex:Cylinder, ex:Skill, ex:ProcessStep))
} LIMIT 200"""
    reason = "List main components, units, skills, steps, and types (fallback)."
    return {'intent': intent, 'sparql': sparql, 'reason': reason}

# --- Example usage ---
if __name__ == "__main__":
    test_inputs = [
        "Which steps are performed by Unit1?",
        "List all vacuum valves",
        "Show feeds from feeder units",
        "Is there a sensor for empty magazine?",
        "Check the retract command"
    ]
    for inp in test_inputs:
        res = nl_to_sparql(inp)
        print(f"NL Input: {inp}")
        print(f"Intent: {res['intent']}")
        print(f"SPARQL:\n{res['sparql']}")
        print(f"Reason: {res['reason']}")
        print("-"*50)
