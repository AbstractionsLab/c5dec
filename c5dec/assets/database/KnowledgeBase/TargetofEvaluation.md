---
Last Updated: October 4, 2023
Relevant CC Version: 3.1 Revision 5, CC 2022
---

# Target of Evaluation

**Acronym:** TOE

In the context of Common Criteria the product or system that is subject of the evaluation is called the Target of Evaluation (TOE). 
In other words, the TOE is what you're trying to evaluate under the Common Criteria. It might be a whole IT product, just a part of it, a combination of several products, or even a unique technology that isn't typically available as a product. 

- **Complete IT Product**: An entire software or hardware product.
- **Part of IT Product**: A specific module or functionality within a product.
- **Set of IT Products**: A suite of related software or hardware products.
- **Unique Technology**: Specialized technologies, which might not be available to the broader market.

The physical and logical scope of the TOE is determined by the [TOE's Boundary](TOEBoundary.md). Any parts of an IT product that are not within the TOE boundary are outside the scope of the evaluation and are called *non-TOE parts of the IT product* and considered to be part of the [TOE's Operational Environment](TOEOperationalEnvironment.md).

## Practical Guidance

### Points to Ponder While Defining TOE:

1. **Functionality**: Ensure to dissect all functionalities the product is supposed to perform.
2. **Security**: Highlight and document all security aspects that are intended to be evaluated.
3. **Components**: Explicitly differentiate between what is TOE and what isn’t.
4. **External Dependencies**: Be mindful of interactions or dependencies with external components, especially those in the TOE’s Operational Environment.

### TOE Specification

In the context of the Common Criteria (CC), the Target of Evaluation (TOE) is outlined in the [Protection Profile (PP)](./ProtectionProfile.md) and/or [Security Target (ST)](./SecurityTarget.md) in terms of a TOE overview, TOE description, and TOE Reference to provide a clear, comprehensive understanding of the product or system.

- **[TOE Overview](./TOEOverview.md):** The TOE overview functions as an introductory section, offering a high-level glimpse into the TOE, and typically entails:
    - TOE Usage: A description detailing how the TOE is utilized.
    - Major Security Features: An exposition of principal security functionalities and features.
    - TOE Type: A definition or categorization of the TOE.
    - Non-TOE Hardware/Software/Firmware: Identifying any additional elements required for the TOE’s operation but not part of the evaluation.
- **[TOE Reference (ST-specific)](./TOEReference.md):** The TOE reference acts as a unique identifier, ensuring clear and unambiguous identification of the specific TOE variant being evaluated by including:
    - TOE Identifier: A unique name or label.
    - Version Information: Specific version or release details.
    - Developer/Manufacturer Information: Data pertaining to the entity responsible for the TOE’s development.
    - Additional Identifiers: Any other pertinent reference data or identifiers.
- **[TOE Description (ST-specific)](./TOEDescription.md):** This section delves into detailed information about the TOE, encompassing delineating the limits and extents of the TOE and distinguishing between what constitutes the TOE physically and logically and what lies outside of it. 
    - physical scope: a list of all hardware, firmware, software, and guidance parts that constitute the TOE.
    - logical scope: major TOE functions and brief description of the [security features](./TOESecurityFunctionality.md)
- **[TOE Summary Specification (ST-specifc):](./TOESummarySpecification.md)** This section provides a high-level description of how the TOE meets each [SFR](./SecurityFunctionalRequirement.md) through its TSF. It relates the SFRs to the actual security functions provided by the TSF, demonstrating that the implementation of the TSF satisfies the defined requirements.

### Tips for Beginners:

- Ensure that the TOE is distinctly and accurately defined to avoid ambiguity during evaluations.
- Maintain clear documentation that precisely differentiates between TOE and non-TOE components.
 
## Additional Resources

- [Understanding TOE Boundaries](./TOEBoundary.md)
- [Understandning TOE Operational Environement](./TOEOperationalEnvironment.md)
- [Common Pitfalls while defining TOE](./404.md)

## Related Articles

- [Security Target (ST)](./SecurityTarget.md)
- [Protection Profile (PP)](./ProtectionProfile.md)
