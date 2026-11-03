# Renal Transtubular Potassium Gradient (TTKG) Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Renal Transtubular Potassium Gradient (TTKG) and Distal Tubular Secretion Evaluator based on nephrological electrolyte physiology.

```mermaid
flowchart TD
    A[Urine & Plasma Potassium + Osmolality] --> B[Check Validity: U_osm >= P_osm]
    B --> C[Compute TTKG = U_K * P_osm / P_K * U_osm]
    C --> D{Serum Potassium Level}
    D -- Hyperkalemia > 5.0 --> E{TTKG > 7.0?}
    E -- Yes --> F[Appropriate Aldosterone Secretion]
    E -- No --> G[Hypoaldosteronism / Type IV RTA]
    D -- Hypokalemia < 3.5 --> H{TTKG < 3.0?}
    H -- Yes --> I[Appropriate Extra-Renal K Loss]
    H -- No --> J[Inappropriate Renal K Wasting]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **Physiological Verification**: Automatically validates urine-to-plasma osmolality ratio and distal sodium delivery conditions.
- **Electrolyte Precision**: Rigorous algorithmic discrimination between mineralocorticoid deficiency, excess, and extra-renal losses.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0
