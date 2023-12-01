---
Last Updated: October 4, 2023
Relevant CC Version: 3.1 Revision 5, CC 2022
Tags: [Evaluation Assurance Level, EAL]
---

# Evaluation Assurance Level

**Acronym:** EAL

An attack potential is a measure of the effort to be expended in attacking a TOE, expressed as the sum of the numerical values calculated for each of the five factors

| Attack Factor | Value Range | Example Values |
|----|----|----|
| **Elapsed time** | (0-8)        | It refers to the time required for mounting the attack. The value is weighted in accordance with the elapsed time. "less than one day" (value: 0), "between one day and one week" (value: 1), "between one week and two weeks" (value: 2), "between two weeks and one month" (value: 4) |
| **Specialist expertise** | (0-11) | It refers to the generic technical knowledge required for mounting the attack. The value is weighted in accordance with the level of knowledge. "layman" (value: 0), "proficient person" (value: 3), "expert" (value: 6) |
| **Knowledge of TOE** | (0-19) | It refers to knowledge of the design and operation of the target product that is required for successfully mounting the attack. The value is weighted in accordance with the difficulty in obtaining the product information. "public information" (value: 0), "restricted information" (value: 3), "sensitive information" (value: 7)  |
| **Window of opportunity** | (0-10) | It refers to the access opportunity to the target product that is required for the attack. The value is weighted in accordance with the difficulty involved in accessing the product without the attack being noticed until the success of the attack. "unnecessary/unlimited access" (value: 0), "easy access" (value: 1), "moderate access" (value: 4), "difficult access" (value: 10) |
| **Equipment** | (0-9) | It refers to the software or hardware required for the attack. The value is weighted in accordance with the difficulty in obtaining the equipment. "standard equipment" (value:0), "specialized equipment" (value: 4), "bespoke equipment" (value: 7) |

The calculated attack potential translates to a Vulnerability analysis (AVA_VAN) component, and indirectly to an [Evaluation Assurance Level](./EvaluationAssuranceLevel.md).

| Values | Attack Potential required to exploit scenario | Meets assurance components | Failure of components|
|---|---|---|---|
| 0-9 | basic | - | AVA_VAN.1, AVA_VAN.2, AVA_VAN.3, AVA_VAN.4, AVA_VAN.5 |
| 10-13 | enhanced-basic | AVA_VAN.1, AVA_VAN.2 | AVA_VAN.3, AVA_VAN.4, AVA_VAN.5 |
| 14-19 | moderate | AVA_VAN.1, AVA_VAN.2, AVA_VAN.3 | AVA_VAN.4, AVA_VAN.5 |
| 20-24 | high | AVA_VAN.1, AVA_VAN.2, AVA_VAN.3, AVA_VAN.4 | AVA_VAN.5 |
| =>25 | beyond high | AVA_VAN.1, AVA_VAN.2, AVA_VAN.3, AVA_VAN.4, AVA_VAN.5 | - |

The [TOE's](./TargetofEvaluation.md) resistance must be equal to the highest attack potential, i.e., the attack scenario with the highest attack potential is decisive for the determination of TOE resistance, vulnerability analysis component, and subsequently the TOE’s EAL.
