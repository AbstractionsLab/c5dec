---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: PP-Configuration, protection-profile, PP-Module, base-PP, modular-PP
---

# PP-Configuration

**Acronym:** PP-Config

A **PP-Configuration** is a combined construct formed by pairing a **Base Protection Profile** with one or more **[PP-Modules](./PPModule.md)**. It represents the complete set of security requirements that a [Security Target](./SecurityTarget.md) must satisfy when claiming conformance to both the base PP and the selected modules. PP-Configurations enable a modular, scalable approach to protection profile development — a single base PP can serve as the foundation for multiple product variants, with PP-Modules adding specialised capabilities as needed.

PP-Configurations are a core concept in CC 2022 and are fundamental to modern certification schemes such as the [EUCC](./EUCC.md) and NIAP, where product categories are increasingly addressed through modular PP ecosystems.

> **CC 2022 note:** In CC 3.1 R5, PP-Configurations were not formally defined. The concept of combining PPs was discussed informally, but lacked standardised rules for module composition, dependency resolution, and conformance type handling. CC 2022 Part 1 Annex D introduces formal PP-Configuration semantics. This article reflects the CC 2022 formalisation.

## Structure

A PP-Configuration is not a standalone document. It is the logical combination of:

1. **Exactly one Base PP** — provides the foundational security requirements (SPD, objectives, SFRs, SARs) for the product category.
2. **One or more PP-Modules** — each adds incremental requirements for a specific capability or feature.

The resulting PP-Configuration defines:
- The union of security problem definitions from the base PP and all selected modules.
- The union of security objectives.
- The combined set of SFRs (base PP SFRs plus module SFRs, with any module-permitted modifications).
- The SARs from the base PP (modules may add but typically do not reduce SARs).

## Conformance to a PP-Configuration

A [Security Target](./SecurityTarget.md) claiming conformance to a PP-Configuration must:

1. Identify the specific PP-Configuration (base PP version + selected PP-Module versions).
2. Meet all requirements of the base PP.
3. Meet all additional requirements of each selected PP-Module.
4. Resolve any SFR dependencies introduced across module boundaries.
5. Demonstrate consistency — no contradiction between base PP requirements and module requirements.

The conformance type (exact, strict, or demonstrable) is determined by the [conformance statement](./ConformanceStatement.md) of the base PP. PP-Modules inherit the base PP's conformance type unless they explicitly specify a different type for their own requirements.

## Practical guidance

### Reading a PP-Configuration

1. **Start with the base PP.** Read and understand the base PP in its entirety — its security problem definition, objectives, SFRs, and SARs.
2. **Read each selected PP-Module sequentially.** For each module, identify:
   - Additional threats, OSPs, and assumptions it introduces.
   - Additional SFRs it specifies.
   - Any modifications to base PP SFRs (check if the base PP permits this).
3. **Assemble the combined picture.** Mentally (or in a table) merge the base PP and module requirements into a unified set. Verify that all SFR dependencies are resolved.
4. **Check for conflicts.** Ensure no module requirement contradicts a base PP requirement. This is particularly important for assignments and selections that may be fixed differently.

### Building a PP-Configuration

1. **Select the base PP.** Choose a certified or established base PP for the product category. The base PP should address the general-purpose security requirements of the product.
2. **Identify required modules.** Based on the product's capabilities, determine which PP-Modules are needed. Only select modules that are designed for the chosen base PP.
3. **Verify compatibility.** Confirm that:
   - Each selected module declares compatibility with the base PP.
   - No two modules impose contradictory requirements.
   - All cross-module SFR dependencies are resolvable.
4. **Document the PP-Configuration.** In the ST, clearly list the base PP and each selected module, including version identifiers.
5. **Build the conformance claim.** State that the ST claims conformance to the specified PP-Configuration and identify the conformance type.

### Common pitfalls

- **Selecting incompatible modules.** Not all PP-Modules are designed for the same base PP. Always verify the declared base PP compatibility.
- **Unresolved cross-module dependencies.** Module A may introduce an SFR that depends on a component that Module B was expected to provide. If Module B is not selected, the dependency remains unresolved.
- **Version mismatch.** The base PP and PP-Modules should reference compatible CC versions. Mixing CC 3.1 R5 and CC 2022 artefacts may create conformance issues.

## Additional resources

- CC 2022 Part 1, Annex D — formal PP-Configuration rules, composition semantics, and examples.
- CC 2022 Part 1, Section 6.4 — conformance claims for PP-Configurations.
- NIAP PP-Configuration examples — real-world PP-Configurations from an active certification scheme.

## Related articles

- [Protection Profile](./ProtectionProfile.md)
- [PP-Module](./PPModule.md)
- [Security Target](./SecurityTarget.md)
- [Conformance Claim](./ConformanceClaim.md)
- [Conformance Statement](./ConformanceStatement.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [EUCC](./EUCC.md)
