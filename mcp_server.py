"""
MCP Server for Renal Transtubular Potassium Gradient (TTKG) Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import TranstubularPotassiumGradientClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-renal-transtubular-potassium-gradient-ttkg-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_ttkg",
                        "description": "Calculate Transtubular Potassium Gradient (TTKG) to assess aldosterone action and distal tubular potassium handling.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "urine_potassium_mmol_l": {"type": "number", "description": "Spot urine potassium (mmol/L)."},
                                "plasma_potassium_mmol_l": {"type": "number", "description": "Serum/plasma potassium (mmol/L)."},
                                "urine_osmolality_mosm_kg": {"type": "number", "description": "Urine osmolality (mOsm/kg)."},
                                "plasma_osmolality_mosm_kg": {"type": "number", "description": "Plasma osmolality (mOsm/kg)."},
                                "urine_sodium_mmol_l": {"type": "number", "description": "Spot urine sodium (mmol/L, optional)."}
                            },
                            "required": [
                                "urine_potassium_mmol_l",
                                "plasma_potassium_mmol_l",
                                "urine_osmolality_mosm_kg",
                                "plasma_osmolality_mosm_kg"
                            ]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "evaluate_ttkg":
            client = TranstubularPotassiumGradientClient()
            try:
                res = client.evaluate_ttkg(
                    urine_potassium_mmol_l=float(args["urine_potassium_mmol_l"]),
                    plasma_potassium_mmol_l=float(args["plasma_potassium_mmol_l"]),
                    urine_osmolality_mosm_kg=float(args["urine_osmolality_mosm_kg"]),
                    plasma_osmolality_mosm_kg=float(args["plasma_osmolality_mosm_kg"]),
                    urine_sodium_mmol_l=float(args["urine_sodium_mmol_l"]) if "urine_sodium_mmol_l" in args and args["urine_sodium_mmol_l"] is not None else None
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
