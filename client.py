"""
Renal Transtubular Potassium Gradient (TTKG) & Distal Secretion Client.
Zero-mock pure Python standard library implementation.
Calculates the Transtubular Potassium Gradient (TTKG) across the cortical collecting duct,
evaluating aldosterone mineralocorticoid bioactivity and discriminating renal vs extra-renal dyskalemias.
"""

import math
from typing import Dict, Any, Optional


class TranstubularPotassiumGradientClient:
    """
    Computes TTKG = (U_K * P_osm) / (P_K * U_osm) to evaluate cortical collecting duct (CCD)
    potassium secretion driven by aldosterone and distal sodium delivery.
    """

    def __init__(self):
        pass

    def evaluate_ttkg(
        self,
        urine_potassium_mmol_l: float,
        plasma_potassium_mmol_l: float,
        urine_osmolality_mosm_kg: float,
        plasma_osmolality_mosm_kg: float,
        urine_sodium_mmol_l: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates TTKG.
        Physiological validity criteria:
        1. Urine osmolality must be equal to or greater than plasma osmolality (U_osm >= P_osm)
           to ensure ADH is active and distal medullary water abstraction does not confound calculation.
        2. Urine sodium should be > 25 mmol/L to ensure adequate distal sodium delivery for K exchange.
        """
        if plasma_potassium_mmol_l <= 0:
            raise ValueError("Plasma potassium must be positive.")
        if urine_potassium_mmol_l < 0:
            raise ValueError("Urine potassium must be non-negative.")
        if urine_osmolality_mosm_kg <= 0 or plasma_osmolality_mosm_kg <= 0:
            raise ValueError("Osmolality values must be positive.")

        # Validity check: TTKG is strictly accurate when U_osm >= P_osm
        is_physiologically_valid = (urine_osmolality_mosm_kg >= plasma_osmolality_mosm_kg)

        # TTKG formula: (U_K / P_K) / (U_osm / P_osm) = (U_K * P_osm) / (P_K * U_osm)
        ttkg = (urine_potassium_mmol_l * plasma_osmolality_mosm_kg) / (plasma_potassium_mmol_l * urine_osmolality_mosm_kg)

        # Distal delivery flag
        low_distal_na_delivery = False
        if urine_sodium_mmol_l is not None and urine_sodium_mmol_l < 25.0:
            low_distal_na_delivery = True

        # Clinical evaluation of dyskalemia:
        # Case A: Hyperkalemia (P_K > 5.0)
        #   Normal response: Aldosterone triggers K excretion -> TTKG > 7.0 - 8.0
        #   Impaired response (TTKG < 7.0): Hypoaldosteronism, adrenal insufficiency, mineralocorticoid resistance
        # Case B: Hypokalemia (P_K < 3.5)
        #   Normal response: Kidneys conserve K -> TTKG < 3.0
        #   Inappropriate renal wasting (TTKG > 3.0): Hyperaldosteronism, Bartter/Gitelman, diuretic abuse
        # Case C: Normokalemia (P_K 3.5 - 5.0)
        #   Normal baseline TTKG is typically 6.0 - 12.0 on standard Western potassium diet.

        if plasma_potassium_mmol_l > 5.0:
            clinical_context = "Hyperkalemia"
            if ttkg > 7.0:
                classification = "Appropriate Aldosterone-Mediated Renal Potassium Secretion"
                aldosterone_activity = "Intact / Stimulated"
                pathophysiology = "Cortical collecting ducts are actively secreting potassium; suspect high intake or cellular shift."
            else:
                classification = "Impaired Renal Potassium Excretion / Mineralocorticoid Deficit"
                aldosterone_activity = "Deficient or Blunted (Hypoaldosteronism / Type IV RTA)"
                pathophysiology = "Inadequate distal tubular K secretion in the setting of hyperkalemia (TTKG < 7.0)."
        elif plasma_potassium_mmol_l < 3.5:
            clinical_context = "Hypokalemia"
            if ttkg < 3.0:
                classification = "Appropriate Renal Potassium Conservation"
                aldosterone_activity = "Suppressed (Normal Feedback)"
                pathophysiology = "Intact collecting duct K retention; hypokalemia is likely extra-renal (GI loss or transcellular shift)."
            else:
                classification = "Inappropriate Renal Potassium Wasting"
                aldosterone_activity = "Excessive / Unregulated Mineralocorticoid Action"
                pathophysiology = "Ongoing renal K loss despite systemic hypokalemia (TTKG > 3.0); suspect hyperaldosteronism or tubulopathy."
        else:
            clinical_context = "Normokalemia"
            if 4.0 <= ttkg <= 12.0:
                classification = "Normal Baseline Distal Potassium Handling"
                aldosterone_activity = "Normal Homeostatic Range"
                pathophysiology = "Balanced cortical collecting duct secretory gradient."
            elif ttkg < 4.0:
                classification = "Low Distal Potassium Secretory Gradient"
                aldosterone_activity = "Low / Conserving"
                pathophysiology = "Subdued distal potassium excretion."
            else:
                classification = "High Distal Potassium Secretory Gradient"
                aldosterone_activity = "High / Natriuretic-Driven"
                pathophysiology = "Elevated distal potassium secretion."

        validity_notes = []
        if not is_physiologically_valid:
            validity_notes.append("Urine osmolality is lower than plasma osmolality (dilute urine); ADH action is incomplete.")
        if low_distal_na_delivery:
            validity_notes.append("Urine sodium < 25 mmol/L may limit distal sodium-potassium exchange.")

        return {
            "status": "success",
            "transtubular_potassium_gradient": round(ttkg, 2),
            "clinical_context": clinical_context,
            "plasma_potassium_mmol_l": plasma_potassium_mmol_l,
            "urine_potassium_mmol_l": urine_potassium_mmol_l,
            "osmolality_ratio_u_p": round(urine_osmolality_mosm_kg / plasma_osmolality_mosm_kg, 2),
            "evaluation": {
                "classification": classification,
                "aldosterone_activity": aldosterone_activity,
                "pathophysiology": pathophysiology,
                "is_physiologically_valid": is_physiologically_valid,
                "validity_notes": validity_notes
            }
        }
