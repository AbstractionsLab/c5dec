---
Last Updated: October 4, 2023
Relevant CC Version: 3.1 Revision 5
---

# Security Problem Definition

**Acronym:** SPD

The **Security Problem Definition** (SPD) stands as a pivotal component within each [Protection Profile](./ProtectionProfile.md) and [Security Target](./SecurityTarget.md), anchoring the foundational understanding of the security context in which the [TOE](./TargetofEvaluation.md) operates. It rigorously elucidates the security challenges that the TOE seeks to navigate and provides a structured description of them via the lens of [threats](./Threat.md) to [assets](./Asset.md), adherence to [organizational security policies](./OrganizationalSecurityPolicy.md), and [assumptions](./Assumption.md) pertaining to the [operational environment](./TOEOperationalEnvironment.md).

An effectively constructed SPD not only lends clarity to the evaluative context but also, significantly influences the utility of evaluation results. The CC, while emphasizing the pivotal role of the SPD, abstain from defining a structured process for its derivation, effectively treating the SPD as axiomatic. Nevertheless, ISO/IEC TR 15446, through its Clause 9, proposes a high-level framework that can guide the structuring of an SPD. 

## Practical Guidance

Following the high-level framework proposed in ISO/IEC TR 15446, here's a step-by-step guide to deriving an SPD:

1. **Informal Security Requirement Analysis:** Begin by capturing and validating general security needs. This could be through stakeholder interviews, risk assessments, and reviewing existing security documentation.
2. **Risk and Threat Analysis:** Implement a robust and synchronized risk and threat analysis, ensuring that the identification of threats and the assessment of associated risks are both comprehensive and relevant.
    - Threat Identification: Detail all conceivable threats related to the TOE, ensuring they are rooted in realistic and relevant scenarios.
    - Risk Assessment: Evaluate the risks associated with each identified threat, considering both the likelihood of occurrence and the potential impact on assets.
    - Risk Treatment: Determine how each identified risk will be managed – whether through mitigation, transfer, acceptance, or avoidance, and detail the rationale behind these decisions.
    - Correlation and Relevance: Establish and document clear links between identified threats and assets, ensuring that the relevance and impact of each threat are clearly defined.
3. **Policy Documentation:** List and detail any organizational, regulatory, or industry-specific policies that need to be considered for the TOE and its environment.
4. **Assumption Recording:** Clearly specify any assumptions regarding the TOE's operational environment. These could be about the user base, network conditions, hardware specifications, or even geographical locations.
5. **SPD Specification Check:** After drafting the SPD, review for completeness, clarity, and relevance. Engage different stakeholders for feedback, ensuring the SPD addresses all their concerns.

## Tips for Beginners

- **Start Broad, Then Narrow Down:** Begin your SPD with a wide perspective, capturing all potential concerns. Later, refine these into specific, actionable items.
- **Engage Multiple Stakeholders:** Ensuring their concerns and perspectives are considered even in the technical aspects of the SPD.
- **Stay Updated:** The threat landscape is ever-evolving. Regularly review and update the SPD, especially after significant changes in the organization or industry.
- Leverage existing SPD examples and templates to guide your initial efforts in crafting an SPD.
- Work closely with security analysts to understand common threats and to ground your SPD in realistic scenarios.

## Additional Resources

- **ISO/IEC TR 15446:** This technical report provides a methodical approach to creating an SPD, guiding users through the identification of informal security requirements, threats, policies, and assumptions.
- **Common Threat Databases:** Websites like the Common Vulnerabilities and Exposures (CVE) can provide insights into prevalent threats and vulnerabilities.
- [**BSI - The PP/ST Guide, Version 2.0**](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Zertifizierung/Interpretationen/AIS_41_BSI_PP_ST_Guide_pdf.pdf?__blob=publicationFile&v=1)
- **ENISA Interoperable EU Risk Management Toolbox:**

## Related Articles

- [Protection Profiles and Their Role](./ProtectionProfile.md)
- [In-depth Exploration of Security Targets](./SecurityTarget.md)
- [Identifying Threats](./Threat.md)
- [Organizational Security Policies](./OrganizationalSecurityPolicy.md)
- [Assumptions](./Assumptions.md)
- [Threat Modeling](./ThreatModeling.md)