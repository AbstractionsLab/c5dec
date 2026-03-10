---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: single-assurance, evaluation, EAL, standard-evaluation
---

# Single-assurance evaluation

**Acronym:** None

The **Single-Assurance Evaluation** is the standard and most common CC evaluation approach. It assumes that the entire [Target of Evaluation (TOE)](./TargetofEvaluation.md) is evaluated against a single, uniform set of [Security Assurance Requirements (SARs)](./SecurityAssuranceRequirement.md), typically expressed as an [Evaluation Assurance Level (EAL)](./EvaluationAssuranceLevel.md). All parts of the [TOE Security Functionality (TSF)](./TOESecurityFunctionality.md) are subject to the same depth and rigour of evaluation — the same level of design documentation, the same testing depth, and the same vulnerability analysis apply uniformly.

This is in contrast to [multi-assurance evaluation](./MultiAssuranceEvaluation.md), where different parts of the TOE (sub-TOEs) may be evaluated at different assurance levels.

## When to use single-assurance evaluation

Single-assurance evaluation is appropriate when:

1. **The TOE is homogeneous in security criticality.** All parts of the TSF face similar threat levels and protect assets of comparable value.
2. **The TOE architecture does not lend itself to decomposition.** The TSF is tightly integrated, and separating it into [sub-TOEs](./SubTOESecurityFunctionality.md) would be artificial or architecturally unsound.
3. **Regulatory or scheme requirements mandate a single EAL.** Many [Protection Profiles](./ProtectionProfile.md) and certification schemes specify a single EAL for the product category.
4. **Simplicity is preferred.** Single-assurance evaluation has lower management overhead and is well understood by evaluators, developers, and certification bodies.

## Evaluation process

A single-assurance evaluation follows the standard CC/CEM process:

1. **Security Target review (ASE).** The evaluator assesses the completeness and consistency of the [Security Target](./SecurityTarget.md), including the [security problem definition](./SecurityProblemdefinition.md), [security objectives](./SecurityObjective.md), [SFRs](./SecurityFunctionalRequirement.md), SARs, and [rationale](./Rationale.md).

2. **Development evidence review (ADV).** The evaluator reviews design documentation at the detail level required by the selected EAL. See [Evaluation Evidence](./EvaluationEvidence.md) for the evidence required at each level.

3. **Guidance review (AGD).** The evaluator verifies that operational and preparative guidance is adequate for secure operation.

4. **Life-cycle support review (ALC).** The evaluator assesses the developer's configuration management, delivery procedures, development security, and flaw remediation processes.

5. **Testing (ATE).** The evaluator reviews developer tests and performs independent testing to verify that the TSF behaves as specified.

6. **Vulnerability assessment (AVA).** The evaluator performs vulnerability analysis and penetration testing appropriate for the [attack potential](./AttackPotential.md) level associated with the selected EAL.

All of these activities apply to the entire TSF at a uniform level. The results are documented in the [Evaluation Technical Report (ETR)](./EvaluationTechnicalReport.md).

## Practical guidance

### Selecting the assurance level

1. **Assess the threat environment.** Determine the expected attacker profile — what expertise, resources, and motivation are assumed? Map this to attack potential levels and corresponding AVA_VAN components.

2. **Consider the product category.** Review applicable [Protection Profiles](./ProtectionProfile.md) and scheme guidance for recommended EALs. Certification schemes like [EUCC](./EUCC.md) map product categories to assurance levels.

3. **Balance effort against value.** Higher EALs require exponentially more development evidence and evaluation effort. Ensure the selected EAL is proportionate to the security risk:
   - **EAL1-2:** Suitable for products with low threat exposure or where independent confirmation of basic security is sufficient.
   - **EAL3-4:** Suitable for products in regulated environments or where moderate confidence in security engineering is required.
   - **EAL5-7:** Suitable for high-security products in government, defence, or critical infrastructure contexts.

4. **Consider augmentation.** If only one assurance area needs strengthening (e.g., vulnerability analysis for a network-facing product), augment the base EAL rather than moving to a higher level. See [Package](./Package.md).

### Comparison with multi-assurance

| Aspect | Single-assurance | Multi-assurance |
|---|---|---|
| SAR selection | One set of SARs for the entire TOE | Different SARs per [sub-TOE](./SubTOESecurityFunctionality.md) |
| Evidence requirements | Uniform across all TSF | Varies by sub-TOE |
| Evaluation complexity | Lower | Higher (requires sub-TOE decomposition, inter-sub-TOE analysis) |
| Applicable when | TOE is homogeneous in criticality | TOE has parts with significantly different security criticality |
| PP compatibility | Compatible with all PPs | Only compatible with PPs that permit multi-assurance |

### Tips for developers

- **Prepare evidence uniformly.** In a single-assurance evaluation, all TSF components need the same level of documentation. Do not provide detailed design for one module and skip another — evaluators will note the inconsistency.
- **Plan testing comprehensively.** Test coverage must span all TSFIs and, at higher EALs, all TSF subsystems. Identify all interfaces early in the development process.
- **Align with guidance requirements.** Operational guidance must cover the entire evaluated configuration, not just security-critical functions.

## Additional resources

- CC 2022 Part 1, Section 7 — standard evaluation approach and evaluation process.
- CC Part 3, Section 7 — EAL definitions (EAL1-EAL7).
- CEM (ISO/IEC 18045) — evaluator methodology for all assurance activities.

## Related articles

- [Multi-Assurance Evaluation](./MultiAssuranceEvaluation.md)
- [Evaluation Assurance Levels](./EvaluationAssuranceLevel.md)
- [Evaluation Methods](./EvaluationMethods.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
- [Attack Potential](./AttackPotential.md)
- [Package](./Package.md)
- [Evaluation Evidence](./EvaluationEvidence.md)
- [Security Target](./SecurityTarget.md)
