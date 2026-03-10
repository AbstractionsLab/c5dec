---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: sub-TOE, multi-assurance, TSF-decomposition, assurance-level
---

# Sub-TOE security functionality

**Acronym:** None

A **Sub-TOE** is a defined portion of a [TOE](./TargetofEvaluation.md) that is subject to its own [assurance level](./EvaluationAssuranceLevel.md) within a [multi-assurance evaluation](./MultiAssuranceEvaluation.md). Sub-TOEs enable different parts of a product to be evaluated at different levels of rigour, reflecting the varying security criticality and threat exposure of each part. Each sub-TOE contains a subset of the [TOE Security Functionality (TSF)](./TOESecurityFunctionality.md) and is bounded within the overall [TOE boundary](./TOEBoundary.md).

The sub-TOE concept is particularly relevant for complex products where some parts operate in high-threat environments (e.g., cryptographic cores, key management modules) while other parts face lower threats (e.g., user interface components, logging subsystems).

> **CC 2022 note:** CC 2022 significantly expands the multi-assurance evaluation framework and formalises sub-TOE definitions more rigorously than CC 3.1 R5. In CC 3.1 R5, the concept was present but less developed, and most evaluations used a single assurance level for the entire TOE.

## Sub-TOE decomposition

Decomposing a TOE into sub-TOEs requires careful architectural analysis:

1. **Each sub-TOE must be a well-defined portion of the TSF.** It must be possible to clearly identify which hardware, firmware, and software elements belong to each sub-TOE.
2. **Sub-TOEs must collectively cover the entire TSF.** No TSF element may be left unassigned.
3. **Sub-TOE boundaries must align with architectural boundaries.** The decomposition should follow the TOE's actual modular structure (e.g., separate processes, separate hardware components, separate firmware images).
4. **Inter-sub-TOE interfaces must be identified.** Where one sub-TOE relies on services from another, the interfaces must be documented and their security properties assessed.

## Assurance assignment

Each sub-TOE is evaluated against its own set of [SARs](./SecurityAssuranceRequirement.md), typically expressed as an EAL:

- The **global SARs** apply to the TOE as a whole (e.g., ASE for ST evaluation applies globally).
- The **individual SARs** are assigned per sub-TOE based on the sub-TOE's criticality and exposure.
- The highest-assurance sub-TOE determines the upper bound of evaluation effort; the lowest-assurance sub-TOE must still meet a meaningful assurance baseline.

See [Multi-Assurance Evaluation](./MultiAssuranceEvaluation.md) for details on how global and individual SARs interact.

## Practical guidance

### Defining sub-TOEs

1. **Analyse the TOE architecture.** Review the TOE's design documentation, identifying major modules, processes, or hardware components. Look for natural architectural separations (e.g., kernel vs. user space, secure enclave vs. application processor).

2. **Assess security criticality.** For each candidate sub-TOE, determine:
   - Which [SFRs](./SecurityFunctionalRequirement.md) it enforces.
   - What [assets](./Asset.md) it protects.
   - What [threat](./Threat.md) exposure it has (e.g., directly network-facing, physically accessible, isolated).

3. **Assign assurance levels.** Map the criticality and threat exposure to appropriate EALs:
   - High-criticality, high-exposure components → higher EAL (e.g., EAL5+).
   - Lower-criticality, lower-exposure components → lower EAL (e.g., EAL2-3).

4. **Verify separation.**  Ensure that architectural properties — [domain separation](./DomainSeparation.md), [self-protection](./SelfProtection.md), and [non-bypassability](./NonBypassability.md) — are maintained between sub-TOEs. A compromised lower-assurance sub-TOE must not be able to undermine a higher-assurance sub-TOE.

5. **Document inter-sub-TOE interfaces.** For each interface between sub-TOEs, describe:
   - The services provided and consumed.
   - The security properties that must hold across the interface.
   - The assurance level at which the interface is assessed (typically the higher of the two sub-TOEs).

6. **Update the Security Target.** The [ST](./SecurityTarget.md) must describe the sub-TOE decomposition, assign SARs to each sub-TOE, and provide a rationale for the decomposition and assurance assignments.

### Common pitfalls

- **Artificial decomposition.** Splitting a tightly coupled module into sub-TOEs with different assurance levels is problematic if the separation is not architecturally enforced.
- **Ignoring transitive dependencies.** A high-assurance sub-TOE that depends on a low-assurance sub-TOE's services may not achieve its intended assurance in practice.
- **Under-specifying interfaces.** Vague inter-sub-TOE interface descriptions make it impossible for evaluators to assess whether separation is adequate.

## Additional resources

- CC 2022 Part 1, Section 8 — multi-assurance evaluation framework and sub-TOE rules.
- CC 2022 Part 3, Section 11 — assurance assignment for sub-TOEs.
- CEM, multi-assurance sub-activities — evaluator guidance for sub-TOE-specific evaluation tasks.

## Related articles

- [TOE Security Functionality](./TOESecurityFunctionality.md)
- [Multi-Assurance Evaluation](./MultiAssuranceEvaluation.md)
- [Evaluation Assurance Levels](./EvaluationAssuranceLevel.md)
- [Domain Separation](./DomainSeparation.md)
- [Self-Protection](./SelfProtection.md)
- [Non-Bypassability](./NonBypassability.md)
- [TOE Boundary](./TOEBoundary.md)
- [Security Target](./SecurityTarget.md)
