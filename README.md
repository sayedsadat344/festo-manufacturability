
# 🤖 LLM-Driven Manufacturability Analysis for FESTO Distribution Station

An experimental research project exploring how **Large Language Models (LLMs), knowledge graphs, ontologies, industrial automation, and simulation** can work together to automatically determine whether a product or production process can be implemented on a given manufacturing line.

The **FESTO MPS Distribution Station** is used as a simplified industrial use case for investigating manufacturability analysis, capability gaps, automated solution generation, and simulation-based validation.

---

## 🎯 Project Goal

The main goal is to build an intelligent system that can answer a fundamental manufacturing question:

> **"Can this product or production process be implemented on this production line?"**

To answer this question, the system reasons over multiple layers of knowledge describing the manufacturing environment, identifies incompatibilities or missing capabilities, and proposes possible solutions.

These solutions may include:

* 🔗 Adding missing ontology relationships
* 🏭 Adding required equipment or tools
* ⚙️ Identifying missing production capabilities
* 🧩 Detecting incompatible parameters
* 💻 Identifying missing control logic
* 🤖 Generating IEC 61499/PLC code patches

---

## 🧠 Knowledge Graph & Ontology

The project uses **GraphDB** as the knowledge-graph foundation. The manufacturing environment is represented through multiple interconnected ontological layers describing:

* Product features
* Structural properties of the production line
* Functional capabilities
* Available machinery and equipment
* Automation and control software
* Recipes and related system information

By connecting these concepts in a knowledge graph, the system can reason about relationships between **products, processes, machines, capabilities, and control logic**.

---

## 🤖 LLM-Based Reasoning

A key research direction is combining traditional semantic reasoning with **Large Language Models**.

The system can potentially use:

**User Request → LLM → Knowledge Graph → SPARQL/Reasoning → Manufacturability Analysis → Gap Identification → Proposed Solution**

For example, when a user asks whether a particular process can be executed on the FESTO Distribution Station, the system can analyze the available capabilities and identify:

* Missing machinery
* Missing operations
* Unsupported parameters
* Missing relationships in the ontology
* Missing automation logic

The project specifically investigates whether **SPARQL queries, LLM-based analysis, or a combination of both** can establish whether a product or process is implementable on a production line.

---

## ⚙️ Skills-Based Industrial Automation

The FESTO Distribution Station control application is based on the **Skills approach** using **IEC 61499** and **EcoStruxure Automation Expert**.

A skill represents a unified, stateful service associated with a mechatronic component. Each operation exposes a standardized interface that can be invoked through:

* IEC 61499 applications
* HMI faceplates
* OPC UA

This approach improves interoperability and makes the structure of the automation system easier to understand by representing relationships between skills in a knowledge graph.

---

## 🔍 Research Questions

The project investigates three primary research questions:

### RQ1 — Manufacturability Analysis

How can a collection of documents describing different aspects of an automated production system be used to automatically determine whether a particular product or process can be produced or implemented?

The investigation includes:

* GraphDB
* SPARQL
* Ontology-based reasoning
* LLM-based analysis
* Hybrid semantic + LLM approaches

### RQ2 — Automatic Gap Identification & Generation

If a product or process cannot be implemented, how can the system automatically identify the missing physical or software components?

The longer-term objective is to explore whether these missing components can also be **automatically generated or proposed**.

### RQ3 — Simulation-Based Validation

How can simulation models of production modules be integrated into the manufacturability-analysis workflow?

The project considers developing or using simulation models and connecting them to the **SoftPLC of EcoStruxure Automation Expert**, potentially enabling proposed solutions to be tested in a simulated production environment.

---

## 🏭 FESTO MPS Distribution Station

The **FESTO MPS Distribution Station** acts as the primary experimental platform for the project.

The provided control application demonstrates a semi-automatic implementation using the Skills approach. The system can be operated through a simulation canvas where individual skills can be initiated through their HMI faceplates.

This makes the station a useful simplified environment for experimenting with:

> **Ontology → Knowledge Graph → AI Reasoning → Gap Detection → Automation → Simulation**

---

## 🔄 Conceptual Workflow

```text
                    User / Product Specification
                              │
                              ▼
                     ┌─────────────────┐
                     │      LLM        │
                     │ Reasoning Layer │
                     └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │     GraphDB     │
                    │ Knowledge Graph │
                    └────────┬────────┘
                              │
                    SPARQL / Semantic
                         Reasoning
                              │
                              ▼
                  ┌─────────────────────┐
                  │ Manufacturability  │
                  │      Analysis       │
                  └──────────┬──────────┘
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
          Implementable            Not Implementable
                 │                       │
                 ▼                       ▼
             Execute              Gap Identification
                                         │
                              ┌──────────┴──────────┐
                              ▼                     ▼
                       Physical Gaps          Software Gaps
                              │                     │
                              └──────────┬──────────┘
                                         ▼
                              Proposed / Generated
                                  Improvements
                                         │
                                         ▼
                              Simulation / SoftPLC
                                  Validation
```

---

## 🧩 Technologies & Concepts

The project brings together several technologies and research areas:

| Area                        | Technology / Concept          |
| --------------------------- | ----------------------------- |
| 🧠 AI                       | Large Language Models (LLMs)  |
| 🕸️ Knowledge Graph         | GraphDB                       |
| 🔎 Querying                 | SPARQL                        |
| 📚 Semantic Modeling        | RDF / Ontologies              |
| ⚙️ Automation               | IEC 61499                     |
| 🏭 Industrial Automation    | EcoStruxure Automation Expert |
| 🔌 Industrial Communication | OPC UA                        |
| 🎛️ Control                 | SoftPLC                       |
| 🧩 Architecture             | Skills-based automation       |
| 🧪 Validation               | Simulation / Digital Twin     |

The provided project materials include an EcoStruxure Automation Expert solution, RDF/Turtle ontologies, ontology visualizations, a demonstration video, and supporting presentation material.

---

## 🚀 Vision

The broader vision of this project is to explore a more **intelligent, semantic, interoperable, and adaptable approach to industrial automation**.

Instead of manually checking whether a new product can be produced on an existing production line, an intelligent system could understand the capabilities of the line, reason over its available equipment and software, identify what is missing, propose how the gaps can be resolved, and potentially validate the proposed solution through simulation.

In this way, the project investigates the intersection of:

**🤖 Artificial Intelligence + 🕸️ Knowledge Graphs + 🏭 Industrial Automation + 🔌 OPC UA + ⚙️ IEC 61499 + 🧪 Simulation**

with the **FESTO MPS Distribution Station** serving as the experimental platform for developing and evaluating these ideas.




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
