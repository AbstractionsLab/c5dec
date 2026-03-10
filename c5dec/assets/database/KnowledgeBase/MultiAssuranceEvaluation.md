---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: multi-assurance-evaluation, sub-TSF, assurance-rationale, PP-configuration
---

# Multi-Assurance Evaluation

In contrast to the [single-assurance evaluation](./SingleAssuranceEvaluation.md), the multi-assurance evaluation considers a global set of [SARs](./SecurityAssuranceRequirement.md) to apply to the entire [TOE](./TargetofEvaluation.md), while additional sets of SARs apply to individual [sub-TSFs](./SubTOESecurityFunctionality.md). In order to ensure that the set of SARs associated with one sub-TSF does not negatively impact other sub-TSFs, multi-assurance evaluations require an **assurance rationale** to demonstrate the consistency of the sets of SARs.

## Definition

A multi-assurance evaluation is an evaluation where different parts of the TOE are evaluated to different levels of assurance. This approach is used when:
- The TOE implements multiple security functionalities with different risk profiles.
- A [PP-Configuration](./PPConfiguration.md) combines multiple PPs or [PP-Modules](./PPModule.md), each specifying different SAR sets.
- A single TOE contains sub-systems where one sub-system protects higher-value [assets](./Asset.md) than others.

The TOE is decomposed into [sub-TSF](./SubTOESecurityFunctionality.md) partitions, each assigned its own assurance level. A global set of SARs applies to the whole TOE (including cross-cutting concerns like lifecycle and configuration management), while per-sub-TSF SARs apply to design, testing, and vulnerability analysis within each partition.

## Structure

A multi-assurance [Security Target](./SecurityTarget.md) includes:

1. **Global SARs** -- assurance requirements that apply to the entire TOE regardless of sub-TSF boundaries. Typically includes ALC (lifecycle), AGD (guidance), and whole-TOE ASE requirements.
2. **Per-sub-TSF SARs** -- assurance requirements applied to individual sub-TSFs. Typically includes ADV (development), ATE (testing), and AVA (vulnerability analysis) at the level appropriate for that sub-TSF's risk profile.
3. **Assurance rationale** -- a demonstration that:
   - The [domain separation](./DomainSeparation.md), [self-protection](./SelfProtection.md), and [non-bypassability](./NonBypassability.md) properties of the TSF architecture prevent a lower-assurance sub-TSF from compromising a higher-assurance one.
   - The global SARs provide sufficient coverage for concerns that cross sub-TSF boundaries.
   - Each sub-TSF's SAR set is appropriate for the threats it faces.

## Example scenario

Consider a network appliance TOE with two sub-TSFs:
- **Firewall sub-TSF** -- processes network traffic, enforcing packet filtering. Evaluated at EAL 4 (thorough vulnerability analysis needed due to exposure to untrusted traffic).
- **Management sub-TSF** -- provides a web-based administration interface accessible only from a trusted management network. Evaluated at EAL 2 (lower exposure, lower threat profile).

The global SARs (e.g., ALC_CMC.4, ALC_CMS.4) apply to the whole TOE. The ADV, ATE, and AVA families are applied at EAL 4 level for the firewall sub-TSF and at EAL 2 level for the management sub-TSF. The assurance rationale demonstrates that the management sub-TSF cannot be used to bypass the firewall sub-TSF's security functions.

## Practical guidance

### Deciding when to use multi-assurance

1. **Assess sub-system risk profiles.** If all parts of the TOE face similar threats, a [single-assurance evaluation](./SingleAssuranceEvaluation.md) is simpler and usually preferred. Multi-assurance is beneficial when sub-systems have genuinely different exposure levels.
2. **Check PP requirements.** If the claimed [PP-Configuration](./PPConfiguration.md) components specify different SAR sets, a multi-assurance evaluation is required by the PP-Configuration.
3. **Evaluate architectural feasibility.** Multi-assurance requires strong [domain separation](./DomainSeparation.md) between sub-TSFs. If the TOE's architecture does not cleanly separate sub-systems, demonstrating the assurance rationale becomes very difficult.

### Conducting a multi-assurance evaluation

1. **Define sub-TSF boundaries.** Identify which parts of the TSF belong to each sub-TSF. Document the interfaces between sub-TSFs and the mechanisms that enforce separation.
2. **Assign SAR sets.** For each sub-TSF, select the appropriate SARs. For the global scope, select SARs that cover whole-TOE lifecycle, guidance, and ST evaluation.
3. **Write the assurance rationale.** This is the critical new artifact. Demonstrate:
   - Separation mechanisms prevent interference between sub-TSFs.
   - A compromise of a lower-assurance sub-TSF cannot propagate to a higher-assurance one.
   - Global SARs are sufficient for shared components and cross-cutting concerns.
4. **Evaluate each sub-TSF to its assigned level.** The evaluator applies the per-sub-TSF SARs to the evidence for that sub-TSF, and the global SARs to the whole-TOE evidence.
5. **Issue a single certificate.** The result is one certificate for the composed TOE, noting the different assurance levels for each sub-TSF.

### Comparison with single-assurance evaluation

| Aspect | Single-assurance | Multi-assurance |
|--------|-----------------|-----------------|
| SAR assignment | One set for entire TOE | Global set + per-sub-TSF sets |
| Architectural requirement | None specific | Strong domain separation required |
| Additional evidence | None | Assurance rationale |
| Certificate | Single EAL | Single certificate noting per-sub-TSF levels |
| Typical use case | Homogeneous TOE | Heterogeneous TOE or PP-Configuration with mixed SARs |

> **CC 2022 note:** CC 2022 formalises multi-assurance evaluations and their relationship to PP-Configurations with mixed SAR sets. The assurance rationale requirements are defined in CC 2022 Part 1, Annex C.

## Additional resources

- CC 2022 Part 1, Annex C -- multi-assurance evaluation guidance.
- CC 2022 Part 1, Section 7.5 -- assurance rationale requirements.
- CC 2022 Part 3 -- SAR component definitions for per-sub-TSF application.

## Related articles

- [Single-Assurance Evaluation](./SingleAssuranceEvaluation.md)
- [Sub-TOE Security Functionality](./SubTOESecurityFunctionality.md)
- [PP-Configuration](./PPConfiguration.md)
- [Domain Separation](./DomainSeparation.md)
- [Self-Protection](./SelfProtection.md)
- [Non-Bypassability](./NonBypassability.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
- [Security Target](./SecurityTarget.md)
