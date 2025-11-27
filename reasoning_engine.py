"""Executes the SPARQL from the converter and performs simple manufacturability/gap reasoning.
It returns a verdict and suggestions.
"""
from sparql_client import run_sparql

def analyze_results(nl_query_info, results):
    intent = nl_query_info.get('intent')
    reason = nl_query_info.get('reason')
    bindings = results.get('results', {}).get('bindings', [])
    verdict = {}
    verdict['intent'] = intent
    verdict['reason'] = reason
    verdict['matches'] = len(bindings)

    # Simple rules for gap detection per intent
    suggestions = []
    if intent == 'vacuum_check':
        if len(bindings) >= 2:
            verdict['verdict'] = 'OK'
            suggestions.append('Vacuum components found. System likely supports vacuum operations.')
        else:
            verdict['verdict'] = 'MISSING'
            suggestions.append('Missing vacuum components (VacuumUnit or VacuumValve or VacuumSensor). Consider adding a VacuumUnit and VacuumValve or linking them in the ontology.')
    elif intent == 'feed_check':
        if len(bindings) >= 1:
            verdict['verdict'] = 'OK'
            suggestions.append('Feeder->Transfer relation found. Feeding path exists.')
            # check optional parts presence by looking into bindings content
            # We keep it simple: if bindings exist we assume parts are present.
        else:
            verdict['verdict'] = 'MISSING'
            suggestions.append('No feeder->transfer relation found. Check that a MechatronicUnit has :feeds property to another unit and that Magazine and FeederPusher parts are present.')
    elif intent == 'command_check':
        if len(bindings) >= 1:
            verdict['verdict'] = 'OK'
            suggestions.append('Command exists in ontology; check actuator mapping and parameters.')
        else:
            verdict['verdict'] = 'MISSING'
            suggestions.append('Command not found. Add :<command> :commandOf :Actuator or ensure commands are linked to actuators.')
    elif intent == 'sensor_check':
        if len(bindings) >= 1:
            verdict['verdict'] = 'OK'
            suggestions.append('Sensors present. Check datapoints produced (e.g. empty, pos_e, pos_r).')
        else:
            verdict['verdict'] = 'MISSING'
            suggestions.append('No sensors found. Add :Sensor instances and link them with :creates to datapoints.')
    else:
        # fallback
        if len(bindings) >= 1:
            verdict['verdict'] = 'OK'
            suggestions.append('Components found; inspect results for details.')
        else:
            verdict['verdict'] = 'MISSING'
            suggestions.append('No components found for the requested query.')

    verdict['suggestions'] = suggestions
    verdict['bindings_preview'] = bindings[:10]
    return verdict
