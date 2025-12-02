"""
NL → SPARQL conversion engine for manufacturability analysis.
Enhanced for FESTO MPS and skills-based IEC 61499 logic.

Supports:
- Skill capability queries
- Missing-skill detection
- IO reasoning
- Recipe reasoning
- Unit/component lookup
- Feeding, vacuum, transfer actions
"""

import re
from config import PREFIXES


# --------------------------------------------------------------
# Helpers
# --------------------------------------------------------------

def extract_keywords(text):
    """Lowercase and tokenize words."""
    return re.findall(r"[A-Za-z0-9_]+", text.lower())


def detect_skill_keywords(tokens):
    """Detect skill names like moveToPos, grip, transfer, retract, etc."""
    skill_like = [t for t in tokens if t.startswith("skill") or "move" in t or "transfer" in t]
    return skill_like


def detect_step_keywords(tokens):
    return [t for t in tokens if t.startswith("step") or "step" in t]


def detect_unit_keywords(tokens):
    return [t for t in tokens if t.startswith("unit") or "station" in t or "arm" in t]


def detect_io_keywords(tokens):
    return [t for t in tokens if "signal" in t or t.startswith("io") or "pos" in t]


# --------------------------------------------------------------
# Core NL → SPARQL
# --------------------------------------------------------------

