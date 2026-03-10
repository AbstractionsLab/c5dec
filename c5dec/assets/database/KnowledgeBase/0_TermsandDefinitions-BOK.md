---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: glossary, terms, definitions, body-of-knowledge
---

# Terms and definition register

This register provides concise definitions of key Common Criteria terms. Each entry links to the corresponding Knowledge Base article for detailed guidance. Terms are sourced primarily from CC 2022 Part 1, with notes where CC 3.1 R5 differs.

## A

- **Asset** — An item or information of value requiring protection from threats. See [Asset](./Asset.md).
- **Assignment (operation)** — CC operation that fills in a specification-identified parameter with a specific value. See [Assignment](./Operation-Assignment.md).
- **Assumption** — A statement about the TOE operational environment taken to be true during evaluation. See [Assumption](./Assumption.md).
- **Attack potential** — A measure of the effort required to exploit a vulnerability, based on expertise, resources, and motivation. See [Attack Potential](./AttackPotential.md).
- **Assurance** — Grounds for confidence that a TOE meets its security objectives.
- **Assurance class** — A grouping of assurance families sharing a common focus (e.g., development, testing, vulnerability analysis).
- **Assurance component** — A specific set of assurance requirements within an assurance family.
- **Assurance family** — A grouping of assurance components addressing a specific aspect of assurance.
- **Assurance package** — A defined set of assurance components, typically an EAL or an augmented EAL. See [Package](./Package.md).
- **Augmentation** — The addition of one or more assurance components from a different assurance family to an assurance package.

## B

- **Base component** — In a composed TOE, the component upon which another component relies for services. See [Composed TOE](./ComposedTOE.md).
- **Base Protection Profile** — A PP used as the foundation in a PP-Configuration. See [PP-Configuration](./PPConfiguration.md).

## C

- **CC** — Common Criteria for Information Technology Security Evaluation (ISO/IEC 15408).
- **CEM** — Common Evaluation Methodology (ISO/IEC 18045). The companion methodology document used by evaluators.
- **Composed TOE** — A TOE comprising two or more IT components evaluated separately that are combined into a single product. See [Composed TOE](./ComposedTOE.md).
- **Composite evaluation** — An evaluation of a composed TOE that reuses evaluation results of individual components. See [Composite Evaluation](./CompositeEvaluation.md).
- **Conformance claim** — A statement in an ST or PP declaring how the TOE conforms to one or more PPs and packages. See [Conformance Claim](./ConformanceClaim.md).
- **Conformance statement** — The type of conformance required by a PP (exact, strict, or demonstrable). See [Conformance Statement](./ConformanceStatement.md).

## D

- **Demonstrable conformance** — A conformance type where the ST must demonstrate equivalence to PP requirements without textual identity. See [Conformance Statement](./ConformanceStatement.md).
- **Dependent component** — In a composed TOE, the component that relies on services from the base component. See [Composed TOE](./ComposedTOE.md).
- **Direct rationale** — A rationale approach that justifies SFR selection directly without deriving from security objectives. See [Direct Rationale](./DirectRationale.md).
- **Domain separation** — A TSF architectural property ensuring isolation between the TSF domain and other domains. See [Domain Separation](./DomainSeparation.md).

## E

- **EAL** — Evaluation Assurance Level, a predefined package of assurance components (EAL1 through EAL7). See [Evaluation Assurance Levels](./EvaluationAssuranceLevel.md).
- **EUCC** — European Common Criteria-based cybersecurity certification scheme under the EU Cybersecurity Act. See [EUCC](./EUCC.md).
- **Evaluation evidence** — Documentation and other artefacts submitted by a developer or sponsor for evaluation. See [Evaluation Evidence](./EvaluationEvidence.md).
- **Evaluation Technical Report (ETR)** — The report produced by evaluators documenting findings, verdicts, and results. See [Evaluation Technical Report](./EvaluationTechnicalReport.md).
- **Exact conformance** — A conformance type requiring that the ST includes all SFRs and SARs from the PP without modification, except by permitted operations. See [Exact Conformance FAQ](./Exactconformance-FAQ.md).
- **Extended component** — A security component not found in CC Part 2 or Part 3, defined by the ST or PP author. See [Extended Component Definition](./ExtendedComponentDefinition.md).

## F

- **Functional class** — A grouping of functional families sharing a common security focus (e.g., FDP for user data protection).
- **Functional component** — A specific set of security functional requirements within a functional family.
- **Functional family** — A grouping of functional components addressing a specific security service.
- **Functional package** — A named set of functional components intended for reuse across PPs or STs. See [Package](./Package.md).

