# FESTO Manufacturability Prototype (Python)

This is a small prototype that converts a user's natural-language prompt into SPARQL, queries a GraphDB repository, and performs simple manufacturability/gap checks using the provided ontology structure.

## How to run
1. Install dependencies:
```
pip install -r requirements.txt
```
2. Edit `config.py` if your GraphDB endpoint is different.
3. Run:
```
python main.py
```

The program will ask for a prompt, convert it to SPARQL, query the repository, and print results and recommended fixes.

## Notes
- This converter is purposely simple and rule-based, tailored to the ontology you provided (prefix `http://example.org/mps#` with classes like `MechatronicUnit`, `Sensor`, `Actuator`, and properties like `:creates`, `:commandOf`, `:hasPart`, `:feeds`). Extend the `nlp_to_sparql.py` logic to handle more complex phrases.
- Repository URL in config.py defaults to `http://LAP-OM-HUSSAIN:7200/repositories/festo`.
