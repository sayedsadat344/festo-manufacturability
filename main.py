#!/usr/bin/env python3
"""
Entry point for the FESTO manufacturability prototype.
Asks user for a prompt, converts it to SPARQL, queries GraphDB, and prints a verdict + suggestions.
"""

from nlp_to_sparql import nl_to_sparql
from sparql_client import run_sparql
from reasoning_engine import analyze_results
from config import GRAPHDB_REPOSITORY

def pretty_print_bindings(bindings, max_preview=5):
    """Print first few SPARQL bindings nicely, truncate long lists."""
    for i, b in enumerate(bindings):
        if i >= max_preview:
            print(f"... ({len(bindings)-max_preview} more results)")
            break
        print({k: v.get('value') for k, v in b.items()})

def main():
    print("=== FESTO Manufacturability Prototype ===")
    print("GraphDB repository:", GRAPHDB_REPOSITORY)
    print("You can ask about: steps, units, skills, sensors, commands, feeds, vacuum, etc.")

    while True:
        try:
            user_input = input('\nEnter your prompt (or type exit): ').strip()
        except EOFError:
            break
        if not user_input or user_input.lower() in ('exit', 'quit'):
            print('Goodbye.')
            break

        # Convert NL to SPARQL
        nl_info = nl_to_sparql(user_input)
        print('\n[NL -> SPARQL] Intent:', nl_info['intent'])
        print('Reason:', nl_info['reason'])
        print('\nGenerated SPARQL:')
        # Pretty print with line breaks for readability
        print(nl_info['sparql'].replace(" .", ".\n  "))

        # Execute SPARQL query
        try:
            results = run_sparql(nl_info['sparql'])
        except Exception as e:
            print('\nError running SPARQL:', e)
            continue

        # Analyze results
        verdict = analyze_results(nl_info, results)
        print('\n=== Results ===')
        print('Intent:', verdict.get('intent', nl_info['intent']))
        print('Matches:', verdict.get('matches', len(verdict.get('bindings_preview', []))))
        print('Verdict:', verdict.get('verdict', 'No verdict'))
        print('\nSuggestions:')
        for s in verdict.get('suggestions', []):
            print(' -', s)

        print('\nBindings preview:')
        pretty_print_bindings(verdict.get('bindings_preview', []))

if __name__ == '__main__':
    main()
