---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: observation-report, OR, evaluation-finding, evaluation-process, ITSEF
---

# Observation report

**Acronym:** OR

An **Observation Report (OR)** is a formal document raised by evaluators during a Common Criteria [evaluation](./EvaluationMethods.md) to record a finding, issue, or concern about the [TOE](./TargetofEvaluation.md), its documentation, or the evaluation evidence. Observation Reports are the primary mechanism through which evaluators communicate problems to the developer (sponsor) and track the resolution of identified issues. The lifecycle and management of ORs is governed by the evaluation scheme (e.g., [EUCC](./EUCC.md), BSI, ANSSI) and documented in the [Evaluation Technical Report (ETR)](./EvaluationTechnicalReport.md).

## Types of observation reports

Schemes typically classify ORs by severity, though exact terminology varies. A common classification:

| Type | Severity | Impact on evaluation |
|---|---|---|
| **Major OR** | Critical finding that blocks a positive evaluation verdict if unresolved. | The evaluation cannot pass until the finding is addressed. Examples: missing mandatory evidence, a vulnerability that falls below the claimed [attack potential](./AttackPotential.md) threshold, an SFR that is not implemented. |
| **Minor OR** | Non-critical finding that does not block the verdict but should be addressed. | The evaluation may proceed, but the finding is recorded. Examples: editorial issues in guidance documentation, minor inconsistencies in design descriptions. |
| **Informational OR** | Observations that do not affect the verdict but may be useful for improvement. | No action required. Examples: suggestions for improvement, notes on areas reviewed with no findings. |

> Scheme-specific terminology may differ. For example, some schemes use "Problem Report" instead of "Major OR," or distinguish between "non-conformity" and "observation."

## Lifecycle

A typical OR lifecycle:

1. **Identification.** The evaluator identifies an issue during evaluation activities (e.g., while reviewing design documentation, performing penetration testing, analysing test coverage).
2. **Drafting.** The evaluator documents the finding in a formal OR, including:
   - The evaluation activity (CEM work unit) during which the finding was made.
   - A description of the issue.
   - The severity classification.
   - The evidence or artefact affected.
   - The expected behaviour or requirement that is not met.
3. **Submission.** The OR is submitted to the developer (sponsor) and, depending on scheme procedures, to the certification body.
4. **Response.** The developer analyses the OR and provides a response — typically a corrected artefact, updated evidence, or a reasoned rebuttal.
5. **Verification.** The evaluator reviews the developer's response and verifies that the issue is resolved.
6. **Closure.** The OR is closed once the evaluator is satisfied with the resolution. The closure status (resolved, not applicable, deferred) is documented.
7. **Reporting.** All ORs, their resolutions, and outstanding issues are summarised in the [ETR](./EvaluationTechnicalReport.md).

## Impact on evaluation verdict

The evaluation verdict is directly influenced by OR status:

- **Pass:** All mandatory evaluator actions yield a positive result, all major ORs are closed.
- **Fail:** One or more major ORs remain unresolved and cannot be mitigated.
- **Inconclusive:** The evaluator cannot determine a verdict due to insufficient evidence; this may generate ORs requesting additional evidence.

## Practical guidance

### For developers (sponsors)

1. **Respond promptly.** OR resolution timelines are scheme-dependent but typically measured in weeks. Delays in response extend the evaluation schedule.
2. **Address the root cause.** When correcting an issue, address the underlying problem, not just the specific instance. Evaluators may check for similar issues elsewhere.
3. **Provide clear evidence.** Include corrected documents, test results, or design updates with your response. Reference the specific OR number and quote the finding.
4. **Track OR status.** Maintain an internal log of all ORs, their status, and resolution actions. This supports project management and avoids re-opening closed issues.

### For evaluators (ITSEFs)

1. **Be precise in findings.** Clearly state which CEM work unit, which evidence artefact, and which specific requirement or criterion is not met. Vague ORs lead to misunderstandings and delays.
2. **Classify severity accurately.** Over-classifying minor issues as major generates unnecessary work; under-classifying genuine problems risks a flawed evaluation.
3. **Document resolution thoroughly.** When closing an OR, record the resolution method and verify that the corrected evidence is consistent with the rest of the evaluation.
4. **Summarise in the ETR.** The ETR must include a summary of all ORs raised, their resolutions, and any outstanding observations.

## Additional resources

- CEM (ISO/IEC 18045) — evaluation process and evaluator responsibilities regarding findings.
- Scheme-specific OR management procedures (e.g., EUCC scheme rules, BSI AIS, ANSSI certification procedures).
- CC Part 1, Section 12 — evaluation results and verdicts.

## Related articles

- [Evaluation Methods](./EvaluationMethods.md)
- [Evaluation Technical Report](./EvaluationTechnicalReport.md)
- [Evaluation Evidence](./EvaluationEvidence.md)
- [Attack Potential](./AttackPotential.md)
- [EUCC](./EUCC.md)
- [Security Target](./SecurityTarget.md)
