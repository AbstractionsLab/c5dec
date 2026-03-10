---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: operation, iteration, SFR, SAR, PP, ST
---

# Operation: Iteration

An **iteration** operation allows a component to be used more than once with varying operations, so that different aspects of the same generic requirement can be expressed separately.

## Definition

When a CC component is iterated, each instance is treated as a distinct requirement with its own operations ([assignments](./Operation-Assignment.md), [selections](./Operation-Selection.md), [refinements](./Operation-Refinement.md)). Each iteration must be uniquely identified so that it can be traced individually in the [rationale](./Rationale.md), [TOE Summary Specification](./TOESummarySpecification.md), and test evidence.

The standard notation appends a slash and a sequential number (or a descriptive suffix) to the component identifier. For example:
- FDP_ACC.1/Basic_Access
- FDP_ACC.1/Admin_Access

Or simply:
- FIA_UAU.2/1
- FIA_UAU.2/2

Each iteration must differ from every other iteration of the same component in at least one completed operation. If two iterations are identical after all operations are completed, they are redundant and one should be removed.

## When to iterate

- **Different subjects or objects.** The same functional requirement applies to different categories of users or data types, each with different parameters (e.g., different authentication mechanisms for administrators versus regular users).
- **Different security policies.** The same access control component is instantiated once for each distinct security function policy (SFP).
- **PP-driven iteration.** A [PP](./ProtectionProfile.md) or [PP-Module](./PPModule.md) may explicitly require iteration of certain components to cover distinct functional areas.

## Practical guidance

### Performing an iteration

1. **Determine whether iteration is necessary.** Consider whether the different aspects can be captured in a single instance using broader [assignments](./Operation-Assignment.md) or [selections](./Operation-Selection.md). Iterate only when the operations genuinely require distinct values that cannot be combined without loss of clarity.
2. **Choose meaningful identifiers.** Descriptive suffixes (e.g., FDP_ACC.1/Network, FDP_ACC.1/Local) are preferred over numeric suffixes because they aid reader comprehension and evaluator traceability.
3. **Complete all operations in each instance.** Each iteration is a standalone requirement. Every [assignment](./Operation-Assignment.md) and [selection](./Operation-Selection.md) in the component must be completed for each iteration independently.
4. **Trace each iteration separately.** The [rationale](./Rationale.md) must map each iteration to the [security objectives](./SecurityObjective.md) it addresses. The [TSS](./TOESummarySpecification.md) must describe the implementation mechanism for each iteration.
5. **Verify unique differentiation.** Before finalising, confirm that each iteration differs in at least one completed operation. Identical iterations indicate a modelling error.

### Example

The ST requires two instances of FIA_UAU.2 for a network gateway TOE:

- **FIA_UAU.2/Admin** -- Administrators authenticate using certificate-based authentication before any management actions.
- **FIA_UAU.2/VPN_User** -- VPN users authenticate using username/password and OTP before establishing a tunnel.

Each iteration traces to a different security objective and is tested independently.

## Additional resources

- CC 2022 Part 1, Section 5.3 -- operations on components.
- CC 2022 Part 2, introductory text -- component naming and iteration conventions.

## Related articles

- [Operations](./Operations.md)
- [Operation: Assignment](./Operation-Assignment.md)
- [Operation: Selection](./Operation-Selection.md)
- [Operation: Refinement](./Operation-Refinement.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [Rationale](./Rationale.md)
- [TOE Summary Specification](./TOESummarySpecification.md)
