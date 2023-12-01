---
Last Updated: October 4, 2023
Relevant CC Version: 3.1 Revision 5, CC2022
---

# TSF Interface

**Acronym:** TSFI

The **TSF Interface (TSFI)** within the context of the [Common Criteria (CC)](./CommonCriteria.md) pertains to the explicit detailing and specification of all interactions that occur between the [TOE Security Functionality (TSF)](./TOESecurityFunctionality.md) and external entities, as well as between TSF parts, and between TSF parts and [non-TSF parts](./NonTSFPart.md) within the TOE. Defined under the Development (ADV) class, particularly the Functional Specification (ADV_FSP) family, the TSFI is critical in describing how the TSF interacts and communicates, ensuring that all interactions are secure, controlled, and aligned with the [Security Functional Requirements (SFRs)](./SecurityFunctionalRequirement.md). Specifically, TSFI can be:

- **SFR-Enforcing:** if services accessible through the interface can be directly traced to SFRs.
- **SFR-Supporting:** interfaces that facilitate services that are not directly traced to SFRs but are essential for the functionality of SFR-enforcing services.
- **SFR Non-Interfering:** interfaces that have no impact on or interaction with SFR-enforcing functionality.

## Practical Guidance

### Ensuring Traceability to SFRs
One of the pivotal requisites in defining and detailing TSFI is establishing an explicit and clear traceability to the SFRs, ensuring that each interface either enforces, supports, or does not interfere with the defined security functional requirements. The ability to draw a coherent line from the TSFI to SFRs is not only essential for establishing a robust security architecture but also imperative to fulfill CC validation requirements.

### Detailed Specifications
To adequately define and evaluate TSFI, consider incorporating the following detailed attributes:
- **Purpose:** Define the general functionalities it is designed to manage or facilitate.
- **Method of Use:** Define how the interface is used, detailing available interactions and behaviors across interfaces.
- **Parameters:** Identify and list inputs and outputs that govern the interface’s behaviors.
- **Parameter Descriptions:** Provide comprehensive definitions of parameters, clarifying their role and importance.
- **Actions:** Describe functionalities executed by the interface, indicating how these actions relate to SFRs or otherwise.
- **Error Messages:** Detail conditions and methods under which error messages are generated and classified, differentiating between direct, indirect, and remaining errors.

## Additional Resources

- **CC Part 3: Security Assurance Requirements**: Providing detailed insight into ADV_FSP and the specification of the TSFI within the CC framework.

## Related Articles

- [TOE Security Functionality (TSF)](./TOESecurityFunctionality.md)
- [Security Functional Requirements (SFRs)](./SecurityFunctionalRequirement.md)
