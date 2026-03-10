---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: package, EAL, assurance-package, functional-package, augmentation
---

# Package

**Acronym:** None

A **Package** in Common Criteria is a named, reusable set of either functional or assurance components that addresses an identified set of security objectives. Packages are designed to be reused across multiple [Protection Profiles](./ProtectionProfile.md) and [Security Targets](./SecurityTarget.md), providing a standardised and consistent way to express security requirements without redefining component selections each time. The most well-known packages are the [Evaluation Assurance Levels (EALs)](./EvaluationAssuranceLevel.md), but the CC framework also supports custom assurance packages and functional packages.

## Assurance packages

Assurance packages provide a predefined combination of [Security Assurance Requirements (SARs)](./SecurityAssuranceRequirement.md) at a specific level of rigour. The most common assurance packages are the seven Evaluation Assurance Levels:

| Package | Name | Description |
|---------|------|-------------|
| EAL1 | Functionally tested | Basic assurance through functional testing and examination of guidance |
| EAL2 | Structurally tested | Adds developer testing, vulnerability analysis, and design review |
| EAL3 | Methodically tested and checked | Adds methodical development environment controls and independent testing |
| EAL4 | Methodically designed, tested, and reviewed | Detailed design review, systematic testing, and informal security policy model |
| EAL5 | Semiformally designed and tested | Semiformal methods, modular design, and covert channel analysis |
| EAL6 | Semiformally verified design and tested | Structured development, comprehensive vulnerability analysis |
| EAL7 | Formally verified design and tested | Formal methods, complete independent testing, and formal analysis |

### Augmentation

An assurance package can be **augmented** by adding one or more assurance components from families not already included in the package, or by substituting a hierarchically higher component for one already present. Augmented EALs are denoted with a "+" suffix (e.g., EAL4+ with AVA_VAN.5).

Augmentation rules:
1. The added component must not already be in the package (unless it is hierarchically higher).
2. The added component must not create contradictions with other components in the package.
3. A rationale shall be provided for the augmentation in the [Security Target](./SecurityTarget.md) or [Protection Profile](./ProtectionProfile.md).

## Functional packages

Functional packages group [Security Functional Requirements (SFRs)](./SecurityFunctionalRequirement.md) addressing a common security objective (e.g., cryptographic key management, secure session handling). Unlike assurance packages, functional packages are not predefined by the CC standard — they are defined by PP authors, technical communities, or certification schemes.

A functional package:
- Contains a named set of SFRs from CC Part 2 or [extended components](./ExtendedComponentDefinition.md).
- May specify operations (assignments, selections) that must be completed by the PP or ST author.
- Can be referenced by a PP or ST for conformance purposes.
- Is subject to **exact conformance** rules when referenced from an exact-conformance PP.

> **CC 2022 note:** CC 2022 formalises the concept of functional packages and their interaction with exact conformance. In CC 3.1 R5, functional packages were less formally defined and rarely used in practice.

## Practical guidance

### Selecting an assurance package

1. **Start with the target evaluation context.** Consider the threat environment, the intended use of the TOE, and any regulatory or scheme requirements (e.g., [EUCC](./EUCC.md) specifies "substantial" and "high" assurance levels mapped to specific EALs).
2. **Match the EAL to the risk.** Higher EALs provide more confidence but require significantly more development and evaluation effort. EAL1-2 are suitable for basic commercial products; EAL3-4 for products in regulated environments; EAL5-7 for high-security government and defence systems.
3. **Consider augmentation over jumping EALs.** If one specific assurance area needs strengthening (e.g., vulnerability analysis), augment the base EAL rather than moving to a higher EAL that increases work across all assurance families.
4. **Document the rationale.** The [Security Target](./SecurityTarget.md) must justify the chosen package and any augmentations.

### Defining a functional package

1. **Identify the security objective** the package addresses (e.g., "secure cryptographic key management").
2. **Select SFRs** from CC Part 2 that collectively meet the objective. Include all dependencies.
3. **Specify required operations** — indicate which assignments and selections are left to the PP/ST author and which are fixed by the package.
4. **Define the conformance type** — typically exact conformance for interoperability.
5. **Validate completeness** — ensure the package is self-contained and all internal dependencies are resolved.

## Additional resources

- CC Part 1, Section 6.3 (Packages) — defines package structure and usage rules.
- CC Part 3, Section 7 (Evaluation Assurance Levels) — defines the seven EALs.
- ISO/IEC TR 15446 — guidance on PP and ST development, including package selection.

## Related articles

- [Evaluation Assurance Levels](./EvaluationAssuranceLevel.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
- [Protection Profile](./ProtectionProfile.md)
- [Security Target](./SecurityTarget.md)
- [EUCC](./EUCC.md)
- [Extended Component Definition](./ExtendedComponentDefinition.md)
