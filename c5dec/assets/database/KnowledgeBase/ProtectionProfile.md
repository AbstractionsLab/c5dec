---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: protection-profile, PP, cPP, collaborative-PP, security-requirements
---

# Protection Profile

**Acronym:** PP

A Protection Profile is typically a statement of need where a user community, a regulatory entity, or a group of developers define a common set of security needs. A PP gives consumers a means of referring to this set and facilitates future evaluation against these needs.
Although this does not preclude other uses, a PP is typically used as:
- part of a requirement specification for a specific consumer or group of consumers, who will only consider buying a specific type of IT product if it meets the PP;
- part of a regulation from a specific regulatory entity, who will only allow a specific type of IT product to be used if it meets the PP;
- to address a common security problem presented by a variety of consumers, and often defined by a group including several IT product developers, who then produce IT products of this type in order to meet the needs of their common market.

Two types of PPs:
- [Single-Assurance Evaluation](./SingleAssuranceEvaluation.md): evaluation of a TOE using one set of [assurance requirements](./SecurityAssuranceRequirement.md)
- [Multi-Assurance Evaluation](./MultiAssuranceEvaluation.md): evaluation of a TOE using a PP-Configuration where each PP-Configuration component is associated with its own set of assurance requirements.

PPs can be defined using the [direct rationale](./DirectRationale.md) approach or the standard approach.

## Collaborative Protection Profiles
A collaborative Protection Profile (cPP) is a specialized protection profile developed by an international technical community within a particular technical domain. It defines security requirements and an evaluation methodology specific to that domain, allowing for consistent and recognized security evaluations and certifications in that area of expertise. The refined or specifically applicable evaluation methods within the cPP are defined in supporting documents and published individually.
According to the German certification scheme , certification of a product according to a cPP under the recognition of the CCRA must maintain exact conformance. This means that the security requirements for the product certification process should not deviate from the cPP, neither in terms of functional security requirements nor testing requirements, even if the IT product provides higher security performance. In addition, the CCRA Supporting Documents associated with the cPP, which refine the evaluation methodology of the CEM in a technology-specific manner, must be applied. These documents can be found on the Common Criteria portal under the section "Collaborative PPs." Security features that go beyond the scope of the cPP can be granted in a second certificate as part of the same evaluation process, using the Re-Use processes. This certificate is either not recognized by the CCRA or is not compliant with the cPP and is recognized by the CCRA up to EAL 2.

## Practical guidance

### Reading a Protection Profile

1. **Begin with the PP introduction and TOE overview.** Understand the product category targeted, the intended operational environment, and the security problem the PP addresses. This sets context for all subsequent sections.
2. **Review the conformance statement.** Determine whether the PP requires [exact](./Exactconformance-FAQ.md), strict, or [demonstrable conformance](./ConformanceStatement.md). This dictates how much flexibility an ST author has when claiming conformance.
3. **Study the security problem definition.** Identify the [threats](./Threat.md), [OSPs](./OrganizationalSecurityPolicy.md), and [assumptions](./Assumption.md). Assess whether these match the actual threat landscape for the intended deployment.
4. **Examine the SFR selection.** Understand which [functional requirements](./SecurityFunctionalRequirement.md) the PP mandates. Pay attention to which [operations](./Operations.md) are completed by the PP (fixed values) and which are left to the ST author (open assignments/selections).
5. **Check SAR requirements.** Identify the required [assurance level](./EvaluationAssuranceLevel.md) or specific SAR components. This determines the [evaluation evidence](./EvaluationEvidence.md) effort.
6. **Note any PP-Module or PP-Configuration context.** Some PPs are designed as base PPs for modular extension. Check whether [PP-Modules](./PPModule.md) exist for the product's specific capabilities.

### Writing a Protection Profile

1. **Define the product category.** Clearly describe the type of IT product the PP targets. The scope should be broad enough to be useful across products but narrow enough to be meaningful.
2. **Engage stakeholders.** Involve user communities, regulatory bodies, and developers in the requirements definition process. PPs that represent genuine market needs gain broader adoption.
3. **Develop the security problem definition.** Systematically identify threats, OSPs, and assumptions following the guidance in [Security Problem Definition](./SecurityProblemdefinition.md). Validate against real-world threat intelligence for the product category.
4. **Derive security objectives.** Map the SPD to [security objectives](./SecurityObjective.md) for both the TOE and its [operational environment](./TOEOperationalEnvironment.md), providing a clear [rationale](./Rationale.md) for each mapping.
5. **Select SFRs.** Choose [functional components](./SecurityFunctionalRequirement.md) from CC Part 2 (or define [extended components](./ExtendedComponentDefinition.md)) that fulfil each security objective. Complete or constrain operations where the PP wants to mandate specific values; leave operations open where implementer flexibility is appropriate.
6. **Define the conformance statement.** Choose the conformance type:
   - **Exact conformance** — ST must include exactly the PP's SFRs (standard for cPPs and [EUCC](./EUCC.md)).
   - **Strict conformance** — ST must include all PP SFRs and may add more.
   - **Demonstrable conformance** — ST must demonstrate equivalence to the PP's security requirements.
7. **Select SARs.** Choose an [EAL](./EvaluationAssuranceLevel.md) or custom assurance [package](./Package.md) appropriate for the threat environment. Consider augmentation if specific assurance areas need strengthening.
8. **Subject the PP to evaluation.** PPs themselves can be evaluated under the APE assurance class, providing third-party confidence in the PP's completeness and consistency.

> **CC 2022 note:** CC 2022 formalises PP-Modules, [PP-Configurations](./PPConfiguration.md), and their interaction with exact conformance. PP authors should consider whether a modular PP architecture is appropriate for the product domain.

## Document outline

1. [PP Introduction]
    1. PP Reference
    2. [TOE Overview](./TOEOverview.md)
2. [Conformance Claims](./ConformanceClaim.md)
    1.  CC Claim
    2.  Package Claim
    3.  PP Claim
    4.  Conformance Claim rationale
        1.  TOE Type consistency
        2.  SPD Consistency
        3.  SO Consistency
        4.  SR Consistency
3.  [Conformance Statement](./ConformanceStatement.md)
    1.  [Allowed-with Statement]
    2.  [Evaluation Methods](./EvaluationMethods.md)
4.  [Security Objectives](./SecurityObjective.md)
    1.  [Security Objectives for the TOE]
    2.  [Security Objectives for the Operational Environment]
    3.  [Security Objectives Rationale](./Rationale.md)
4.  [Extended Component Definition](./ExtendedComponentDefinition.md)
5.  Security Requirements
    1.  [Security Functional Requirements](./SecurityFunctionalRequirement.md)
    2.  [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
    3.  [Security Requirements Rationale](./Rationale.md)

## Additional resources

- CC 2022 Part 1, Section 6 and Annex A — PP structure and content.
- CC 2022 Part 1, Annex D — PP-Module and PP-Configuration rules.
- CC Part 3, APE class — evaluator actions for PP evaluation.
- CCRA Portal — repository of certified PPs and cPPs.
- ISO/IEC TR 15446 — guide for the production of PPs and STs.

## Related articles

- [Security Target](./SecurityTarget.md)
- [PP-Configuration](./PPConfiguration.md)
- [PP-Module](./PPModule.md)
- [Conformance Claim](./ConformanceClaim.md)
- [Conformance Statement](./ConformanceStatement.md)
- [Security Problem Definition](./SecurityProblemdefinition.md)
- [Security Objectives](./SecurityObjective.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [Evaluation Assurance Levels](./EvaluationAssuranceLevel.md)
- [EUCC](./EUCC.md)