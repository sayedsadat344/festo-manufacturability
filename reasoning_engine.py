"""
Improved reasoning engine with manufacturability judgment,
hardware/software gap detection, and optional IEC 61499 FB generation.
"""

from sparql_client import run_sparql


# ---------------------------------------------------------
#  IEC 61499 FB SKELETON GENERATION
# ---------------------------------------------------------
def generate_fb_skeleton(skill_name: str) -> str:
    """Generate a minimal but valid IEC 61499 FB XML skeleton."""
    xml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<FUNC_BLOCK Name="{skill_name}" Type="FB">
    <Interface>
        <EventInputs>
            <Event Name="INIT"/>
            <Event Name="REQ"/>
        </EventInputs>
        <EventOutputs>
            <Event Name="CNF"/>
            <Event Name="EO"/>
        </EventOutputs>
        <DataInputs>
            <Var Name="InputSignal" Type="BOOL"/>
        </DataInputs>
        <DataOutputs>
            <Var Name="OutputSignal" Type="BOOL"/>
        </DataOutputs>
    </Interface>
    <Algorithms>
        <!-- Add algorithm code here -->
    </Algorithms>
    <ECStateMachine>
        <!-- Add Execution Control logic here -->
    </ECStateMachine>
</FUNC_BLOCK>
"""
    return xml_template


# ---------------------------------------------------------
#  CENTRAL REASONING ENGINE
# ---------------------------------------------------------
def analyze_results(nl_query_info, results):
    """
    Map SPARQL query results to manufacturability decisions.
    This version classifies gaps as hardware or software-related
    and suggests fixes.
    """

    intent = nl_query_info.get("intent")
    reason = nl_query_info.get("reason")
    bindings = results.get("results", {}).get("bindings", [])

    # Base response object
    verdict = {
        "intent": intent,
        "reason": reason,
        "matches": len(bindings),
        "manufacturable": None,      # final yes/no
        "verdict": "",              # human-readable
        "hardware_gaps": [],
        "software_gaps": [],
        "suggestions": [],
        "bindings_preview": bindings[:10],
        "generated_fbs": []
    }

    # ---------------------------------------------------------
    #  Helper to register missing components
    # ---------------------------------------------------------
    def missing_hardware(msg):
        verdict["hardware_gaps"].append(msg)
        verdict["suggestions"].append("Hardware missing: " + msg)

    def missing_software(skill_name):
        verdict["software_gaps"].append(f"Missing skill: {skill_name}")
        verdict["suggestions"].append(f"Software missing: Define skill '{skill_name}'")

        fb_xml = generate_fb_skeleton(skill_name)
        verdict["generated_fbs"].append({"skill": skill_name, "fb_xml": fb_xml})
        verdict["suggestions"].append(f"Generated IEC 61499 FB for skill '{skill_name}'")

    # ---------------------------------------------------------
    #  INTENT-SPECIFIC REASONING
    # ---------------------------------------------------------

    # 1) Vacuum check
    if intent == "vacuum_check":
        if len(bindings) >= 2:
            verdict["manufacturable"] = True
            verdict["verdict"] = "Manufacturable: Vacuum subsystem present."
        else:
            verdict["manufacturable"] = False
            verdict["verdict"] = "Not Manufacturable: Vacuum subsystem incomplete."
            missing_hardware("VacuumUnit / VacuumValve / VacuumSensor")

    # 2) Feed check
    elif intent == "feed_check":
        if len(bindings) >= 1:
            verdict["manufacturable"] = True
            verdict["verdict"] = "Manufacturable: Feeding path found."
        else:
            verdict["manufacturable"] = False
            verdict["verdict"] = "Not Manufacturable: No feeding path."
            missing_hardware("Magazine, FeederPusher, or TransferUnit")

    # 3) Command-to-actuator mapping check
    elif intent == "command_check":
        if len(bindings) >= 1:
            verdict["manufacturable"] = True
            verdict["verdict"] = "Manufacturable: Command mapping found."
        else:
            verdict["manufacturable"] = False
            verdict["verdict"] = "Not Manufacturable: Missing command logic."
            missing_software("MissingActuatorCommandSkill")

    # 4) Sensor check
    elif intent in ["sensor_check", "sensor_io_check"]:
        if len(bindings) >= 1:
            verdict["manufacturable"] = True
            verdict["verdict"] = "Manufacturable: Sensor–IO mapping available."
        else:
            verdict["manufacturable"] = False
            verdict["verdict"] = "Not Manufacturable: Missing sensors."
            missing_hardware("Sensor / SensorIO")
            missing_software("SensorProcessingSkill")

    # 5) Full recipe evaluation
    elif intent == "recipe_step_query":
        if len(bindings) >= 1:
            verdict["manufacturable"] = True
            verdict["verdict"] = "Manufacturable: All recipe steps assigned."
        else:
            verdict["manufacturable"] = False
            verdict["verdict"] = "Not Manufacturable: Recipe has missing or unassigned steps."
            missing_software("MissingRecipeSkill")

    # ---------------------------------------------------------
    #  DEFAULT CASE
    # ---------------------------------------------------------
    else:
        if len(bindings) >= 1:
            verdict["manufacturable"] = True
            verdict["verdict"] = "Manufacturable: Components match query."
        else:
            verdict["manufacturable"] = False
            verdict["verdict"] = "Not Manufacturable: Required components missing."
            missing_hardware("Unknown required component")
            missing_software("MissingSkill")

    return verdict
