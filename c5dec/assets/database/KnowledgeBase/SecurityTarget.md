---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: security-target, ST, evaluation, conformance, security-requirements
---

# Security Target

**Acronym:** ST

A ST is a document that describes a specific [TOE](./TargetofEvaluation.md), the [conformance claims](./ConformanceClaim.md) applicable to the evaluation of the TOE, the [security problem](./SecurityProblemdefinition.md) to be addressed, the [security objectives](./SecurityObjective.md) for the TOE and its operational environment, the [security requirements](./SecurityFunctionalRequirement.md) applicable to solving the stated security problem, and additional material necessary to describe the TOE sufficiently for evaluation. STs are generally based upon [PPs](./ProtectionProfile.md) or [PP-Configurations](./PPConfiguration.md) that describe a security problem and security requirements for a TOE type that is relevant to the specific TOE, but can also be defined as standalone documents.
A ST is typically produced by a developer and the audience for the ST includes evaluators, the certification body, and end users of the evaluated TOE.

STs can be evaluated according to:
- [Single-Assurance Evaluation](./SingleAssuranceEvaluation.md): evaluation of a TOE using one set of [assurance requirements](./SecurityAssuranceRequirement.md).
- [Multi-Assurance Evaluation](./MultiAssuranceEvaluation.md): evaluation of a TOE using a PP-Configuration where each PP-Configuration component is associated with its own set of assurance requirements.

A ST can either adopt the [direct rationale](./DirectRationale.md) model or the standard model.

## Practical guidance

### Reading a Security Target

1. **Start with the ST Introduction.** The [TOE Reference](./TOEReference.md) identifies the exact product version; the [TOE Overview](./TOEOverview.md) gives a high-level description of what the product does; the [TOE Description](./TOEDescription.md) details the physical and logical boundaries of the TOE, including any non-TOE components in the operational environment.
2. **Check the Conformance Claims.** Determine which [PP](./ProtectionProfile.md) or [PP-Configuration](./PPConfiguration.md) the ST claims conformance to and what conformance type applies ([exact](./Exactconformance-FAQ.md), strict, or [demonstrable](./ConformanceStatement.md)). If no PP is claimed, the ST is standalone.
3. **Understand the Security Problem Definition.** Read the [threats](./Threat.md), [OSPs](./OrganizationalSecurityPolicy.md), and [assumptions](./Assumption.md). Verify these are realistic for the product's intended deployment.
4. **Trace Security Objectives.** The [security objectives](./SecurityObjective.md) for the TOE and its [operational environment](./TOEOperationalEnvironment.md) must address every threat, OSP, and assumption. The [rationale](./Rationale.md) should clearly explain each mapping.
5. **Review SFRs.** Check which [functional requirements](./SecurityFunctionalRequirement.md) are selected and how [operations](./Operations.md) are completed. Compare against the claimed PP to find any additions or refinements.
6. **Examine the TOE Summary Specification.** The [TSS](./TOESummarySpecification.md) maps each SFR to the TOE's actual implementation mechanisms. This is often the most valuable section for understanding how the product works.
7. **Note the assurance level.** The selected [EAL](./EvaluationAssuranceLevel.md) or custom [package](./Package.md) determines the rigour of evidence required.

### Writing a Security Target

1. **Identify the claimed PP(s).** If the target market or certification scheme requires conformance to a PP, obtain the PP and ensure its requirements drive the ST structure. For standalone STs, define the security problem independently.
2. **Draft the TOE description.** Clearly delineate the [TOE boundary](./TOEBoundary.md) — what is inside the TOE, what is in the operational environment, and what interfaces cross the boundary. Use diagrams to illustrate the physical and logical scope.
3. **Build the Security Problem Definition.** Identify [threats](./Threat.md), [OSPs](./OrganizationalSecurityPolicy.md), and [assumptions](./Assumption.md) through threat modelling and stakeholder analysis. Ensure completeness by considering all [assets](./Asset.md), threat agents, and attack vectors relevant to the product.
4. **Derive Security Objectives and SFRs.** Map every SPD element to [objectives](./SecurityObjective.md), then select [SFRs](./SecurityFunctionalRequirement.md) that realise each objective. Complete all [operations](./Operations.md) (assignment, selection, refinement, iteration) on each SFR component. Provide a traceable [rationale](./Rationale.md) at each mapping step.
5. **Write the TOE Summary Specification.** For each SFR, describe the specific implementation mechanism in the TOE that satisfies the requirement. Evaluators use this for ADV and ATE work.
6. **Choose the direct rationale model when appropriate.** If a standalone ST omits formal security objectives, adopt [direct rationale](./DirectRationale.md) and map the SPD directly to SFRs with per-SFR justification.
7. **Select SARs.** Choose an [EAL](./EvaluationAssuranceLevel.md) or custom [package](./Package.md). Consider augmenting specific components (e.g., AVA_VAN.3 at EAL 2) where the threat environment demands extra assurance.
8. **Review and iterate.** Before submitting for evaluation, verify that every SPD element is addressed, every SFR is traced to an objective (or directly to the SPD), and every SFR is mapped by the TSS. Use the certification body's ST checklist when available.

> **Tip:** Many certification schemes publish ST templates or exemplary STs. Consulting these avoids common structural mistakes and speeds up evaluator review.

## Document outline

1.  [ST Introduction]
    1.  [ST Reference]
    2.  [TOE Reference](./TOEReference.md)
    3.  [TOE Overview](./TOEOverview.md)
    4.  [TOE Description](./TOEDescription.md)
2.  [Conformance Claims](./ConformanceClaim.md)
    1.  CC Claim
    2.  Package Claim
    3.  PP Claim
    4.  Conformance Claim rationale
        1.  TOE Type consistency
        2.  SPD Consistency
        3.  SO Consistency
        4.  SR Consistency
    5.  [Evaluation Methods](./EvaluationMethods.md)
3.  [Security Problem Definition](./SecurityProblemdefinition.md)
    1.  [Threats](./Threat.md)
    2.  [Organizational Security Policies](./OrganizationalSecurityPolicy.md)
    3.  [Assumptions](./Assumption.md)
4.  [Security Objectives](./SecurityObjective.md)
    1.  [Security Objectives for the TOE]
    2.  [Security Objectives for the Operational Environment]
    3.  [Security Objectives Rationale](./Rationale.md)
4.  [Extended Component Definition](./ExtendedComponentDefinition.md)
5.  Security Requirements
    1.  [Security Functional Requirements](./SecurityFunctionalRequirement.md)
    2.  [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
    3.  [Security Requirements Rationale](./Rationale.md)
6.  [TOE Summary Specification](./TOESummarySpecification.md)

## Additional resources

- CC 2022 Part 1, Section 7 and Annex B — ST structure and content.
- CC Part 3, ASE class — evaluator actions for ST evaluation.
- ISO/IEC TR 15446 — guide for the production of PPs and STs.
- CEM, Section 12 (ASE activities) — detailed evaluation sub-activities for each ASE family.

## Related articles

- [Protection Profile](./ProtectionProfile.md)
- [TOE Description](./TOEDescription.md)
- [TOE Summary Specification](./TOESummarySpecification.md)
- [Conformance Claim](./ConformanceClaim.md)
- [Security Problem Definition](./SecurityProblemdefinition.md)
- [Security Objectives](./SecurityObjective.md)
- [Rationale](./Rationale.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [Evaluation Assurance Levels](./EvaluationAssuranceLevel.md)
- [Direct Rationale](./DirectRationale.md)

