---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: operations, assignment, selection, refinement, iteration, SFR, SAR
---

# Operations

**Operations** are the mechanisms by which CC components are tailored to meet a specific security need. They transform generic CC catalogue components into precise, evaluable requirements within a [Protection Profile](./ProtectionProfile.md) or [Security Target](./SecurityTarget.md).

## The four operations

CC 2022 defines four operations that can be applied to components from CC Part 2 (functional) and CC Part 3 (assurance):

| Operation | Purpose | Who performs | Notation in CC text |
|-----------|---------|-------------|---------------------|
| [**Assignment**](./Operation-Assignment.md) | Fill in a value where the component leaves a specification open. | PP/ST author | `[assignment: ...]` |
| [**Selection**](./Operation-Selection.md) | Choose one or more items from a predefined list within the component. | PP/ST author | `[selection: ...]` |
| [**Refinement**](./Operation-Refinement.md) | Add detail to narrow or clarify a requirement without changing its fundamental meaning. | PP/ST author | Shown in **bold** with annotation |
| [**Iteration**](./Operation-Iteration.md) | Use the same component more than once with different operation completions. | PP/ST author | Component ID + suffix (e.g., `/1`, `/Admin`) |

## When operations are performed

Operations are performed at two stages in the CC lifecycle:

1. **PP authoring.** The PP author completes or constrains operations to define requirements for a class of products. Some operations may be fully completed in the PP (e.g., a fixed key length for cryptographic requirements); others are left open for the ST author.
2. **ST authoring.** The ST author completes any operations left open by the PP and may perform additional refinements or iterations specific to the individual TOE. In a standalone ST (no PP claimed), all operations are completed by the ST author.

## Rules summary

- **Assignments** must be completed with concrete, unambiguous values matching the expected type.
- **Selections** are constrained to the options listed in the CC component (unless a refinement modifies the list).
- **Refinements** must make the requirement stricter, not weaker, and must not conflict with other requirements.
- **Iterations** must each differ in at least one completed operation; identical iterations are redundant.
- All completed operations must be traceable through the [rationale](./Rationale.md) to [security objectives](./SecurityObjective.md) (standard model) or directly to the [security problem definition](./SecurityProblemdefinition.md) ([direct rationale](./DirectRationale.md) model).

## Practical guidance

1. **Start with the PP.** Read the claimed PP to understand which operations are pre-completed and which are open. This determines the ST author's remaining work.
2. **Process each SFR systematically.** For every SFR in the ST, walk through each element and complete every assignment and selection. Apply refinements and iterations where the TOE's design requires them.
3. **Use consistent notation.** Follow the PP or scheme template for how operations are visually distinguished (bold for refinements, underlined for selections, etc.). Consistency aids evaluator review.
4. **Cross-check dependencies.** Some operations in one SFR depend on choices made in another (e.g., an access control SFP name assigned in FDP_ACC.1 must be referenced consistently in FDP_ACF.1). Verify cross-references after completing all operations.

## Additional resources

- CC 2022 Part 1, Section 5.3 -- operations overview and rules.
- CC 2022 Part 2, Annex A -- notation conventions for functional component operations.
- CC 2022 Part 3, Annex A -- notation conventions for assurance component operations.
- ISO/IEC TR 15446 -- guide for completing operations in PPs and STs.

## Related articles

- [Operation: Assignment](./Operation-Assignment.md)
- [Operation: Selection](./Operation-Selection.md)
- [Operation: Refinement](./Operation-Refinement.md)
- [Operation: Iteration](./Operation-Iteration.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
- [Protection Profile](./ProtectionProfile.md)
- [Security Target](./SecurityTarget.md)
