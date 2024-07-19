---
Last Updated: October 9, 2023
Relevant CC Version: 3.1 Revision 5, CC2022
---

# TOE Reference

**Acronym:** None

The TOE Reference, a vital component of the [Security Target (ST)](./SecurityTarget.md) introduction, serves to distinctly identify a [TOE](./TargetofEvaluation.md) and typically comprises the developer name, TOE name, and TOE version number.

## Practical Guidance

For a robust and clear TOE identification, the TOE Reference should not only be concise but also adequately detailed. Although the basic identification involves the developer's name, TOE name, and version, embedding additional identifiers enhances clarity and specificity:

- **Build Number & Release Date:** For detailed versioning and time-stamping the TOE status.
- **Patch Level:** Indicates the application of specific patches.
- **Configuration Details:** Offers insight into the TOE’s deployment and operational settings.
- **Hardware/Software Dependencies:** Specifies any dependent hardware or software.
- **Serial or Batch Number:** Particularly relevant for hardware TOEs, offering additional tracing capabilities.
- **Hash Values:** For software TOEs, providing a cryptographic hash of the evaluated binary can be curcial to ensure the authenticity and integrity.

These identifiers help safeguard against ambiguities and misidentifications, particularly crucial given that developers might circumvent misleading TOE reference prohibitions stipulated in subclause A.4.1 (CCv3R5 Part 1), and D.3.2.2 (CC2022 Part 1) by utilizing a product name. Thus, a thorough examination of the [TOE Overview](./TOEOverview.md) and/or [TOE Description](./TOEDescription.md) becomes imperative, ensuring that the TOE's deployment and use are not only consistent with its evaluated status but also transparently communicated to all relevant stakeholders.