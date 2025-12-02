#!/usr/bin/env python3
"""
Entry point for the FESTO manufacturability prototype.
Asks user for a prompt, converts it to SPARQL, queries GraphDB,
and prints a manufacturability verdict with gap analysis.
"""

import os
from nlp_to_sparql import nl_to_sparql
from sparql_client import run_sparql
from reasoning_engine import analyze_results
from config import GRAPHDB_REPOSITORY


FB_OUTPUT_DIR = "generated_fbs"
os.makedirs(FB_OUTPUT_DIR, exist_ok=True)


def pretty_print_bindings(bindings, max_preview=5):
    """
    Print first few SPARQL bindings nicely.
    """
    if not bindings:
        print("(No bindings)")
        return

    for i, b in enumerate(bindings):
        if i >= max_preview:
            print(f"... ({len(bindings) - max_preview} more results)")
            break
        print({k: v.get('value') for k, v in b.items()})


def print_gap_section(title, items):
    """
    Print hardware/software gap lists neatly.
    """
    if not items:
        print(f"{title}: None")
        return

    print(f"{title}:")
    for gap in items:
        print(" -", gap)


def main():
    print("=== FESTO Manufacturability Prototype ===")
    print("GraphDB repository:", GRAPHDB_REPOSITORY)
    print("------------------------------------------")
    print("Ask about process steps, units, skills, sensors, IO, vacuum, feeding, commands, etc.")
    print("Example: 'Does the line support vacuum handling?'")
    print("------------------------------------------")

    while True:
        try:
            user_input = input("\nEnter your prompt (or 'exit'): ").strip()
        except EOFError:
            break

        if not user_input or user_input.lower() in ("exit", "quit"):
            print("Goodbye.")
            break

        # -----------------------------------------------------------
        # Convert NL → SPARQL
        # -----------------------------------------------------------
        nl_info = nl_to_sparql(user_input)
        print("\n[NL → SPARQL]")
        print("Intent :", nl_info["intent"])
        print("Reason :", nl_info["reason"])

        print("\nGenerated SPARQL:")
        formatted_sparql = nl_info["sparql"].replace(" .", ".\n  ")
        print(formatted_sparql)

        # -----------------------------------------------------------
        # Execute SPARQL query
        # -----------------------------------------------------------
        try:
            results = run_sparql(nl_info["sparql"])
        except Exception as e:
            print("\nSPARQL execution error:")
            print(e)
            continue

        # -----------------------------------------------------------
        # Manufacturability reasoning
        # -----------------------------------------------------------
        verdict = analyze_results(nl_info, results)

        print("\n=== Manufacturability Evaluation ===")
        print("Intent     :", verdict.get("intent", "unknown"))
        print("Matches    :", verdict.get("matches", 0))
        print("Verdict    :", verdict.get("verdict", "No verdict"))
        print("Manufacturable:", "YES" if verdict.get("manufacturable") else "NO")

        print("\n=== Gap Analysis ===")
        print_gap_section("Hardware gaps", verdict.get("hardware_gaps", []))
        print_gap_section("Software gaps", verdict.get("software_gaps", []))

        print("\n=== Suggestions ===")
        if verdict.get("suggestions"):
            for s in verdict["suggestions"]:
                print(" -", s)
        else:
            print("No suggestions.")

        # -----------------------------------------------------------
        # Bindings preview
        # -----------------------------------------------------------
        print("\n=== SPARQL Bindings Preview ===")
        pretty_print_bindings(verdict.get("bindings_preview", []))

        # -----------------------------------------------------------
        # Generate IEC 61499 FBs if required
        # -----------------------------------------------------------
        print("\n=== Generated Function Blocks ===")
        if verdict["generated_fbs"]:
            for fb in verdict["generated_fbs"]:
                skill_name = fb["skill"]
                xml_content = fb["fb_xml"]

                safe_filename = f"{skill_name}.xml".replace(" ", "_")
                filepath = os.path.join(FB_OUTPUT_DIR, safe_filename)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(xml_content)

                print(f"Generated IEC 61499 FB: {filepath}")
        else:
            print("No FBs generated.")

        print("\n------------------------------------------")


if __name__ == "__main__":
    main()
