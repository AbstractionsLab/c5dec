---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: operation, selection, SFR, SAR, PP, ST
---

# Operation: Selection

A **selection** operation allows a PP/ST author to choose one or more items from a list provided in a CC component. A selection is indicated in CC Part 2 and Part 3 by text enclosed in square brackets with the prefix "selection:".

## Definition

When a CC component contains a selection, the PP/ST author picks from the enumerated options to tailor the requirement to the specific TOE or product category. The chosen items replace the selection placeholder in the completed requirement.

There are three completion scenarios:

| Scenario | Who completes | Description |
|----------|---------------|-------------|
| **PP completes** | PP author | The PP selects specific items from the list. An ST claiming exact conformance must use the same selection. |
| **PP restricts, ST completes** | PP author + ST author | The PP narrows the allowed choices (e.g., "select at least one of: A, B") but leaves the final selection to the ST author. |
| **ST completes** | ST author | The PP leaves the selection open, or no PP is claimed; the ST author selects from the CC-provided options. |

### Selection of "None"

Some CC component selections include "none" as an option. Selecting "none" is valid only when the CC text explicitly lists it. When "none" is selected, any dependent elements (e.g., sub-elements conditioned on the selection) are not applicable. The [Security Target](./SecurityTarget.md) should note that these elements are not applicable rather than omitting them silently.

### Interaction with PP-Modules

When a [PP-Module](./PPModule.md) is added to a base [PP](./ProtectionProfile.md) via a [PP-Configuration](./PPConfiguration.md), the PP-Module may further restrict or complete selections left open by the base PP. The PP-Module's conformance claim section should specify how its selections interact with the base PP's selections.

## Practical guidance

### Completing a selection

1. **Read all available options.** The CC component text lists the valid choices. You may only select from these options (unless a [refinement](./Operation-Refinement.md) extends or restricts the list).
2. **Choose based on the TOE's functionality.** Select items that match what the TOE actually implements. Selecting items the TOE does not support will cause ATE (testing) failures.
3. **Check PP constraints.** If the ST claims conformance to a PP, the PP may have pre-selected items or constrained the available choices. Under exact conformance, the ST must use the PP's selection.
4. **Mark selections visibly.** The conventional notation is to underline or italicise the selected items within the component text, removing unchosen options. This makes evaluator review straightforward.
5. **Handle "none" carefully.** If the TOE does not implement any of the listed options and "none" is available, select it and explicitly note which dependent elements become not applicable.
6. **Document the rationale.** Explain in the [rationale](./Rationale.md) why the chosen options are appropriate for addressing the relevant [security objectives](./SecurityObjective.md).

### Common mistakes

- **Selecting items not in the CC list.** Unlike [assignments](./Operation-Assignment.md), selections are constrained to the provided options. Adding a custom option requires a [refinement](./Operation-Refinement.md) operation on the component.
- **Selecting contradictory options.** Some selections are mutually exclusive. Check whether the CC text uses "one of" (choose exactly one) versus "one or more of" (choose at least one).
- **Ignoring "none" implications.** Selecting "none" without addressing the dependent elements leaves the ST incomplete.

### Example

CC component FIA_UAU.1.1 contains: *"The TSF shall allow [assignment: list of TSF-mediated actions] on behalf of the user to be performed before the user is authenticated."*

FIA_UAU.5.1 contains: *"The TSF shall provide [selection: choose one or more of: password-based, certificate-based, biometric-based] authentication mechanisms."*

An ST author for a VPN gateway might select: **certificate-based, password-based** (two of the three options), reflecting the TOE's supported authentication methods.

## Additional resources

- CC 2022 Part 1, Section 5.3 -- operations on components.
- CC 2022 Part 2, Annex A -- notation conventions for selections.
- ISO/IEC TR 15446 -- guidance on completing operations in PPs and STs.

## Related articles

- [Operations](./Operations.md)
- [Operation: Assignment](./Operation-Assignment.md)
- [Operation: Refinement](./Operation-Refinement.md)
- [Operation: Iteration](./Operation-Iteration.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [PP-Module](./PPModule.md)
- [Protection Profile](./ProtectionProfile.md)
- [Security Target](./SecurityTarget.md)
