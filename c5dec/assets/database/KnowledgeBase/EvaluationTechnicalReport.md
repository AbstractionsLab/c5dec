---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: evaluation-technical-report, ETR, ITSEF, certification-body
---

# Evaluation Technical Report

**Acronym:** ETR

The Evaluation Technical Report (ETR) is the primary deliverable produced by the evaluation facility (ITSEF / CCTL) at the conclusion of a CC evaluation. It documents the evaluator's findings, verdicts, and rationale for each assurance component, providing the certification body with the evidence needed to make a certification decision.

## Definition

The ETR records the results of all evaluation activities performed under the CEM (Common Evaluation Methodology). For each [SAR](./SecurityAssuranceRequirement.md) component in the [Security Target](./SecurityTarget.md), the evaluator documents:
- The evidence examined.
- The work units performed.
- The verdict (pass, fail, or inconclusive) with justification.
- Any [Observation Reports](./ObservationReport.md) raised during the evaluation.

The ETR also includes an overall evaluation verdict and a recommendation to the certification body.

## Structure

A typical ETR contains:

| Section | Content |
|---------|---------|
| **Introduction** | Evaluation identifiers, ST reference, TOE identification, evaluation dates, and ITSEF details. |
| **TOE description** | Summary of the [TOE](./TargetofEvaluation.md), its [boundaries](./TOEBoundary.md), and evaluated configuration. |
| **Evaluation approach** | Methodology references (CEM version, scheme-specific guidance, supporting documents for cPPs). |
| **Per-component results** | For each SAR component: evidence reviewed, work units, verdicts, and findings. |
| **Vulnerability analysis results** | Detailed AVA_VAN findings including attack potential calculations and penetration test results. |
| **Observation Reports** | Summary of all ORs raised, their dispositions, and impact on verdicts. |
| **Overall verdict** | The evaluator's overall pass/fail determination and certification recommendation. |

## Practical guidance

### For evaluators

1. **Write verdicts as you go.** Document findings for each work unit during the evaluation, not after. This ensures accuracy and completeness.
2. **Provide sufficient rationale.** Each verdict must be justified with enough detail for the certification body to independently assess the finding. "Pass" without explanation is insufficient.
3. **Link to evidence.** Reference specific sections of the developer's [evaluation evidence](./EvaluationEvidence.md) using the [Evidence Index](./EvaluationEvidenceIndex.md) identifiers.
4. **Document negative findings clearly.** For failed work units, explain what was expected, what was found, and why the gap constitutes a failure.

### For developers

1. **The ETR is not publicly released.** It is a confidential document between the ITSEF and the certification body. However, specific findings may be communicated to the developer via [Observation Reports](./ObservationReport.md).
2. **Prepare evidence with the ETR structure in mind.** Organizing evaluation evidence to match the SAR component structure makes the evaluator's task easier, which typically results in fewer ORs and a smoother evaluation.

## Additional resources

- CEM, Section 5 -- ETR structure and content requirements.
- ISO/IEC 18045 -- Common Evaluation Methodology.
- Scheme-specific ETR templates (BSI, ANSSI, NSCIB, etc.).

## Related articles

- [Observation Report](./ObservationReport.md)
- [Evaluation Evidence](./EvaluationEvidence.md)
- [Evaluation Evidence Index](./EvaluationEvidenceIndex.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
- [Evaluation Assurance Levels](./EvaluationAssuranceLevel.md)
- [Security Target](./SecurityTarget.md)