## I

- **Iteration (operation)** — CC operation that allows a component to be used more than once with varying operations. See [Iteration](./Operation-Iteration.md).

## M

- **Multi-assurance evaluation** — An evaluation where different parts of the TOE are evaluated at different assurance levels. See [Multi-Assurance Evaluation](./MultiAssuranceEvaluation.md).

## N

- **Non-bypassability** — A TSF architectural property ensuring that security enforcement functions cannot be circumvented. See [Non-Bypassability](./NonBypassability.md).
- **Non-TSF part** — Portions of the TOE that are outside the TSF and do not enforce security policy. See [Non-TSF Part](./NonTSFPart.md).

## O

- **Observation Report (OR)** — A document raised by evaluators to record issues found during evaluation. See [Observation Report](./ObservationReport.md).
- **Organizational Security Policy (OSP)** — A set of security rules imposed by an organization on the TOE. See [Organizational Security Policy](./OrganizationalSecurityPolicy.md).

## P

- **PP** — Protection Profile, an implementation-independent set of security requirements for a category of TOEs. See [Protection Profile](./ProtectionProfile.md).
- **PP-Configuration** — A combination of a base PP with one or more PP-Modules. See [PP-Configuration](./PPConfiguration.md).
- **PP-Module** — A PP that specifies incremental security requirements and cannot stand alone. See [PP-Module](./PPModule.md).

## R

- **Rationale** — Justification demonstrating that security objectives address the security problem definition and that SFRs meet security objectives. See [Rationale](./Rationale.md).
- **Refinement (operation)** — CC operation that adds detail to a requirement without changing its meaning. See [Refinement](./Operation-Refinement.md).

## S

- **SAR** — Security Assurance Requirement. See [Security Assurance Requirements](./SecurityAssuranceRequirement.md).
- **Security component** — A building block of security requirements, either functional (SFC) or assurance (SAC). See [Security Components](./SecurityComponent.md).
- **Security objective** — A statement of intent to counter identified threats or enforce OSPs. See [Security Objectives](./SecurityObjective.md).
- **Security problem definition (SPD)** — The formal identification of threats, OSPs, and assumptions relevant to the TOE. See [Security Problem Definition](./SecurityProblemdefinition.md).
- **Security Target (ST)** — An implementation-dependent statement of security requirements for a specific TOE. See [Security Target](./SecurityTarget.md).
- **Selection (operation)** — CC operation that narrows a requirement by choosing from a set of options. See [Selection](./Operation-Selection.md).
- **Self-protection** — A TSF architectural property ensuring the TSF can resist tampering and maintain integrity. See [Self-Protection](./SelfProtection.md).
- **SFR** — Security Functional Requirement. See [Security Functional Requirements](./SecurityFunctionalRequirement.md).
- **Single-assurance evaluation** — An evaluation where the entire TOE is evaluated at a single assurance level. See [Single-Assurance Evaluation](./SingleAssuranceEvaluation.md).
- **Strict conformance** — A conformance type where the ST must include all PP requirements and may add more. See [Conformance Statement](./ConformanceStatement.md).
- **Sub-TOE** — A defined part of a TOE subject to its own assurance level in a multi-assurance evaluation. See [Sub-TOE Security Functionality](./SubTOESecurityFunctionality.md).

## T

- **Threat** — A potential for a threat agent to exercise a threat action against an asset. See [Threat](./Threat.md).
- **Threat agent** — An entity that can adversely act on assets.
- **TOE** — Target of Evaluation, the product or system subject to evaluation. See [Target of Evaluation](./TargetofEvaluation.md).
- **TOE boundary** — The demarcation separating TOE components from the operational environment. See [TOE Boundary](./TOEBoundary.md).
- **TOE security functionality (TSF)** — The combined set of all hardware, software, and firmware within the TOE that enforces security policy. See [TOE Security Functionality](./TOESecurityFunctionality.md).
- **TSFI** — TSF Interface, a means by which external entities interact with the TSF. See [TSF Interface](./TSFInterface.md).
- **TSS** — TOE Summary Specification, a description of how the TOE meets each SFR. See [TOE Summary Specification](./TOESummarySpecification.md).

## W

- **Work unit** — The smallest evaluator task defined by the CEM, corresponding to an evaluator action element.

## Related articles

- [Map of Content](./0_MapofContent.md)
- [Security Components](./SecurityComponent.md)
- [Evaluation Methods](./EvaluationMethods.md)
