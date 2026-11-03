---
name: genpark-personal-agent-renal-transtubular-potassium-gradient-ttkg-skill
description: Transtubular Potassium Gradient (TTKG) and distal cortical collecting duct bio-potassium handling analyzer. Computes TTKG = (U_K * P_osm) / (P_K * U_osm) to evaluate aldosterone mineralocorticoid bioactivity.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - nephrology
  - potassium
  - aldosterone
  - ttkg
  - electrolytes
  - openclaw
  - genpark
  - mcp
---

# Renal Transtubular Potassium Gradient (TTKG) Skill

## Overview
This skill computes the electrochemical potassium secretory gradient across the cortical collecting duct (CCD):
- **Aldosterone Bioactivity**: Aldosterone upregulates principal cell basolateral Na+/K+-ATPase and apical ROMK/ENaC channels to drive potassium secretion.
- **Hyperkalemic Response**: In hyperkalemia ($P_K > 5.0\text{ mmol/L}$), aldosterone should stimulate distal secretion resulting in $\text{TTKG} > 7.0 - 8.0$. A $\text{TTKG} < 7.0$ signals hypoaldosteronism or mineralocorticoid resistance.
- **Hypokalemic Response**: In hypokalemia ($P_K < 3.5\text{ mmol/L}$), normal kidneys shut down secretion ($\text{TTKG} < 3.0$). A $\text{TTKG} > 3.0$ indicates inappropriate renal potassium wasting.

## Mathematical Formulation
1. **Transtubular Potassium Gradient (TTKG)**:
   $$\text{TTKG} = \frac{U_K \times P_{\text{osm}}}{P_K \times U_{\text{osm}}}$$
2. **Physiological Validity Requirements**:
   - $U_{\text{osm}} \ge P_{\text{osm}}$ (concentrated urine ensures ADH-driven equilibration across medullary collecting duct).
   - $U_{\text{Na}} \ge 25\text{ mmol/L}$ (adequate distal sodium delivery for cation exchange).

## Usage
```python
from client import TranstubularPotassiumGradientClient

client = TranstubularPotassiumGradientClient()
res = client.evaluate_ttkg(
    urine_potassium_mmol_l=32.0,
    plasma_potassium_mmol_l=5.5,
    urine_osmolality_mosm_kg=600.0,
    plasma_osmolality_mosm_kg=295.0
)
print(res["evaluation"]["aldosterone_activity"])
```