def nl_to_sparql(user_input):
    """
    Returns dict:
    - intent: high-level task
    - sparql: generated SPARQL
    - reason: explanation
    """
    tokens = extract_keywords(user_input)

    # ----------------------------------------------------------
    # 1. Manufacturability Check
    # ----------------------------------------------------------
    if any(t in tokens for t in ["manufacturable", "manufacturability", "possible", "can", "capable"]):
        if "process" in tokens or "product" in tokens:
            intent = "manufacturability_check"
            sparql = PREFIXES + """
SELECT ?step ?requiredSkill ?unit WHERE {
    ?step rdf:type ex:ProcessStep .
    ?step ex:requiresSkill ?requiredSkill .

    OPTIONAL {
        ?unit rdf:type ex:MechatronicUnit .
        ?unit ex:providesSkill ?requiredSkill .
    }
}
"""
            reason = (
                "Checks which required skills of a product/process exist on available units. "
                "Used to detect missing skills."
            )
            return {"intent": intent, "sparql": sparql, "reason": reason}

    # ----------------------------------------------------------
    # 2. Missing-Skill Detection
    # ----------------------------------------------------------
    if "missing" in tokens and "skill" in tokens:
        intent = "missing_skill_check"
        sparql = PREFIXES + """
SELECT ?requiredSkill WHERE {
    ?step rdf:type ex:ProcessStep .
    ?step ex:requiresSkill ?requiredSkill .
    FILTER NOT EXISTS {
        ?unit rdf:type ex:MechatronicUnit .
        ?unit ex:providesSkill ?requiredSkill .
    }
}
"""
        reason = "Lists required skills that no unit in the line currently provides."
        return {"intent": intent, "sparql": sparql, "reason": reason}

    # ----------------------------------------------------------
    # 3. List All Available Skills
    # ----------------------------------------------------------
    if ("skill" in tokens and "list" in tokens) or "skills" in tokens:
        intent = "list_skills"
        sparql = PREFIXES + """
SELECT ?skill ?unit WHERE {
    ?skill rdf:type ex:Skill .
    OPTIONAL {
        ?unit rdf:type ex:MechatronicUnit .
        ?unit ex:providesSkill ?skill .
    }
}
"""
        reason = "Lists skills and which mechatronic units provide them."
        return {"intent": intent, "sparql": sparql, "reason": reason}

    # ----------------------------------------------------------
    # 4. Vacuum Component Lookup
    # ----------------------------------------------------------
    if any(t in tokens for t in ["vacuum", "suck", "vacuumunit", "vacuumvalve", "vacuum_sensor"]):
        intent = "vacuum_check"
        sparql = PREFIXES + """
SELECT ?component ?type WHERE {
    ?component rdf:type ?type .
    FILTER(?type IN (ex:VacuumUnit, ex:Valve, ex:VacuumSensor))
}"""
        reason = "Checks vacuum-related components (units, valves, sensors)."
        return {"intent": intent, "sparql": sparql, "reason": reason}

    # ----------------------------------------------------------
    # 5. Feed / Transfer / Pick / Place
    # ----------------------------------------------------------
    if any(t in tokens for t in ["feed", "transfer", "feeds", "pick", "place"]):
        intent = "feed_transfer_check"
        sparql = PREFIXES + """
SELECT ?feeder ?target WHERE {
    ?feeder rdf:type ex:MechatronicUnit .
    ?feeder ex:feeds ?target .
}"""
        reason = "Checks feeding/transfer relations between mechatronic units."
        return {"intent": intent, "sparql": sparql, "reason": reason}

    # ----------------------------------------------------------
    # 6. Unit Capability Query
    # “What can Unit1 do?”
    # ----------------------------------------------------------
    units = detect_unit_keywords(tokens)
    if units:
        u = units[0]
        intent = "unit_skills"
        sparql = PREFIXES + f"""
SELECT ?skill WHERE {{
    ex:{u} rdf:type ex:MechatronicUnit .
    ex:{u} ex:providesSkill ?skill .
}}"""
        reason = f"Lists skills provided by unit {u}."
        return {"intent": intent, "sparql": sparql, "reason": reason}

    # ----------------------------------------------------------
    # 7. IO Signal Query
    # ----------------------------------------------------------
    ios = detect_io_keywords(tokens)
    if ios:
        intent = "io_query"
        sparql = PREFIXES + """
SELECT ?sensor ?io ?skill WHERE {
    ?sensor rdf:type ex:Sensor .
    OPTIONAL { ?sensor ex:creates ?io }
    OPTIONAL {
        ?skill rdf:type ex:Skill .
        ?skill ex:controlsIO ?io .
        ?skill ex:receivesIO ?io .
    }
}"""
        reason = "Lists IO, related sensors, and which skills use/produce IO signals."
        return {"intent": intent, "sparql": sparql, "reason": reason}

    # ----------------------------------------------------------
    # 8. Recipe / Step Query
    # ----------------------------------------------------------
    if "step" in tokens or "recipe" in tokens:
        intent = "recipe_step_query"
        sparql = PREFIXES + """
SELECT ?step ?unit WHERE {
    ?step rdf:type ex:ProcessStep .
    OPTIONAL { ?step ex:performedBy ?unit }
}"""
        reason = "Lists steps and the units performing them."
        return {"intent": intent, "sparql": sparql, "reason": reason}

    # ----------------------------------------------------------
    # 9. Fallback – List main components
    # ----------------------------------------------------------
    intent = 'list_components'
    sparql = PREFIXES + """
SELECT ?component ?type WHERE {
    ?component rdf:type ?type .
    FILTER(?type IN (
        ex:MechatronicUnit, ex:Magazine, ex:FeederPusher, ex:TransferArm,
        ex:VacuumUnit, ex:Valve, ex:Sensor, ex:Cylinder, ex:Skill, ex:ProcessStep
    ))
}"""
    reason = "Fallback: list main components and their types."
    return {"intent": intent, "sparql": sparql, "reason": reason}


# --------------------------------------------------------------
# Test
# --------------------------------------------------------------
if __name__ == "__main__":
    tests = [
        "Is this process manufacturable?",
        "List missing skills",
        "What skills does Unit1 provide?",
        "Show all IO signals",
        "Which unit feeds the next one?",
        "Check vacuum valves",
        "List all skills",
        "Show recipe steps",
    ]
    for t in tests:
        o = nl_to_sparql(t)
        print("\nINPUT:", t)
        print("INTENT:", o["intent"])
        print("SPARQL:\n", o["sparql"])
        print("REASON:", o["reason"])
        print("-" * 50)
