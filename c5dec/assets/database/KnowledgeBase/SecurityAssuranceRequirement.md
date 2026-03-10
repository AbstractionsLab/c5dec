---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: SAR, assurance-requirement, assurance-class, assurance-family, assurance-component, CC-Part-3, CEM
---

# Security assurance requirement

**Acronym:** SAR

A **Security Assurance Requirement (SAR)** specifies the actions a developer must take, the evidence that must be produced, and the analyses an evaluator must perform to gain confidence that the [TOE](./TargetofEvaluation.md) meets its [Security Functional Requirements (SFRs)](./SecurityFunctionalRequirement.md). While SFRs define *what* the TSF must do, SARs define *how thoroughly* the TOE's security claims are verified. SARs are drawn from the assurance [security components](./SecurityComponent.md) catalogued in CC Part 3 and assessed using the activities defined in the Common Evaluation Methodology (CEM).

The selection of SARs determines the depth and rigour of the evaluation and is typically expressed through an [Evaluation Assurance Level (EAL)](./EvaluationAssuranceLevel.md) or a custom assurance [package](./Package.md).

## Hierarchical structure

CC Part 3 organises assurance requirements into a three-level hierarchy, mirroring the functional side:

### Assurance classes

An assurance class groups families that share a common evaluation focus. CC 2022 defines the following assurance classes:

| Class | Name | Evaluation focus |
|-------|------|-----------------|
| APE | Protection Profile evaluation | Evaluation of the PP itself |
| ASE | Security Target evaluation | Evaluation of the ST's completeness and consistency |
| ADV | Development | TOE design documentation (functional specification, TOE design, implementation representation) |
| AGD | Guidance documents | Adequacy of operational and preparative guidance |
| ALC | Life-cycle support | Development environment security, CM, delivery, flaw remediation |
| ATE | Tests | Developer testing, functional test coverage and depth, independent testing |
| AVA | Vulnerability assessment | Vulnerability analysis, penetration testing, attack potential |
| ACO | Composition | Assurance for composed TOEs (reliance and integration evidence) |

> **CC 2022 note:** CC 2022 restructured several assurance classes. The ACO class for composed TOE evaluation was refined. In CC 3.1 R5, the assurance classes were ACM, ADO, ADV, AGD, ALC, ATE, AVA — CC 2022 reorganised configuration management (ACM) and delivery (ADO) under ALC, and added APE/ASE as top-level classes for PP and ST evaluation.

### Assurance families

Each class contains one or more families. A family addresses a specific aspect of assurance (e.g., ADV_FSP — functional specification, ATE_COV — test coverage). Families define the evaluator's focus area.

### Assurance components

Components within a family are hierarchically ordered by rigour. A higher component demands more detailed evidence and deeper evaluator analysis. Each assurance component consists of three types of **assurance elements**:

- **Developer action elements (D)** — What the developer must do (e.g., "The developer shall provide a functional specification").
- **Content and presentation elements (C)** — What the evidence must contain and how it must be presented (e.g., "The functional specification shall describe all TSFIs").
- **Evaluator action elements (E)** — What the evaluator must verify (e.g., "The evaluator shall confirm that the functional specification describes all TSFIs"). Each evaluator action element maps to one or more **work units** in the CEM.

## Relationship between CC and CEM

The CC defines what assurance is required (SARs); the CEM defines how evaluators assess it. The mapping is:

| CC structure | CEM structure |
|---|---|
| Assurance class | Activity |
| Assurance family | Sub-activity |
| Evaluator action element | Action → Work units |

Each work unit is the smallest unit of evaluator effort and produces a pass/fail/inconclusive verdict. See [Evaluation Methods](./EvaluationMethods.md) for details on the evaluation process.

## Practical guidance

### Selecting SARs

1. **Start with an EAL or custom package.** Most evaluations use a predefined [EAL](./EvaluationAssuranceLevel.md) (EAL1–EAL7) as the baseline SAR selection. Custom packages select individual components to match specific assurance needs.

2. **Consider augmentation.** If a specific assurance area requires deeper analysis (e.g., vulnerability analysis for a network-facing product), augment the base EAL with a higher component from that family (e.g., EAL2 + AVA_VAN.3). See [Package](./Package.md) for augmentation rules.

3. **Check scheme requirements.** National schemes and [EUCC](./EUCC.md) often mandate specific SAR selections or minimum EALs for certain product categories.

4. **Ensure PP conformance.** If the ST claims conformance to a [Protection Profile](./ProtectionProfile.md), the SAR selection must satisfy the PP's SAR requirements. Under exact conformance, the SARs must match exactly.

### Understanding SAR impact on developer effort

Each SAR level increase adds evidence requirements. As a guideline:

| SAR area | Low assurance (EAL1-2) | Medium assurance (EAL3-4) | High assurance (EAL5-7) |
|---|---|---|---|
| **Design documentation (ADV)** | Functional spec only | + TOE design | + Implementation representation, formal/semiformal models |
| **Testing (ATE)** | Developer functional tests | + Coverage analysis, independent testing | + Depth analysis, complete independent testing |
| **Vulnerability analysis (AVA)** | Survey of public sources | + Focused penetration testing | + Methodical, independent vulnerability analysis |
| **Life-cycle (ALC)** | Identification of CM system | + Development security, delivery procedures | + Formal CM, flaw remediation procedures |
| **Guidance (AGD)** | Basic operational guidance | + Preparative procedures | + Complete secure configuration guidance |

### Writing SAR rationale

In the [Security Target](./SecurityTarget.md), justify the SAR selection:
1. Link the SAR selection to the identified threat level and the TOE's intended operational environment.
2. If augmenting, explain why the specific augmented component is needed.
3. If deviating from a PP's SAR requirements, provide a conformance rationale.

## Additional resources

- CC 2022 Part 3 — the complete catalogue of assurance classes, families, and components.
- CC 2022 Part 1, Section 6.2 — security assurance requirements structure and usage.
- CEM (ISO/IEC 18045) — evaluator methodology mapped to assurance components.
- ISO/IEC TR 15446 — guidance on SAR selection and rationale development.

## Related articles

- [Security Components](./SecurityComponent.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [Evaluation Assurance Levels](./EvaluationAssuranceLevel.md)
- [Evaluation Methods](./EvaluationMethods.md)
- [Package](./Package.md)
- [Evaluation Evidence](./EvaluationEvidence.md)
- [Protection Profile](./ProtectionProfile.md)
- [Security Target](./SecurityTarget.md)
