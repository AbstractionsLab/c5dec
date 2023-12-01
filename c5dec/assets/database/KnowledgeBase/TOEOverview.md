---
Last Updated: October 9, 2023
Relevant CC Version: 3.1 Revision 5, CC2022
---

# TOE Overview

**Acronym:** None

The TOE Overview, positioned in the [Protection Profile (PP)](./ProtectionProfile.md) or [Security Target (ST)](./SecurityTarget.md) Introduction provides a succinct and clear description of the [TOE](./TargetofEvaluation.md) aimed at potential consumers and, in the context of a PP, developers. When part of a PP, the overview typically describes an implementation-independent TOE Type, while within an ST, it outlines a specific TOE implementation. This section is tailored to assist those who are exploring TOEs or TOE Types that align with their security requirements and are compatible with their hardware, software, and/or firmware environments. 

*CC2022 specific*

For [multi-assurance](./MultiAssuranceEvaluation.md) STs, the TOE Overview also delineates the [TOE Security Functions (TSFs)](./TOESecurityFunctionality.md) organization into [sub-TSFs](./SubTOESecurityFunctionality.md), concretely defined in the [PP-Configuration](./PPConfiguration.md) to which the ST [claims conformance](./ConformanceClaim.md). Consequently, the TOE Overview serves as a pivotal section, articulating the TOE or TOE Type concerning its type, usage, principal security features, and notable dependencies, offering a focused and comprehensive snapshot imperative for evaluating its suitability and compliance with both consumer and developer needs.

## Practical Guidance

The TOE Overview, describes the TOE in terms of its usage and major security features, the TOE Type, alongside any required non-TOE hardware/software/firmware. 

### Reading a TOE Overview:

1. **Commence with the TOE Overview:**
   - Begin by reading the TOE Overview in a PP or ST as it offers an initial understanding of potential TOEs for your needs and informs about their compatibility with certain hardware, software, and firmware.

2. **Understand Three Key Sections:**
   a. **Usage and Major Security Features:** 
      - Gain a general insight into the TOE’s capabilities and applicability in a security context without delving into technical depths.
      - This segment should be consumer-friendly and non-technical, providing a general, non-exhaustive overview.
   b. **TOE Type:** 
      - Identify the broad category to which the TOE belongs (e.g., firewall, LAN, etc.).
      - Heed any warnings about expected functionalities or usage environments that the TOE does not support, as these might be pivotal in your decision-making process.
   c. **Required Non-TOE Hardware/Software/Firmware:** 
      - Identify essential external components needed to utilize the TOE, ensuring these elements align with your infrastructure and policies without necessitating exhaustive details.

3. **Cautious Consideration:**
   - Especially note any warnings or limitations mentioned in the TOE type section, weighing their impact against your operational needs and determining the TOE’s viability accordingly.

### Writing a TOE Overview:

1.** Summarizing Usage & Security Features (ASE_INT.1.4C)**
- Provide a brief, non-technical summary of TOE usage and main security features.
- Ensure consistency and explicit identification of evaluated/non-evaluated features across the ST.
- In composed TOEs, focus on the overall TOE, not individual components.
2. **Identifying TOE Type (ASE_INT.1.5C)**
- Clearly identify the TOE type and ensure it is not misleading.
- Discuss any absent functionality or operational environment limitations explicitly.
3. **Specifying Non-TOE Hardware/Software/Firmware (ASE_INT.1.6C)**
- Identify and briefly describe any non-TOE hardware, software, or firmware required.
- Ensure clarity for consumers regarding what is needed for TOE operation.
4. **Describing TSF Organization for Multi-Assurance STs (ASE_INT.1.7C)** [If applicable]
- Detail the TSF organization according to sub-TSFs defined in the related PP Configuration.
- Integrate any specific actual TOE details if relevant.

#### Quick Tips for TOE Overview Writing
- **Clarity:** Keep language clear and accessible for consumers.
- **Transparency:** Be explicit and transparent about TOE limitations and non-supported functionalities.
- **Consistency:** Maintain consistency in information and descriptions throughout the ST.

This compact guide centralizes the fundamental aspects of writing a TOE Overview compliant with evaluator actions and work units outlined in the Common Criteria (CC) Part 3, balancing evaluation adherence with consumer-friendliness and information accessibility.

## Additional Resources

- **CC Part 1 and Part 3**
- **ISO/IEC TR 15446**

## Related Articles

- [Security Target](./SecurityTarget.md)
- [Protection Profile](./ProtectionProfile.md)
- [Multi-Assurance Evaluation](./MultiAssuranceEvaluation.md)
- [Single-Assurance Evaluation](./SingleAssuranceEvaluation.md)