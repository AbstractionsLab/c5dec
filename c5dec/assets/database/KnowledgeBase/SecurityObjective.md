---
Last Updated: October 4, 2023
Relevant CC Version: 3.1 Revision 5
---

# Security Objective

**Acronym:** SO

Security Objectives, within the context of the Common Criteria (CC), articulate the overarching security actions or attributes that are required to counter identified [threats](./Threat.md) and comply with defined [OSPs](./OrganizationalSecurityPolicy.md), as well as uphold any [assumptions](./Assumption.md) that are outlined in the [SPD](./SecurityProblemdefinition.md). Essentially, they translate the security problems into security solutions, expressed in a high-level, solution-oriented language.

Security Objectives are separated into two categories:

- **Security Objectives for the TOE:** These lay out what the [TOE](./TargetofEvaluation.md) itself must achieve to mitigate the identified threats and adhere to OSPs.
- **Security Objectives for the Operational Environment:** These detail what needs to be achieved within the [TOE’s operational environment](./TOEOperationalEnvironment.md) to support the TOE in countering threats, adhering to OSPs, and maintaining assumptions.

Each security objective should be traceable back to one or more elements of the SPD, ensuring that all identified security issues are being addressed. This traceability is typically captured in the [Security Objective Rationales](./Rationale.md), which demonstrate that the stated objectives are well-founded and suitable to address the identified security problems Moreover, they help define the [Security Functional Requirements (SFRs)](./SecurityFunctionalRequirement.md) and [Security Assurance Requirements (SARs)](./SecurityAssuranceRequirement.md) by providing a conceptual basis for what is required from the TOE and its operational environment in practical, implementable terms.

In the development of a [Security Target (ST)](./SecurityTarget.md) or a [Protection Profile (PP)](./ProtectionProfile.md), security objectives serve to bridge the gap between the high-level security issues defined in the SPD and the detailed requirements that will be applied during the evaluation of the TOE.

## Practical Guidance

1. **Identify the What, Not the How:** Clearly understand that security objectives should articulate what needs to be achieved, not how to achieve it. Ensure they are implementation-independent and don't mirror SFRs or simply restate SPD elements.
2. **Bridge the Gap:** Establish security objectives as a medium between the threats/OSPs and the semi-formalized model of SFRs, ensuring that they are set at an abstraction level that translates high-level security issues into actionable objectives.
3. **In-depth Understanding of the TOE:** Answer key questions, such as:
    - Where will the TOE be placed, and is it susceptible to physical attacks?
    - What is the principal purpose of the TOE?
    - How will the TOE be managed?
4. **Mitigation and Addressal:** Derive security objectives that concretely address identified threats and comply with OSPs. Ensure each security objective is traceable back to one or more elements in the SPD and that they collectively cover all aspects of the SPD.
5. **Iterative Refinement:** Engage in an iterative process between the security objectives, SFRs, and SPD to ensure all three components align perfectly and that the objectives aptly bridge the SPD and SFRs.
6. **Rationale Development:**
    - Ensure that all security objectives are mutually consistent and collectively exhaustive in addressing all elements of the SPD without unnecessary overlaps or gaps.
    - Formulate a security objectives rationale that clearly demonstrates how each objective addresses specific threats, policies, and assumptions from the SPD. Ensure traceability and logical coherency in the rationale.


## Additionoal Resources
- **ISO/IEC TR 15446:** This technical report provides a methodical approach to creating an SPD, guiding users through the identification of informal security requirements, threats, policies, and assumptions.
- [**BSI - The PP/ST Guide, Version 2.0**](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Zertifizierung/Interpretationen/AIS_41_BSI_PP_ST_Guide_pdf.pdf?__blob=publicationFile&v=1)
- [**Cybersecurity Certification: Candidate EUCC Scheme**](https://www.enisa.europa.eu/publications/cybersecurity-certification-eucc-candidate-scheme)
- [**Cybersecurity Act (CSA) - Article 51**](https://lexparency.org/eu/32019R0881/ART_51/)

## Related Articles

- [Security Target (ST)](./SecurityTarget.md)
- [Protection Profile (PP)](./ProtectionProfile.md)
- [Security Problem Definition](./SecurityProblemdefinition.md)
- [Rationale Definition](./Rationale.md)

