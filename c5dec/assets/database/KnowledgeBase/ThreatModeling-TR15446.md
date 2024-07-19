---
Last Updated: October 11, 2023
Relevant CC Version: 3.1 Revision 5
---

# Threat Modeling in the Context of ISO/IEC TR 15446

**Acronym:** None

In the formulation of a Security Problem Definition (SPD), threat modeling stands out as a pivotal component. Within ISO/IEC TR 15446, threat modeling is underscored as a methodical approach to identify, analyze, and prioritize potential threats to the Target of Evaluation (TOE). This involves a rigorous analysis phase where threats are systematically identified, followed by detailed documentation to serve as a foundational element of the SPD.

## Practical Guidance

Developing an adept threat model following TR 15446 involves:

1. **Threat Identification:**
   - **Asset Identification:** Recognize and categorize assets within the TOE and its operational environment.
   - **Threat Agents:** Identify potential attackers, considering capabilities, intentions, and targets.
   - **Attack Vectors:** Determine the potential pathways or methods that threat agents may employ.
   
2. **Threat Analysis:**
   - **Attack Tree Analysis:** Develop attack trees to visualize different paths an attacker might utilize to compromise assets.
   - **Weakness Analysis:** Identify and analyze vulnerabilities or weak points within the TOE that might be exploited.
   
3. **Threat Documentation:**
   - **Clear Descriptions:** Provide detailed, clear, and comprehensive descriptions of each threat.
   - **Prioritization:** Based on potential impact and likelihood, prioritize threats to guide focused mitigation efforts.
   
4. **Integration into SPD:**
   - **Alignment:** Ensure threats are aligned with assets, organizational policies, and environmental assumptions.
   - **Inclusion of Mitigation:** Detail any existing or planned mitigation strategies or security controls against each threat.
   
## Tips for Beginners

- **Collaborative Approach:** Engage stakeholders from various domains (IT, business, compliance, etc.) to ensure a comprehensive threat model.
- **Use of Tooling:** Employ threat modeling tools to document and analyze identified threats and attack paths systematically.
- **Consistent Review:** Post-implementation, continuously review and update the threat model in response to changes in the environment or emerging threat vectors.

## Additional Resources

- **ISO/IEC TR 15446:** Dive deep into its guidelines to understand nuanced aspects of conducting a detailed threat analysis.
- **Threat Modeling Tools:** Explore tools that facilitate systematic threat modeling, analysis, and documentation.
- **Industry Threat Reports:** Utilize reports and whitepapers from cybersecurity organizations to stay abreast of emerging threats.

## Related Articles

- [Security Problem Definition (SPD)](./SecurityProblemDefinition.md)
- [Understanding and Managing Assets](./Asset.md)
- [Navigating through Organizational Security Policies](./OrganizationalSecurityPolicy.md)


---
Last Updated: October 11, 2023
Relevant CC Version: 3.1 Revision 5
---

# Security Problem Definition and Methodology according to ISO/IEC TR 15446

**Acronym:** SPD

ISO/IEC 15408 provides flexibility in the approach toward creating a Security Problem Definition (SPD). It does not stipulate a particular methodology but allows for various processes to be employed in defining the SPD. However, for those unfamiliar with preparing Protection Profiles (PPs) and Security Targets (STs), ISO/IEC TR 15446 offers a seasoned and pragmatic methodology, valid across numerous organizations and environments. 

ISO/IEC TR 15446 emphasizes utilizing the outcomes from a security risk assessment as a pivotal source for comprehending a security problem and formulating the SPD. This approach not only strives for comprehensiveness but also introduces the element of proportionality, identifying both acceptable and unacceptable risks, and enabling adaptable modifications through design trades based on the implementational and evaluational complexity of required controls.

## Practical Guidance

Based on ISO/IEC TR 15446, develop the SPD by:

1. **Identifying and Confirming the Informal Security Requirement:**
   - Acknowledge existing informal security needs, which might be unwritten or informally discussed among stakeholders.
   - Secure confirmation from management and stakeholders that identified requirements genuinely represent their security needs.

2. **Identifying and Specifying Threats via Formal Threat Analysis:**
   - Perform a rigorous analysis to identify potential threats and their impacts on identified assets.

3. **Documenting Applicable Policies and Assumptions:**
   - Clearly detail relevant organizational security policies and assumptions regarding the operational environment.

4. **Finalising and Checking the SPD Specification:**
   - Ensure the finalized SPD aligns accurately with the previously established and confirmed informal requirement.

In addition, the methodology embeds two supplementary aspects that, while not mandatory per ISO/IEC 15408, have proven beneficial in practice:

- **Documenting Discounted Threats:**
   - Detail threats that might or might not apply to the product but, if pertinent, would be countered by security functionality integrated into the TOE for varied reasons.

- **Producing a Rationale:**
   - Establish a coherent rationale that maps the SPD back to the informal security requirement, ensuring traceability and justifiability of the formalized SPD.

## Tips for Beginners

- **Informal Requirement Identification:** Engage stakeholders through workshops or interviews to elicit potential informal security requirements.
- **Inclusivity:** Ensure that all discounted threats and applicable policies are exhaustively explored and documented to mitigate future challenges or overlooked aspects.
- **Iteration:** Recognize that SPD development might necessitate iterative processes to refine and validate the documented requirements and threats.

## Additional Resources

- **ISO/IEC TR 15446:** Investigate its methodological insights and step-by-step guidance for a deeper, contextual understanding of SPD formulation.
- **Threat Modeling Tools:** Utilize available tools to facilitate threat identification and analysis processes in a systematic manner.

## Related Articles

- [Formulating the Security Target (ST)](./SecurityTarget.md)
- [Developing the Protection Profile (PP)](./ProtectionProfile.md)
- [Understanding and Managing Assets](./Asset.md)


## Practical Guidance

### Utilizing Security Risk Assessment Findings

1. **Leveraging Proportionality:**
   - Assess risks considering their likelihood and significance of loss.
   - Identify acceptable and unacceptable risks, facilitating adaptable security problem modifications.

2. **Employing Informed Decision Making:**
   - After gathering and validating all information, segregate it into:
     a) Attacks the product must counteract.
     b) Essential security attributes or features.
     c) Non-essential security attributes or features.

   - Understand that these distinctions guide varied treatments in subsequent development stages:
     - **Attacks:** Treated as threats and need to be countered.
     - **Essential Features:** Correspond to organizational security policies (OSPs).
     - **Non-Essential Features:** Align with assumptions.

### Integrating the Risk Assessment into SPD Development

Ensure the risk assessment findings are intricately woven into the SPD development process, offering a robust foundation to define and differentiate between potential threats, obligatory security attributes, and assumptive attributes. 

## Tips for Beginners

- **Leverage Existing Resources:** Maximize the use of available risk assessment results to guide the SPD development.
- **Collaborate with Risk Teams:** Engage with risk assessment teams to gain insights into the identified risks and mitigation strategies.
- **Iterative Validation:** Regularly verify for inconsistencies in collated information, ensuring a coherent and accurate SPD.

## Additional Resources

- **Security Risk Assessment Methodologies:** Explore and utilize standardized methodologies to facilitate a thorough and proportional risk assessment.
- **ISO/IEC TR 15446:** A deeper dive will offer further detailed methodological insights.

## Related Articles

- [Understanding and Addressing Threats](./Threat.md)
- [Formulating and Applying Organizational Security Policies (OSPs)](./OrganizationalSecurityPolicy.md)
- [Developing and Validating Assumptions](./Assumption.md)
