---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: operation, refinement, SFR, SAR, PP, ST
---

# Operation: Refinement

A **refinement** operation allows a PP/ST author to add detail to a requirement, thereby narrowing its scope or clarifying its application, without changing the fundamental meaning.

## Definition

A refinement modifies the text of a CC component element to provide additional constraints or precision. Two rules govern valid refinements:

1. **A refinement must make the requirement stricter, not weaker.** The refined requirement must be at least as restrictive as the original. For example, narrowing "cryptographic operation" to "AES-256 encryption" is valid; broadening "AES-256" to "any symmetric cipher" is not.
2. **A refinement of one requirement must not conflict with another requirement.** If two SFRs share related elements, a refinement applied to one must remain consistent with the other's elements and any refinements applied there.

An **editorial refinement** is a minor text change that improves clarity without altering the technical meaning -- for example, replacing a CC generic term with a product-specific synonym. Editorial refinements are always acceptable and do not change the requirement's coverage.

### Refinement in PPs and PP-Modules

When a [PP](./ProtectionProfile.md) refines a component, the refinement becomes part of the PP's requirement. A [Security Target](./SecurityTarget.md) claiming exact conformance must include the PP's refinement verbatim. Under [demonstrable conformance](./ConformanceStatement.md), the ST may propose an equivalent or stricter refinement.

When a [PP-Module](./PPModule.md) refines a requirement, the refinement applies only when that PP-Module is included in a [PP-Configuration](./PPConfiguration.md). If the base PP has its own refinement for the same component, the PP-Module's conformance claim must state how the two interact.

### Extended requirements

[Extended components](./ExtendedComponentDefinition.md) may also be refined. The same rules apply: the refined extended requirement must remain at least as restrictive as the original.

## Practical guidance

### Performing a refinement

1. **Identify the element to refine.** Refinements apply to individual elements within a component (e.g., a specific bullet point or clause), not to the component as a whole.
2. **Use bold text and annotation.** The conventional notation places the refined text in **bold** and adds "[Refinement:]" or a footnote indicating the change. This makes the refinement immediately visible to evaluators.
3. **Verify the "stricter" rule.** Ask: "Does every TOE that satisfies the refined requirement also satisfy the original?" If yes, the refinement is valid. If no, the refinement weakens the requirement and is invalid.
4. **Check cross-requirements consistency.** If the refined requirement shares subjects, objects, or operations with other SFRs, verify no contradiction arises.
5. **Document the rationale.** Explain in the [rationale](./Rationale.md) why the refinement is needed and how it relates to the [security objectives](./SecurityObjective.md) or threat model.

### Common mistakes

- **Weakening disguised as refinement.** Adding "when enabled by the administrator" to a mandatory security function is a weakening, not a refinement.
- **Conflicting refinements.** Refining FDP_ACC.1 to apply to "network traffic only" while FDP_IFC.1 requires "all information flows" introduces an inconsistency.
- **Unnecessary refinement.** If the original CC text is already precise enough for the TOE, a refinement adds complexity without benefit. Only refine when the generic CC language genuinely needs narrowing.

### Example

CC component FCS_COP.1.1 requires: *"The TSF shall perform [assignment: list of cryptographic operations] in accordance with a specified cryptographic algorithm [assignment: cryptographic algorithm] and cryptographic key sizes [assignment: cryptographic key sizes] that meet the following: [assignment: list of standards]."*

A refinement might add: *"The TSF shall perform **AES encryption and decryption** in accordance with **AES-256-GCM** and cryptographic key sizes **256 bits** that meet the following: **NIST SP 800-38D and FIPS 197**."*

Here the assignments are completed and the specification is refined to a specific algorithm mode. This is stricter than the generic requirement.

## Additional resources

- CC 2022 Part 1, Section 5.3.3 -- refinement operation rules.
- CC 2022 Part 2, Annex A -- notation conventions.
- ISO/IEC TR 15446 -- guidance on completing and refining requirements.

## Related articles

- [Operations](./Operations.md)
- [Operation: Assignment](./Operation-Assignment.md)
- [Operation: Selection](./Operation-Selection.md)
- [Operation: Iteration](./Operation-Iteration.md)
- [Extended Component Definition](./ExtendedComponentDefinition.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [Conformance Statement](./ConformanceStatement.md)
