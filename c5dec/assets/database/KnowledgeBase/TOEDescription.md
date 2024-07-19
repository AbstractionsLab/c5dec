---
Last Updated: October 9, 2023
Relevant CC Version: 3.1 Revision 5, CC2022
---

# TOE Description

**Acronym:** None

The TOE (Target of Evaluation) Description, embedded within the [Security Target (ST)](./SecurityTarget.md) Introduction, serves as a narrative exposition that navigates a middle ground, offering more detail than the [TOE Overview](./TOEOverview.md) while not delving as deep as the [TOE Summary Specification (TSS)](./TOESummarySpecification.md). It furnishes a panoramic view of the [TOE](./TargetofEvaluation.md), elucidating its inherent security functionalities and potentially exploring its applicability within a broader application context. The TOE Description meticulously parses through both the physical and logical scopes of the TOE. The physical scope delineates all constituent parts of the TOE, encapsulating hardware, firmware, software, and guidance parts, while the logical scope ventures into delineating major TOE functionalities and succinctly describing the [security features](./TOESecurityFunctionality.md). Intrinsically, the TOE Description is crafted to extirpate ambiguity, ensuring that the demarcation between what is enveloped within the TOE and what lies outside is lucidly clear and indisputable, thereby offering a coherent comprehension of the TOE’s capabilities and boundaries to evaluators and potential consumers.

For [composed TOEs](./ComposedTOE.md), the description will also delve into the composed solution, discussing the physical and logical scopes, and identifying the logical boundaries between components. The role of each component in providing security functionality is also specified.

## Practical Guidance

### Reading a TOE Description

For consumers seeking confidence in a TOE’s evaluated security features, the TOE Description emerges as an essential part of every ST, furnishing a detailed exposition of both its physical and logical security functionalities. Regarding the physical scope,all hardware, firmware, software, and guidance parts of the TOE are enumerated, providing not only their identifiers and formats but also their delivery mechanisms, ensuring that consumers are well-informed about each constituent part and its availability. 
In parallel, the logical scope gives consumers a clear picture of the TOE's security features, elucidating them to a degree that allows a general understanding. 
This detailed breakdown, coupled with clarifications on the evaluated TOE configurations, eliminates ambiguities regarding what is included in the TOE and hence in the evaluation. 

Particularly for composed TOEs, the TOE Description provides clarity on which features of individual components are encapsulated in the evaluated TOE, assuring that consumers can make enlightened decisions based on the actual evaluated security functionalities and configurations. Consequently, a careful reading of the TOE Description is indispensable for affirming that desired features and parts have been subjected to rigorous evaluation, thereby facilitating an informed selection and implementation of the TOE.

### Writing a TOE Description

1. Define the TOE’s Physical Scope 
**Objective:** Clearly detail all physical constituents of the TOE.
- **List All Components:** Enumerate all hardware, firmware, and software parts.
- **Detail Component Identifiers:** Include unique identifiers and formats (e.g., binary, *.pdf, etc.)
- **Describe Delivery Methods:** Outline how each part is made available to the consumer (e.g., download link, physical delivery, etc.)
- **Clarify Evaluated Configurations:** Provide descriptions and identifications of configurations evaluated, especially when multiple configurations are possible.
2. Outline the TOE’s Logical Scope
**Objective:** Present a detailed depiction of the TOE's logical security functionalities.
- **Detail Security Features:** Describe the TOE's logical security features with sufficient detail for general understanding.
- **Be Explicit About Included Features:** Ensure clarity about what logical security features are offered by the TOE.
**Note:** In cases where an ST for a composed TOE is being developed, highlight which features of individual components are not within the composed TOE, and ensure clarity about the logical features that have been evaluated.
3. Contextualize the TOE
- **Position Within a Larger Context:** Describe how the TOE fits into a broader application or security context. This may provide clarity to consumers about its application and integration.
- **Address User Needs:** Ensure that the TOE Description serves as a reliable reference for consumers to understand which features have been evaluated.
4. Ensure Clarity and Lack of Ambiguity
- **Avoid Misunderstandings:** Make sure that each part and feature is clearly identified as either being inside or outside the TOE. Eliminate any ambiguity.
- **Provide Sufficient Detail:** Offer a level of detail that ensures readers can develop a broad understanding of the TOE's components and features without becoming bogged down in technicalities.
5. Review and Validate
- **Consumer-Centric Validation:** Ensure that the TOE Description aids consumers in affirming that the security features they intend to utilize have been evaluated.
- **Evaluator-Friendly:** Facilitate the evaluators' work by clearly detailing what is included in the TOE, adhering to clarity and comprehensiveness.

Creating a detailed and clear TOE Description is critical for ensuring that the evaluation of a product or system is both transparent and verifiable. This guide provides a structured approach to crafting a TOE Description that ensures both evaluators and consumers can discern what is part of the evaluation or what has been evaluated, facilitating confidence and informed decision-making. Always aim for clarity and completeness to ensure the TOE Description is both reliable and valid.


## Additional Resources

- **CC Part 3**
- **ISO/IEC TR 15446**

## Related Articles

- [Security Target (ST)](./SecurityTarget.md)
- [Target of Evaluation (TOE)](./TargetofEvaluation.md)
- [TOE Security Functionality](./TOESecurityFunctionality.md)