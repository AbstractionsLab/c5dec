---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: rationale, traceability, security-objectives, SFR, SPD
---

# Rationale

The **rationale** in a [Protection Profile](./ProtectionProfile.md) or [Security Target](./SecurityTarget.md) provides the logical justification that connects the security problem to the security solution. It demonstrates that the chosen [security objectives](./SecurityObjective.md) address all identified threats, [OSPs](./OrganizationalSecurityPolicy.md), and [assumptions](./Assumption.md), and that the selected [security requirements](./SecurityFunctionalRequirement.md) fulfil all security objectives.

## Definition

CC 2022 Part 1 describes the rationale as having the following structure:

> *The rationale expresses the resolution of the security problem by the security objectives, the coverage of all security objectives by the security requirements, and the mapping between the security requirements and the TOE Summary Specification. The rationale also includes a sufficiency argument demonstrating that these mappings are complete and mutually supportive.*

In the standard model (as opposed to the [direct rationale](./DirectRationale.md) approach), the rationale consists of three layers:

| Rationale layer | From | To | Purpose |
|-----------------|------|----|---------|
| **Security objectives rationale** | Threats, OSPs, Assumptions | Security Objectives for the TOE and its Operational Environment | Demonstrates that every SPD item is addressed by at least one objective and that each objective traces back to at least one SPD item. |
| **Security requirements rationale** | Security Objectives for the TOE | SFRs (and SARs) | Demonstrates that every TOE security objective is met by at least one SFR, and every SFR traces to at least one objective. |
| **TOE Summary Specification mapping** | SFRs | Implementation mechanisms | Shows how each SFR is realised by the [TOE Summary Specification](./TOESummarySpecification.md). |

### Completeness and sufficiency

For each rationale layer, two properties must hold:

- **Completeness:** Every item on the "from" side is addressed by at least one item on the "to" side (no unaddressed threats, no unmet objectives).
- **Sufficiency:** The items on the "to" side, taken together, are enough to fully address each item on the "from" side. This is a qualitative argument, not just a check-mark exercise.

### Direct rationale

When the [direct rationale](./DirectRationale.md) model is used, the security objectives layer is omitted. The rationale maps the SPD directly to the SFRs. See the [Direct Rationale](./DirectRationale.md) article for details.

## Practical guidance

### Writing a rationale

1. **Build a traceability matrix.** Create a table with SPD items (threats, OSPs, assumptions) as rows and security objectives as columns. Place a mark where an objective addresses an SPD item. Verify every row has at least one mark and every column has at least one mark.
2. **Write per-cell justifications.** For each marked cell, write a sentence or paragraph explaining how the objective addresses the SPD item. Generic statements like "this objective counters this threat" are insufficient -- describe the mechanism (e.g., "O.ACCESS_CONTROL counters T.UNAUTH_ACCESS by ensuring that only authenticated users with the appropriate role can access protected resources").
3. **Repeat for objectives-to-SFRs.** Build a second matrix mapping security objectives to SFRs. For each marked cell, explain how the SFR fulfils or contributes to the objective.
4. **Verify sufficiency.** Walk through each SPD item and read all the linked justifications together. Ask: "If the TOE satisfies all these objectives/SFRs, is this threat fully countered / this OSP fully enforced / this assumption fully supported?" If not, add more objectives or SFRs.
5. **Verify mutual support.** Check that SFRs do not undermine each other. For example, an SFR allowing anonymous access to certain resources should not conflict with an SFR requiring authentication for all access.
6. **Cross-reference the TSS.** After the requirements rationale, verify that the [TOE Summary Specification](./TOESummarySpecification.md) maps every SFR to an implementation mechanism. If an SFR has no TSS mapping, the specification is incomplete.

### Common rationale deficiencies

- **Missing coverage.** An SPD item (often an assumption) with no corresponding objective, or an objective with no SFR mapping. This is the most common evaluation finding in ASE activities.
- **Insufficient justification.** A traceability mark without explanation. Evaluators need to understand *how* the mapping works, not just that it exists.
- **One-to-one reasoning.** Assuming each threat maps to exactly one objective and each objective to exactly one SFR. In practice, many-to-many mappings are normal and expected.
- **Ignoring the operational environment.** Assumptions and objectives for the operational environment also need rationale demonstrating that the environment, as described, satisfies them.

### Example traceability table (SPD to objectives)

| | O.ACCESS_CTRL | O.AUDIT | O.CRYPTO | OE.PHYSICAL |
|---|:---:|:---:|:---:|:---:|
| **T.UNAUTH_ACCESS** | X | X | | |
| **T.DATA_DISCLOSURE** | X | | X | |
| **P.AUDIT_REVIEW** | | X | | |
| **A.PHYSICAL** | | | | X |

Each "X" cell has an accompanying justification paragraph in the rationale text.

## Additional resources

- CC 2022 Part 1, Section 7.4 -- rationale requirements for PPs and STs.
- CC 2022 Part 1, Annex A.5 -- rationale for PPs.
- CC 2022 Part 1, Annex B.5 -- rationale for STs.
- CEM, ASE_REQ and ASE_OBJ evaluation activities.

## Related articles

- [Security Objectives](./SecurityObjective.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [Security Problem Definition](./SecurityProblemdefinition.md)
- [Direct Rationale](./DirectRationale.md)
- [TOE Summary Specification](./TOESummarySpecification.md)
- [Security Target](./SecurityTarget.md)
- [Protection Profile](./ProtectionProfile.md)
