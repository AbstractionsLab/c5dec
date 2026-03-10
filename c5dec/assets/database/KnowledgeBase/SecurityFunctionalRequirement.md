---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: SFR, functional-requirement, functional-class, functional-family, functional-component, CC-Part-2
---

# Security functional requirement

**Acronym:** SFR

A **Security Functional Requirement (SFR)** is a translation of a [security objective](./SecurityObjective.md) for the [TOE](./TargetofEvaluation.md) into a standardised, technically precise statement of what the TOE's security functions must achieve. SFRs are expressed using the functional [security components](./SecurityComponent.md) catalogued in CC Part 2, possibly augmented with [extended components](./ExtendedComponentDefinition.md). Each SFR specifies a particular security behaviour that the [TOE security functionality (TSF)](./TOESecurityFunctionality.md) must enforce at runtime.

SFRs form the core of both [Protection Profiles](./ProtectionProfile.md) and [Security Targets](./SecurityTarget.md), and are the primary basis against which the TSF implementation is verified during evaluation.

## Hierarchical structure

CC Part 2 organises functional requirements into a three-level hierarchy:

### Functional classes

A functional class groups families that share a common security focus. CC 2022 defines 11 functional classes:

| Class | Name | Security focus |
|-------|------|----------------|
| FAU | Security audit | Audit data generation, review, storage, and accountability |
| FCO | Communication | Non-repudiation of origin and receipt |
| FCS | Cryptographic support | Key management and cryptographic operations |
| FDP | User data protection | Access control, information flow, data integrity and confidentiality |
| FIA | Identification and authentication | User identity verification and binding |
| FMT | Security management | Management of TSF functions, data, roles, and attributes |
| FPT | Protection of the TSF | Integrity, state management, and internal data protection |
| FRU | Resource utilisation | Fault tolerance, resource allocation, and service priority |
| FTA | TOE access | Session management, banners, concurrent session limits |
| FTP | Trusted path/channels | Secure communication between TSF and remote entities or users |
| FPR | Privacy | Anonymity, pseudonymity, unlinkability, and unobservability |

### Functional families

Each class contains one or more families. A family addresses a specific security service within its class (e.g., FDP_ACC — access control policy, FDP_IFC — information flow control policy). Families also define management requirements and audit events applicable to their components.

### Functional components

A component is the smallest selectable unit of functional requirements. Components within a family are often hierarchically ordered, where a higher component provides strictly more security functionality than a lower one. A component consists of one or more **functional elements**, which are the indivisible requirements.

**Dependencies:** Components may declare dependencies on other components. If an SFR is selected, all its dependencies must also be satisfied — either by selecting the dependent component, by demonstrating that the dependency is already met by the TOE design, or by providing a rationale for why the dependency is not applicable.

> **CC 2022 note:** CC 2022 introduced the FPR (Privacy) class, which was not present in CC 3.1 R5. Additionally, several families were restructured and new components were added across existing classes. When using CC 2022 components, verify that the specific component identifier exists in the CC 2022 Part 2 catalogue.

## Operations on SFRs

Once a functional component is selected from CC Part 2, it typically requires completion through one or more [CC operations](./Operations.md):

- **[Assignment](./Operation-Assignment.md)** — Fill in a parameter with a specific value (e.g., specify a password length).
- **[Selection](./Operation-Selection.md)** — Choose from a set of options specified in the component (e.g., select "modification" from {modification, deletion, insertion}).
- **[Iteration](./Operation-Iteration.md)** — Use the same component multiple times with different operations or for different subjects/objects.
- **[Refinement](./Operation-Refinement.md)** — Add detail or narrow scope without changing the component's fundamental meaning.

The result of applying operations to a functional component is a fully specified SFR ready for inclusion in an ST or PP.

## Practical guidance

### Deriving SFRs from security objectives

1. **Start from each security objective for the TOE.** Review the [security objectives](./SecurityObjective.md) derived from the [Security Problem Definition](./SecurityProblemdefinition.md). Each objective must be addressed by one or more SFRs.

2. **Identify candidate functional components.** For each security objective, search CC Part 2 for functional components that address the required security behaviour. Use the class descriptions above to narrow the search. For example:
   - Objective requiring access control → FDP_ACC, FDP_ACF families.
   - Objective requiring user authentication → FIA_UAU, FIA_UID families.
   - Objective requiring audit trail → FAU_GEN, FAU_SAR families.

3. **Select the appropriate hierarchical level.** Within a family, choose the lowest component that fully satisfies the objective. Higher components impose additional requirements and increase evaluation effort.

4. **Complete all operations.** Apply assignments, selections, iterations, and refinements to transform the generic component into a concrete SFR. Each operation should be traceable to the security objective or security problem definition.

5. **Resolve dependencies.** Check the selected components' declared dependencies. For each dependency:
   - Select the required component if not already included.
   - Or provide a rationale for why the dependency does not apply.

6. **Map SFRs to objectives.** Create a traceability matrix showing which SFRs address which security objectives. This mapping forms the core of the [rationale](./Rationale.md) that security objectives are met by the selected SFRs.

7. **Verify completeness and consistency.**
   - **Completeness:** Every security objective for the TOE is addressed by at least one SFR.
   - **Consistency:** No two SFRs impose contradictory requirements on the TSF.
   - **Necessity:** Each SFR traces back to at least one security objective (no unnecessary requirements).

### Common pitfalls

- **Over-specifying operations:** Avoid narrowing assignments or selections beyond what the security objective requires — this unnecessarily constrains TOE implementations.
- **Ignoring dependencies:** Unresolved dependencies lead to evaluation findings. Always check the dependency chain.
- **Mixing SFRs and implementation:** SFRs describe *what* the TSF must do, not *how* it does it. Implementation details belong in the [TOE Summary Specification](./TOESummarySpecification.md).
- **Duplicate iterations without distinction:** When iterating a component, ensure each iteration serves a distinct purpose (different subject/object pair, different policy, etc.) and is clearly labeled.

## Additional resources

- CC 2022 Part 2 — the complete catalogue of functional classes, families, and components.
- CC 2022 Part 1, Section 6.2 — security functional requirements structure and usage.
- ISO/IEC TR 15446 — guidance for PP and ST authors on SFR selection.
- CEM Part 2, ASE_REQ — evaluator actions for assessing the statement of security requirements.

## Related articles

- [Security Components](./SecurityComponent.md)
- [Security Objectives](./SecurityObjective.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
- [Operations](./Operations.md)
- [Extended Component Definition](./ExtendedComponentDefinition.md)
- [Rationale](./Rationale.md)
- [TOE Summary Specification](./TOESummarySpecification.md)
- [Protection Profile](./ProtectionProfile.md)
