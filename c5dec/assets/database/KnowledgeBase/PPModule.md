---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: PP-Module, protection-profile, modular-PP, PP-Configuration
---

# PP-Module

**Acronym:** PP-Module / MOD

A **PP-Module** is a special type of [Protection Profile](./ProtectionProfile.md) that cannot stand alone. It specifies incremental security requirements intended to be combined with a **Base PP** to form a [PP-Configuration](./PPConfiguration.md). PP-Modules enable a modular approach to PP development, allowing communities to define specialised security requirements that augment a general-purpose base PP without modifying it.

PP-Modules are a central feature of CC 2022 and are increasingly required by modern certification schemes such as the [EUCC](./EUCC.md) and NIAP. They enable flexible and scalable protection profile ecosystems where a single base PP can be extended by multiple modules addressing different product capabilities (e.g., VPN functionality, biometric authentication, wireless communication).

> **CC 2022 note:** PP-Modules were informally discussed in CC 3.1 R5 but had no standardised structure or conformance rules. CC 2022 Part 1 Annex D formalises PP-Module structure, permitted dependency resolution approaches, and interaction with exact conformance. This article reflects the CC 2022 formalisation.

## Structure of a PP-Module

A PP-Module follows the standard PP structure but with key differences:

1. **PP-Module reference** — identifies the module, its version, and the base PP(s) it is designed to extend.
2. **Conformance claim** — specifies that this is a PP-Module and names the base PP(s) with which it is compatible.
3. **Security problem definition (SPD)** — defines additional [threats](./Threat.md), [OSPs](./OrganizationalSecurityPolicy.md), and [assumptions](./Assumption.md) introduced by the module's scope. These are additive to the base PP's SPD.
4. **Security objectives** — defines additional [security objectives](./SecurityObjective.md) for the TOE and its operational environment, derived from the module's SPD.
5. **Security requirements** — specifies additional [SFRs](./SecurityFunctionalRequirement.md) and optionally additional [SARs](./SecurityAssuranceRequirement.md). The module may also modify base PP SFRs if permitted by the base PP.
6. **Rationale** — demonstrates that the module's requirements address the module's security objectives and are consistent with the base PP.

## Relationship to base PP and PP-Configuration

A PP-Module **requires** a base PP. The combination of a base PP plus one or more PP-Modules forms a [PP-Configuration](./PPConfiguration.md). The PP-Configuration is the artefact against which a [Security Target](./SecurityTarget.md) claims conformance.

Key rules:
- A PP-Module shall not contradict requirements of the base PP.
- SFR dependencies introduced by the module may be resolved by SFRs in the base PP, by other modules in the same PP-Configuration, or by the module itself.
- If a module modifies a base PP SFR (e.g., by refining an assignment), the base PP must explicitly permit such modifications.
- Multiple PP-Modules can be combined in a single PP-Configuration, provided there are no conflicts.

## Practical guidance

### Reading a PP-Module

1. **Start with the base PP.** Understand the base PP's SPD, security objectives, and SFRs before reading the module.
2. **Identify the incremental scope.** The module's SPD section describes what additional threat surface or functionality is covered. Focus on understanding what the module adds, not what it restates from the base PP.
3. **Check for SFR modifications.** Some modules refine or extend base PP SFRs — look for explicit statements of which base PP requirements are affected.
4. **Verify dependency resolution.** Ensure that all SFR dependencies introduced by the module are satisfied, either by the base PP, by other selected modules, or by the module itself.

### Writing a PP-Module

1. **Identify the capability to be modularised.** Determine the specific product functionality (e.g., VPN, TLS, biometric sensor) that warrants a separate module.
2. **Select the base PP(s).** Define which base PP(s) the module is designed to extend. Ensure the base PP's conformance statement permits modular extension.
3. **Define the incremental SPD.** Identify additional threats, OSPs, and assumptions that are relevant only when the modular capability is present. Avoid restating the base PP's SPD.
4. **Derive additional security objectives.** Map the incremental SPD to new security objectives, demonstrating that each new threat or OSP is addressed.
5. **Specify additional SFRs.** Select or define functional components that fulfil the new security objectives. Clearly distinguish between:
   - New SFRs introduced by the module.
   - Modifications to base PP SFRs (only if permitted).
   - Iterated SFRs that extend a base PP component.
6. **Resolve dependencies.** For each new SFR, verify that its dependencies are met — either internally, by the base PP, or by a co-selected module (with a clear statement of this expectation).
7. **Write the rationale.** Demonstrate SPD-to-objective and objective-to-SFR mappings for the module's additions.
8. **Validate compatibility.** Review the complete PP-Configuration (base PP + all selected modules) for logical consistency and absence of contradictions.

## Additional resources

- CC 2022 Part 1, Annex D — PP-Module and PP-Configuration structure and rules.
- CC 2022 Part 1, Section 6.4 — conformance claims for modular PPs.
- NIAP Technical Decisions on PP-Modules — practical guidance from an active certification scheme.

## Related articles

- [Protection Profile](./ProtectionProfile.md)
- [PP-Configuration](./PPConfiguration.md)
- [Security Target](./SecurityTarget.md)
- [Conformance Claim](./ConformanceClaim.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [Exact Conformance FAQ](./Exactconformance-FAQ.md)
- [EUCC](./EUCC.md)
