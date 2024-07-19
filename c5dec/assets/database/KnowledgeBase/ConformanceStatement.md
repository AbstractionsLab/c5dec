---
Last Updated: October 4, 2023
Relevant CC Version: 3.1 Revision 5, CC2022
---

# Conformance Statement

The Conformance Statement describes the manner in which an ST shall conform. The CC permits a conformance statement to be either exact, strict, or demonstrable.

## Exact conformance
  - The notion of exact conformance was introduced in the latest release of the Common Criteria (CC:2022). Exact conformance requires the ST claiming conformance to be an exact instantiation of the conformity enforcing PP(s), or PP-Configuration, i.e., that it contains all statements (SPD, Security Objective, and SFRs) without including any additional functionality.
  - For SFRs the following applies:
    - Selection-based SFRs in the PPs or PP-Modules shall be excluded if the selection that requires their inclusion is not chosen by the ST author;
    - Optional SFRs in the PPs or PP-Modules may be included or excluded while maintaining its exact conformance claim.
  - If a PP, PP-Configuration requires exact conformance it shall include an Allowed-with Statement that states which other PPs or PP-Configurations are allowed to be included in a conformance claim along with the PP.
## Strict conformance
  - Strict conformance requires that ST claiming conformance is an instantiation of the PP(s), or PP-Configurations though it can be broader, i.e., that it contains all statements (SPD, Security Objective, and SFRs) that are in the conformance enforcing document but can contain additional elements. Strict conformance is expected to be used for stringent requirements that are to be adhered to in a single manner.
## Demonstrable conformance
  - Demonstrable conformance means that ST claiming conformance to the PP(s), or PP-Configurations has to offer a solution to the generic security problem described in the conformance enforcing document(s), but can do so in any way equivalent or more restrictive to that described. More precisely, if demonstrable conformance is required, the ST shall contain an SPD, set of security objectives, and a set of SFRs that are equivalent to a superset of the enforcing document’s SPD, security objectives, and SFRs, where the new assumptions (if any) do not weaken the original SPD, and where the set of the ST’s SFRs imply the original SFRs.


1.  [Conformance Types]
        1.  [Exact]
            1.  [Allowed-with Statement]
            2.  [Exact conformance - FAQ](./Exactconformance-FAQ.md)
        2.  [Strict]
        3.  [Demonstrable]