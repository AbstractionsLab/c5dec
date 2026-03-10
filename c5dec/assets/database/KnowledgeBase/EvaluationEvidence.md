---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: evaluation-evidence, developer-evidence, documentation, assurance, ALC, ADV, AGD, ATE, AVA
---

# Evaluation evidence

**Acronym:** None

**Evaluation evidence** is the collective body of documentation, artefacts, and supporting material that the developer (or sponsor) submits for assessment during a Common Criteria [evaluation](./EvaluationMethods.md). Evaluation evidence demonstrates that the [TOE](./TargetofEvaluation.md) meets its [Security Functional Requirements (SFRs)](./SecurityFunctionalRequirement.md) and that the developer followed appropriate practices as specified by the [Security Assurance Requirements (SARs)](./SecurityAssuranceRequirement.md). The type, depth, and formality of evidence required grows with the [Evaluation Assurance Level (EAL)](./EvaluationAssuranceLevel.md).

## Categories of evidence

Evidence is organised by the assurance class it supports:

### Development evidence (ADV)

Documents describing the TOE's design at increasing levels of detail:

| Component | Evidence | EAL applicability |
|---|---|---|
| ADV_FSP | **Functional specification** — describes all [TSF interfaces](./TSFInterface.md), their parameters, behaviour, and error handling. | EAL1+ |
| ADV_TDS | **TOE design** — describes the TSF's internal structure, subsystems, modules, and their interactions. | EAL2+ |
| ADV_IMP | **Implementation representation** — the TSF source code or hardware design representation. | EAL4+ (partial), EAL6+ (complete) |
| ADV_ARC | **Security architecture** — demonstrates [domain separation](./DomainSeparation.md), [self-protection](./SelfProtection.md), and [non-bypassability](./NonBypassability.md). | EAL1+ |
| ADV_SPM | **Security policy model** — a formal or semiformal model of the TSF's security policy. | EAL5+ |

### Guidance documents (AGD)

| Component | Evidence |
|---|---|
| AGD_OPE | **Operational user guidance** — instructions for secure operation of the TOE by end users and administrators. |
| AGD_PRE | **Preparative procedures** — instructions for secure delivery, installation, and initial configuration. |

### Life-cycle support (ALC)

| Component | Evidence |
|---|---|
| ALC_CMC | **CM capabilities** — description of the configuration management system and its controls. |
| ALC_CMS | **CM scope** — identification of all items under CM (code, documents, test assets). |
| ALC_DEL | **Delivery procedures** — how the TOE is delivered to the consumer without tampering. |
| ALC_DVS | **Development security** — physical and logical security measures in the development environment. |
| ALC_FLR | **Flaw remediation** — procedures for receiving, tracking, and correcting security flaws. |
| ALC_LCD | **Life-cycle definition** — the development model and tools used. |
| ALC_TAT | **Tools and techniques** — development tools with documented options and settings. |

### Tests (ATE)

| Component | Evidence |
|---|---|
| ATE_COV | **Coverage analysis** — mapping of tests to TSF interfaces in the functional specification. |
| ATE_DPT | **Depth analysis** — mapping of tests to TSF subsystem interfaces in the TOE design. |
| ATE_FUN | **Functional tests** — developer's test plans, procedures, and results. |
| ATE_IND | **Independent testing** — evidence supporting evaluator-conducted independent tests. |

### Vulnerability assessment (AVA)

| Component | Evidence |
|---|---|
| AVA_VAN | **Vulnerability analysis** — the developer's vulnerability assessment, list of known vulnerabilities, and justification for resistance claims. |

## Evidence requirements by EAL

The table below summarises which evidence is typically required at each EAL. Higher EALs require more detailed and formal versions of the same evidence:

| Evidence category | EAL1 | EAL2 | EAL3 | EAL4 | EAL5 | EAL6 | EAL7 |
|---|---|---|---|---|---|---|---|
| Functional specification | Basic | Basic | Detailed | Detailed | Semiformal | Formal | Formal |
| TOE design | — | Basic | Basic | Detailed | Semiformal | Formal | Formal |
| Implementation | — | — | — | Subset | Complete | Complete | Complete |
| Security architecture | Basic | Basic | Basic | Detailed | Detailed | Detailed | Detailed |
| Security policy model | — | — | — | — | Semiformal | Formal | Formal |
| Guidance documents | Basic | Basic | Detailed | Detailed | Detailed | Detailed | Detailed |
| CM | Basic | Basic | Detailed | Detailed | Detailed | Detailed | Detailed |
| Developer testing | — | Basic | Basic | Detailed | Detailed | Detailed | Detailed |
| Vulnerability analysis | Survey | Survey | Focused | Enhanced | Systematic | Systematic | Systematic |

## Practical guidance

### Preparing evaluation evidence

1. **Identify the required evidence early.** Based on the target EAL and any scheme-specific requirements, create an evidence checklist. Map each [SAR](./SecurityAssuranceRequirement.md) component to the specific document or artefact it requires.

2. **Align evidence with development artefacts.** Wherever possible, derive evidence from existing development documentation (design documents, test reports, CM system records) rather than creating separate evaluation-only documents.

3. **Maintain traceability.** Each piece of evidence should trace to the SAR component it satisfies and, for development evidence, to the SFRs it covers:
   - Functional specification → TSFIs → SFRs
   - TOE design → TSF subsystems → SFRs
   - Tests → TSFIs and subsystems → SFRs

4. **Follow the content and presentation requirements.** Each SAR component's C (content/presentation) elements specify what the evidence must contain and how it must be structured. Read these requirements carefully before writing.

5. **Establish version control.** All evidence documents should be under configuration management. Evaluators will check CM properties (ALC_CMS, ALC_CMC) and may raise [Observation Reports](./ObservationReport.md) for uncontrolled evidence.

6. **Plan for evidence updates.** As the evaluation progresses and ORs are raised, evidence will need corrections. Design the evidence structure to support incremental updates.

### Evidence quality indicators

Evaluators assess evidence against the CC's content and presentation elements. Common quality characteristics:

- **Completeness** — all required information is present (e.g., all TSFIs are described in the functional specification).
- **Consistency** — evidence at different levels of abstraction is consistent (functional specification and TOE design do not contradict each other).
- **Traceability** — clear mapping between evidence items and between evidence and SFRs/SARs.
- **Clarity** — evidence is understandable to evaluators without requiring developer oral explanation.
- **Currency** — evidence reflects the evaluated version of the TOE, not an earlier or later version.

## Additional resources

- CC Part 3 — defines evidence requirements for each assurance class and component.
- CEM (ISO/IEC 18045) — defines how evaluators assess evidence.
- ISO/IEC TR 15446 — guidance on preparing CC evaluation evidence.

## Related articles

- [Evaluation Evidence Index](./EvaluationEvidenceIndex.md)
- [Evaluation Methods](./EvaluationMethods.md)
- [Evaluation Technical Report](./EvaluationTechnicalReport.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
- [Evaluation Assurance Levels](./EvaluationAssuranceLevel.md)
- [Observation Report](./ObservationReport.md)
- [Security Target](./SecurityTarget.md)
