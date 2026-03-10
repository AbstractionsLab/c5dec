---
Last Updated: October 4, 2023
Relevant CC Version: 3.1 Revision 5, CC2022
---

# TOE Security Functionality

**Acronym:** TSF

 The TOE Security Functionality (TSF) within the context of the Common Criteria refers to a set of security-specific functions, mechanisms, and features that the [TOE](./TargetofEvaluation.md) implements to comply with the identified [security objectives](./SecurityObjective.md) and [requirements](./SecurityFunctionalRequirement.md). It represents the embodiment of all hardware, software, and firmware within the TOE that must be relied upon for the correct enforcement of the security objectives. Essentially, the TSF is responsible for the implementation of the security objectives that mitigate the identified [threats](./Threat.md), uphold [organizational security policies (OSPs)](./OrganizationalSecurityPolicy.md), and maintain environmental [assumptions](./Assumption.md). Depending on the TOE’s architecture, the TSF may represent the entirety of the TOE or a specific component thereof. If it only represents a portion, safeguarding measures must be instituted to ensure non-TSF parts do not manipulate or bypass the TSF, jeopardizing the fulfillment of security objectives. Notably, security objectives prescribed for the operational environment can augment the TSF by providing additional supportive functionalities.

## Practical Guidance

A TSF fundamentally represents the practical realization of security within the TOE, transmuting identified Security Functional Requirements (SFRs) into tangible security controls, mechanisms, and features. A TSF is intrinsically linked to and derived from the various hierarchical elements of the [Protection Profile](./ProtectionProfile.md) and/or [Security Target](./SecurityTarget.md), cascading from the [Security Problem Definition (SPD)](./SecurityProblemdefinition.md) down through Security Objectives (SOs), and SFRs.

In essence, a TSF serves as the actual implementation of the specified SFRs, translating the theoretical and policy-level security necessities into concrete, enforceable security functionalities within the TOE. It emerges at the terminal point of a logical flow that spans:

- **SPD:** Initial identification of threats, assumptions, and OSPs.
- **SOs:** High-level security outcomes and objectives derived from the SPD.
- **SFRs:** Detailed, standardized requirements that embody the practical realization of the SOs.
- **TSF:** The physical and logical embodiment of the SFRs within the TOE, ensuring the realized security attributes and mechanisms adhere to the initially identified security objectives.


The description and definition of the TSF are inherently multifaceted and spread across various domains, each contributing to a comprehensive understanding and depiction.
- **TOE Design and Functional Specification:** The TOE Design, as required by ADV_TDS, identifies the actual parts that make up the TSF. Once the TSF has been defined in terms of constituting components, the [TSF Interfaces](./TSFInterface.md) are identified and described in accordance with the requirements stated in ADV_FSP Functional Specification.
- **Implementation Representation:** Adhering to ADV_IMP, the transition from TSF design to physical implementation within the TOE is meticulously mapped and verified.
- **Security Architecture:** In accordance with ADV_ARC, the TSF ensures unassailable architectural robustness, safeguarding [domain separation](./DomainSeparation.md), [self-protection](./SelfProtection.md), and preventing [bypassing](./NonBypassability.md) of security functionalities.
- **Internal Structuring:** Through ADV_INT, the internal structuring of the TSF is highlighted, emphasizing principles like modularity and layering, which contribute to robust, secure, and maintainable implementations.
- **Security Policy Model:** (If applicable) The ADV_SPM puts forth a model encapsulating the security policies that the TSF enforces, providing an abstracted view that maps to functional specifications, thereby enhancing understanding and verifiability.

## Additional Resources

- CC Part 3: Class ADV Development, Annex A

## Related Articles
- [Security Functional Requirement (SFR)](./SecurityFunctionalRequirement.md) 
- [Security Target](./SecurityTarget.md)
