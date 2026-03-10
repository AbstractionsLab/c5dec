---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: evidence-index, evidence-management, evaluation-process, traceability, ETR
---

# Evaluation evidence index

**Acronym:** EEI

The **Evaluation Evidence Index** is an inventory document that catalogues all [evaluation evidence](./EvaluationEvidence.md) submitted by the developer (sponsor) and received by the evaluator during a Common Criteria [evaluation](./EvaluationMethods.md). It serves as the master reference for tracking which documents have been delivered, their versions, and their mapping to [Security Assurance Requirements (SARs)](./SecurityAssuranceRequirement.md). The evidence index is a key management artefact that supports evidence traceability, completeness checking, and is typically included or referenced in the [Evaluation Technical Report (ETR)](./EvaluationTechnicalReport.md).

## Purpose

The Evaluation Evidence Index serves several critical functions:

1. **Completeness verification.** By mapping each SAR component to the evidence artefact that satisfies it, the index helps evaluators verify that all required evidence has been submitted.
2. **Version control.** The index tracks document versions, ensuring evaluators are working with the correct version of each artefact.
3. **Traceability.** The index provides a single point of reference for tracing from SAR components to the evidence that addresses them.
4. **Evaluation management.** The index supports project management by tracking delivery status, review status, and any outstanding evidence gaps.
5. **ETR support.** The ETR references the evidence index as the authoritative list of evaluated artefacts.

## Structure

A typical evidence index contains the following information for each artefact:

| Field | Description |
|---|---|
| **Document ID** | Unique identifier for the artefact (developer's document number or reference). |
| **Title** | Document title. |
| **Version** | Version number or date of the evaluated version. |
| **Date received** | Date the artefact was delivered to the evaluator. |
| **SAR mapping** | Which SAR component(s) the artefact addresses (e.g., ADV_FSP.4, ATE_FUN.1). |
| **Status** | Delivery and review status (e.g., received, under review, accepted, superseded). |
| **Notes** | Any relevant comments (e.g., "Updated per OR-007 response"). |

## Practical guidance

### Building an evidence index

1. **Start from the SAR selection.** List all SAR components from the [Security Target](./SecurityTarget.md). For each component, identify the developer action elements (D) and content/presentation elements (C) — these define what evidence is needed.

2. **Map evidence to SARs.** For each SAR component, identify which developer document or artefact satisfies the requirement. A single document may address multiple SAR components (e.g., a design document may satisfy both ADV_TDS and ADV_ARC requirements).

3. **Record versions explicitly.** For each artefact, record the exact version (include version numbers, dates, or commit hashes). This is essential for reproducibility and for maintaining consistency if evidence is updated during evaluation.

4. **Track delivery status.** Mark artefacts as delivered, pending, or superseded. This enables evaluators to quickly identify evidence gaps at any point during the evaluation.

5. **Update the index throughout the evaluation.** As [Observation Reports](./ObservationReport.md) are raised and resolved, evidence artefacts may be updated. Reflect all updates in the index with new version numbers and dates.

6. **Include in or reference from the ETR.** The final evidence index should be included as an appendix to the ETR or referenced from it, providing a complete record of all evaluated artefacts.

### Evidence index template

A minimal evidence index structure:

```
| # | Document ID | Title                    | Version | Date Received | SAR Components          | Status   |
|---|-------------|--------------------------|---------|---------------|-------------------------|----------|
| 1 | FSP-001     | Functional Specification | 2.3     | 2026-01-15    | ADV_FSP.4               | Accepted |
| 2 | TDS-001     | TOE Design               | 1.5     | 2026-01-15    | ADV_TDS.3, ADV_ARC.1    | Accepted |
| 3 | TST-001     | Developer Test Report     | 3.0     | 2026-02-01    | ATE_FUN.1, ATE_COV.2    | Accepted |
| 4 | GD-001      | Administrator Guide       | 2.1     | 2026-01-20    | AGD_OPE.1, AGD_PRE.1    | Accepted |
| 5 | CM-001      | CM Plan                   | 1.2     | 2026-01-15    | ALC_CMC.4, ALC_CMS.4    | Accepted |
| 6 | VA-001      | Vulnerability Assessment  | 1.0     | 2026-02-10    | AVA_VAN.3               | Accepted |
```

### Common pitfalls

- **Incomplete mapping.** Ensure every SAR component has at least one evidence artefact mapped to it. Unmapped SARs indicate evidence gaps.
- **Stale versions.** If evidence is updated during evaluation, update the index. Evaluators working with outdated versions will raise ORs.
- **Missing artefacts.** The index should include all evidence, not just formal documents — test scripts, CM system exports, delivery records, and certificates of compliance are all evidence.

## Additional resources

- CEM (ISO/IEC 18045) — evaluation input task and evidence management requirements.
- CC Part 3 — SAR component structure and evidence requirements (D, C, E elements).
- Scheme-specific ETR templates — many schemes provide ETR templates that include evidence index sections.

## Related articles

- [Evaluation Evidence](./EvaluationEvidence.md)
- [Evaluation Technical Report](./EvaluationTechnicalReport.md)
- [Evaluation Methods](./EvaluationMethods.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
- [Observation Report](./ObservationReport.md)
- [Security Target](./SecurityTarget.md)
