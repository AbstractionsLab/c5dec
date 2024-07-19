---
Last Updated: October 4, 2023
Relevant CC Version: CC2022
---

# Protection Profile

**Acronym:** PP

A Protection Profile is typically a statement of need where a user community, a regulatory entitiy, or a group of developers define a common set of security needs. A PP gives consumers a menas of referring to this set and facilitates future evaluation against these needs.
Although this does not preclude other uses, a PP is typically used as:
- part of a requirement specification for a specific consumer or group of consumers, who will only consider buying a specific type of IT product if it meets the PP;
- part of a regulation from a specific regulatory entity, who will only allow a specific type of IT product to be used if it meets the PP;
- to address a common security problem presented by a variety of consumers, and often defined by a group including several IT product developers, who then produce IT products of this type in order to meet the needs of their common market.

Two types of PPs:
- [Single-assurance Evaluation](./Single-assuranceEvaluation.md): evaluation of a TOE using one set of [assurance requirements](./SecurityAssuranceRequirement.md)
- [Multi-assurance Evaluation](./Multi-assuranceEvaluation.md): evaluation of a TOE using a PP-Configuration where each PP-Configuration component is associated with its own set of assurance requirements.

PPs can be defined using the [direct rationale](./DirectRationale.md) approach or the standard approach.

## Collaborative Protection Profiles
A collaborative Protection Profile (cPP) is a specialized protection profile developed by an international technical community within a particular technical domain. It defines security requirements and an evaluation methodology specific to that domain, allowing for consistent and recognized security evaluations and certifications in that area of expertise. The refined or specifically applicable evaluation methods within the cPP are defined in supporting documents and published individually.
According to the German certification scheme , certification of a product according to a cPP under the recognition of the CCRA must maintain exact conformance. This means that the security requirements for the product certification process should not deviate from the cPP, neither in terms of functional security requirements nor testing requirements, even if the IT product provides higher security performance. In addition, the CCRA Supporting Documents associated with the cPP, which refine the evaluation methodology of the CEM in a technology-specific manner, must be applied. These documents can be found on the Common Criteria portal under the section "Collaborative PPs." Security features that go beyond the scope of the cPP can be granted in a second certificate as part of the same evaluation process, using the Re-Use processes. This certificate is either not recognized by the CCRA or is not compliant with the cPP and is recognized by the CCRA up to EAL 2.

## Practical Guidance

COMING SOON.

## Document Outline

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
3.  [Conformance Statement](ConformanceStatement.md)
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

## Document Template

COMING SOON.