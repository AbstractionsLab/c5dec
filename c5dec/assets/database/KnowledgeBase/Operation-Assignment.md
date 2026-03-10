---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: operation, assignment, SFR, SAR, PP, ST
---

# Operation: Assignment

An **assignment** operation allows a PP/ST author to fill in a specification identified in a component with a specific value. An assignment is indicated in CC Part 2 and Part 3 by text enclosed in square brackets with the prefix "assignment:".

## Definition

When a CC component contains an assignment, the PP/ST author must supply a value that completes the requirement. The completed assignment becomes part of the instantiated requirement.

There are four completion scenarios:

| Scenario | Who completes | Description |
|----------|---------------|-------------|
| **PP completes fully** | PP author | The PP specifies the exact value. An ST claiming conformance to this PP must use the same value (exact conformance) or an equivalent value (demonstrable conformance). |
| **PP constrains, ST completes** | PP author + ST author | The PP narrows the range of acceptable values but leaves the final choice to the ST author. |
| **PP leaves open, ST completes** | ST author | The PP does not restrict the assignment; the ST author provides the value based on the specific TOE. |
| **ST standalone** | ST author | No PP is claimed; the ST author provides the value directly. |

## Practical guidance

### Completing an assignment

1. **Read the assignment description carefully.** The CC component text describes what kind of value is expected -- e.g., "assignment: list of subjects", "assignment: number of unsuccessful authentication attempts". The expected type constrains what you may provide.
2. **Check the claimed PP for constraints.** If the ST claims conformance to a PP, the PP may have already completed the assignment or constrained the allowed values. With exact conformance, the ST must use the PP's value verbatim.
3. **Be specific and unambiguous.** Avoid vague values like "appropriate subjects" or "a suitable time period". Evaluators must be able to determine whether the TOE meets the requirement, so values must be concrete (e.g., "authenticated administrators and operators", "5 minutes").
4. **Document the rationale.** The [rationale](./Rationale.md) section of the ST should explain why the chosen value is appropriate for the TOE's [security objectives](./SecurityObjective.md) and threat environment.

### Common mistakes

- **Leaving an assignment incomplete.** Every assignment in a claimed SFR/SAR must be completed in the ST. An empty or placeholder assignment causes an ASE evaluation failure.
- **Overly broad values.** Assigning "all users" when the requirement expects specific subject categories weakens the requirement and may not match the TOE implementation.
- **Contradicting the PP.** Under exact conformance, any deviation from the PP's completed assignment violates the conformance claim.

### Example

CC component FIA_AFL.1.2 contains: *"... the TSF shall [assignment: list of actions]"*.

A completed assignment in an ST might read: *"... the TSF shall lock the user account for 30 minutes and notify the administrator via syslog."*

## Additional resources

- CC 2022 Part 1, Section 5.3 -- operations on components.
- CC 2022 Part 2, Annex A -- notation conventions for assignments and selections.
- ISO/IEC TR 15446 -- guidance on completing operations in PPs and STs.

## Related articles

- [Operations](./Operations.md)
- [Operation: Selection](./Operation-Selection.md)
- [Operation: Refinement](./Operation-Refinement.md)
- [Operation: Iteration](./Operation-Iteration.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [Protection Profile](./ProtectionProfile.md)
- [Security Target](./SecurityTarget.md)
