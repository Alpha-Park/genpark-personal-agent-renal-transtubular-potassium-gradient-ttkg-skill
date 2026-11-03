"""
Example usage of Renal Transtubular Potassium Gradient (TTKG) Skill.
Demonstrates appropriate response vs mineralocorticoid deficiency in hyperkalemia,
and renal wasting vs GI loss in hypokalemia.
"""

import json
from client import TranstubularPotassiumGradientClient


def main():
    print("=== Testing Renal Transtubular Potassium Gradient (TTKG) Skill ===")
    client = TranstubularPotassiumGradientClient()

    # 1. Hyperkalemia with hypoaldosteronism (P_K = 5.8, U_K = 28, P_osm = 290, U_osm = 580 -> TTKG = (28/5.8)/(580/290) = 2.41 < 7.0)
    res_hyper_hypoaldo = client.evaluate_ttkg(
        urine_potassium_mmol_l=28.0,
        plasma_potassium_mmol_l=5.8,
        urine_osmolality_mosm_kg=580.0,
        plasma_osmolality_mosm_kg=290.0,
        urine_sodium_mmol_l=45.0
    )
    print("\n[Case 1: Hyperkalemia with Mineralocorticoid Deficiency / Blunted Secretion]")
    print(json.dumps(res_hyper_hypoaldo, indent=2))

    # 2. Hypokalemia with appropriate renal conservation (P_K = 3.0, U_K = 10, P_osm = 285, U_osm = 600 -> TTKG = 1.58 < 3.0)
    res_hypo_conserve = client.evaluate_ttkg(
        urine_potassium_mmol_l=10.0,
        plasma_potassium_mmol_l=3.0,
        urine_osmolality_mosm_kg=600.0,
        plasma_osmolality_mosm_kg=285.0,
        urine_sodium_mmol_l=55.0
    )
    print("\n[Case 2: Hypokalemia with Appropriate Renal Conservation]")
    print(json.dumps(res_hypo_conserve, indent=2))

    # Assertions
    assert res_hyper_hypoaldo["transtubular_potassium_gradient"] < 7.0
    assert res_hypo_conserve["transtubular_potassium_gradient"] < 3.0
    assert res_hyper_hypoaldo["evaluation"]["is_physiologically_valid"] is True
    print("\n[SUCCESS] Transtubular Potassium Gradient tests passed!")


if __name__ == "__main__":
    main()
