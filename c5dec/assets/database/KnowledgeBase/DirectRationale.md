---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: direct-rationale, rationale, SFR-justification, security-objectives, SPD
---

# Direct rationale approach

**Acronym:** None

The **Direct Rationale** approach is an alternative to the standard rationale structure in a [Security Target](./SecurityTarget.md). Under the standard approach, the ST author must define a complete [Security Problem Definition (SPD)](./SecurityProblemdefinition.md), derive [security objectives](./SecurityObjective.md) from the SPD, and then derive [Security Functional Requirements (SFRs)](./SecurityFunctionalRequirement.md) from the security objectives — producing a two-stage rationale chain:

**Standard:** SPD → Security Objectives → SFRs

The **direct rationale** approach collapses this into a single stage by justifying the SFR selection directly against the SPD, without the intermediate security objectives layer:

**Direct:** SPD → SFRs

This approach is permitted by CC 2022 as an alternative for STs that do not claim conformance to a [Protection Profile](./ProtectionProfile.md) requiring the standard rationale. It reduces documentation effort while still requiring that each SFR be clearly justified.

> **CC 2022 note:** The direct rationale approach is formalised in CC 2022 Part 1. In CC 3.1 R5, the concept was alluded to but not explicitly supported as a first-class alternative. Most CC 3.1 R5 evaluations used the standard two-stage rationale.

## When to use direct rationale

The direct rationale approach is appropriate when:

1. **The ST does not claim PP conformance.** If the ST claims conformance to a PP, the PP's rationale structure must be followed. Most PPs require the standard two-stage rationale.
2. **The TOE's security problem is straightforward.** Products with a limited number of threats and clear SFR mappings benefit most from the reduced documentation.
3. **Security objectives would be redundant.** In some cases, security objectives add no information beyond restating the SPD in different terms. The direct rationale avoids this redundancy.
4. **The evaluation scheme permits it.** Some national schemes or [EUCC](./EUCC.md) scheme rules may have additional guidance on when direct rationale is acceptable.

The direct rationale approach is **not appropriate** when:
- The PP requires a standard rationale with security objectives.
- The TOE has a complex security problem definition with many interacting threats, OSPs, and assumptions where intermediate objectives clarify the design reasoning.
- Stakeholders (consumers, certification bodies) expect the standard rationale structure for transparency.

## Structure of a direct rationale

A Security Target using the direct rationale approach includes:

1. **Security Problem Definition** — [threats](./Threat.md), [OSPs](./OrganizationalSecurityPolicy.md), and [assumptions](./Assumption.md) as in the standard approach.
2. **Security objectives for the operational environment** — objectives addressing what the environment must provide (these are still required, as they are not expressed as SFRs).
3. **SFR selection** — the [SFRs](./SecurityFunctionalRequirement.md) and [SARs](./SecurityAssuranceRequirement.md) for the TOE.
4. **Direct rationale** — for each SFR, a justification explaining:
   - Which threat(s) and/or OSP(s) from the SPD the SFR addresses.
   - How the SFR contributes to countering the threat or enforcing the policy.
   - Why the SFR is necessary (not superfluous).
5. **Completeness argument** — demonstration that every threat and OSP in the SPD is addressed by at least one SFR. Every SFR traces to at least one SPD element.

Note that **security objectives for the TOE** are omitted. The rationale goes directly from SPD to SFRs.

## Practical guidance

### Writing a direct rationale

1. **Define the SPD as usual.** Identify [threats](./Threat.md), [OSPs](./OrganizationalSecurityPolicy.md), and [assumptions](./Assumption.md) using the guidance in [Security Problem Definition](./SecurityProblemdefinition.md). The SPD quality is even more critical in a direct rationale because there is no intermediate objectives layer to catch missing elements.

2. **Select SFRs for each SPD element.** For each threat and OSP, identify the functional components that counter or enforce it. Document the mapping in a traceability table.

3. **Write per-SFR justifications.** For each SFR, write a brief paragraph explaining:
   - The SPD element(s) it addresses.
   - The specific security behaviour it provides that counters the threat or enforces the policy.
   - Any relevant operation completions (assignments, selections) that tailor the SFR to the specific SPD.

4. **Verify completeness.** Check the traceability table for:
   - **Sufficiency:** Every threat and OSP has at least one SFR addressing it. If a threat requires multiple SFRs acting together, explain how they combine.
   - **Necessity:** Every SFR traces to at least one SPD element. If an SFR has no SPD trace, it should be removed or a rationale provided for its inclusion.

5. **Define OE objectives.** Security objectives for the [operational environment](./TOEOperationalEnvironment.md) remain mandatory, covering assumptions and any SPD elements that are not addressed by the TOE itself.

6. **Review with the evaluator.** Since the direct rationale is less common, discuss the approach with the evaluation facility (ITSEF) and certification body before submission to confirm acceptability.

### Traceability table example

| SPD element | SFRs addressing it | Justification summary |
|---|---|---|
| T.UNAUTH_ACCESS | FIA_UID.1, FIA_UAU.1, FDP_ACC.1 | User identification and authentication prevent unauthorised subjects; access control restricts authenticated users. |
| T.DATA_DISCLOSURE | FDP_IFC.1, FCS_COP.1 | Information flow control prevents leakage; cryptographic operations protect data in transit. |
| P.AUDIT_TRAIL | FAU_GEN.1, FAU_SAR.1 | Audit generation creates accountability; audit review enables detection of violations. |

## Additional resources

- CC 2022 Part 1, Section 8.4 — direct rationale approach specification.
- CC 2022 Part 1, ASE_REQ — evaluator actions for assessing direct rationale completeness and consistency.
- ISO/IEC TR 15446 — provides rationale development guidance (primarily for the standard approach, but applicable principles for direct rationale).

## Related articles

- [Rationale](./Rationale.md)
- [Security Problem Definition](./SecurityProblemdefinition.md)
- [Security Objectives](./SecurityObjective.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [Security Target](./SecurityTarget.md)
- [Protection Profile](./ProtectionProfile.md)