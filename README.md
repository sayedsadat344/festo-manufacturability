# FESTO Manufacturability Prototype

This project is a **prototype system to evaluate the manufacturability of recipes on a FESTO Distribution Station**, detect missing skills, and generate IEC 61499 Function Blocks (FBs) for missing capabilities. It uses RDF/OWL ontologies and SPARQL queries to reason over recipes, skills, and station capabilities.

---

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Setup Instructions](#setup-instructions)
4. [Program Components](#program-components)
5. [Program Flow](#program-flow)
6. [Step-by-Step Explanations](#step-by-step-explanations)
7. [Sample Use Cases](#sample-use-cases)
8. [Future Enhancements](#future-enhancements)

---

## Overview

The system allows the user to ask natural-language questions like:

* “Is this product or production process manufacturable on this line?”
* “Which skills are missing for this recipe?”
* “Generate function blocks for missing skills.”

It converts natural-language prompts to SPARQL queries, queries the GraphDB repository containing ontologies for recipes, skills, and distribution stations, and provides a **verdict with actionable suggestions**.

---

## Project Structure

```
.
├── main.py                  # Entry point for the prototype
├── config.py                # GraphDB configuration
├── recipe1.ttl              # Ontology for Recipe 1
├── recipe2.ttl              # Ontology for Recipe 2
├── skills_units_io.ttl      # Skills, units, and IO ontology
├── DistStation_2Units.ttl   # Distribution Station ontology
├── nlp_to_sparql/           # Module to convert natural language to SPARQL
├── sparql_client/           # Module to execute SPARQL queries on GraphDB
├── reasoning_engine/        # Module for manufacturability reasoning
├── skill_generation/        # Module to generate IEC 61499 FBs for missing skills
├── README.md                # This file
```

---

## Setup Instructions

1. Install **Python 3.x** and required libraries:

```bash
pip install requests rdflib
```

2. Configure GraphDB in `config.py`:

```python
GRAPHDB_REPOSITORY = "http://localhost:7200/repositories/myrepo"
```

3. Load all ontologies (`.ttl` files) into your GraphDB repository.

4. Run the prototype:

```bash
python main.py
```

---

## Program Components

### 1. `nlp_to_sparql`

* Converts **natural-language queries** into SPARQL queries.
* Examples:

  * “Is Recipe 1 manufacturable on this station?” → SPARQL checking skills and units.
  * “Which skills are missing?” → SPARQL to find uncovered recipe steps.

### 2. `sparql_client`

* Sends SPARQL queries to GraphDB and returns results as JSON.
* Handles HTTP requests and response parsing.
* Ensures queries are executed correctly and efficiently.

### 3. `reasoning_engine`

* Evaluates **manufacturability**:

  * Checks whether all recipe steps have matching skills on the distribution station.
  * Detects misaligned parameters or missing units.
* Produces a **verdict**: manufacturable or non-manufacturable.
* Returns a list of missing skills or problematic steps.

### 4. `skill_generation`

* Generates **IEC 61499 Function Blocks** for missing skills.
* Uses ontology definitions from `skills_units_io.ttl`.
* Helps extend the station’s capabilities without manual programming.

---

## Program Flow

The workflow of the prototype is as follows:

```
User Prompt (NL)
      ↓
nlp_to_sparql -> Converts NL to SPARQL
      ↓
sparql_client -> Executes queries on GraphDB
      ↓
reasoning_engine -> Analyzes results:
      • Manufacturability check
      • Missing skills detection
      • Misaligned parameters
      ↓
skill_generation -> Generates IEC 61499 FBs (optional)
      ↓
Output: Verdict + Suggestions + FBs
```

---

## Step-by-Step Explanations

### Step 1: User Input

* Prompt the user with natural-language queries about recipe manufacturability.

### Step 2: NLP to SPARQL Conversion (`nlp_to_sparql`)

* Maps natural-language questions to precise SPARQL queries targeting the ontology.
* Example mapping:

  * “Is Recipe 2 manufacturable?” → check all `ProcessStep`s and required skills against station capabilities.

### Step 3: Query Execution (`sparql_client`)

* Sends SPARQL queries to GraphDB.
* Collects JSON results of:

  * Existing skills on the station
  * Recipe steps
  * Unit capabilities

### Step 4: Reasoning (`reasoning_engine`)

* Compares recipe requirements with station capabilities.
* Determines:

  * All steps covered → manufacturable
  * Some steps missing → non-manufacturable
* Returns detailed feedback:

  * Missing skills
  * Units needed
  * Parameter misalignments

### Step 5: Skill Generation (`skill_generation`)

* For missing skills, generates **IEC 61499 FB definitions**.
* These FBs can be integrated into the station to make the recipe executable.

### Step 6: Output

* Prints:

  * Verdict: manufacturable/non-manufacturable
  * Missing skills (if any)
  * Generated IEC 61499 FBs (optional)

---

## Sample Use Cases

1. **Check manufacturability**

```text
"Can Recipe 1 be executed on Distribution Station 2?"
```

2. **Identify missing skills**

```text
"Which skills are required to perform Recipe 2 on this station?"
```

3. **Generate new Function Blocks**

```text
"Create IEC 61499 FBs for missing skills to complete Recipe 2."
```

---

## Future Enhancements

* Automatic **NL-to-SPARQL translation** using LLMs.
* Visual workflow and unit allocation diagrams.
* Real-time **simulation with sensors/actuators feedback**.
* Extended library of **pre-configured IEC 61499 FB templates** for FESTO units.

---

This README provides a **complete guide** to the prototype including files, modules, workflow, and reasoning steps.
