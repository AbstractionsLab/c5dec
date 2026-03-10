---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022
Tags: EUCC, certification-scheme, EU-Cybersecurity-Act, ENISA, SOG-IS
---

# EUCC

**Acronym:** EUCC (European Common Criteria-based cybersecurity certification scheme)

The **EUCC** is the first cybersecurity certification scheme adopted under the EU Cybersecurity Act (Regulation (EU) 2019/881). It builds upon the established Common Criteria (CC) and Common Evaluation Methodology (CEM) frameworks to provide a harmonised, EU-wide scheme for certifying ICT products. The EUCC replaces the patchwork of national CC-based schemes that previously operated under the SOG-IS Mutual Recognition Agreement (MRA) and introduces two assurance levels — **substantial** and **high** — aligned with the EU Cybersecurity Act's assurance framework.

The scheme is managed by ENISA (European Union Agency for Cybersecurity), with evaluation performed by accredited IT Security Evaluation Facilities (ITSEFs) and certificates issued by national Cybersecurity Certification Authorities (CCA).

## Assurance levels

The EUCC maps CC assurance levels to the EU Cybersecurity Act's two-level framework:

| EUCC level | CC mapping | Description |
|---|---|---|
| **Substantial** | EAL1–EAL4 (+ augmentations) | Provides confidence that the product handles known risks of incidents and cyberattacks. Suitable for most commercial ICT products. |
| **High** | EAL4+ through EAL7 (with AVA_VAN ≥ 4) | Provides confidence that the product handles advanced cybersecurity risks, including risks from actors with significant skills and resources. Required for high-security environments. |

### Key rules

- **Substantial** evaluations may use EAL1 through EAL4, with or without augmentation, and must use AVA_VAN.1 through AVA_VAN.3.
- **High** evaluations require at least AVA_VAN.4 (or AVA_VAN.5), typically with EAL4+ or higher. High-level evaluations must be performed by ITSEFs specifically accredited for high-level evaluations.
- [Protection Profiles](./ProtectionProfile.md) certified under EUCC establish domain-specific requirements. Many EUCC evaluations require conformance to an approved PP.

## Scope of EUCC

The EUCC covers ICT products including:
- Hardware and software components (smartcards, secure elements, operating systems, network devices).
- Products for which an applicable certified [Protection Profile](./ProtectionProfile.md) exists.
- Products without a PP, provided the assurance level and scope are agreed with the CCA.

The scheme does not cover ICT services or ICT processes — these fall under separate EU certification schemes (EUCS for cloud services, EU5G for 5G security).

## Evaluation process under EUCC

The EUCC evaluation follows the standard CC/CEM process with additional scheme-specific requirements:

1. **Application.** The applicant (typically the vendor) submits a certification request to a CCA, referencing the applicable PP (if any) and the target assurance level.
2. **ITSEF selection.** The evaluation is performed by an accredited ITSEF. For high-level evaluations, the ITSEF must hold specific accreditation.
3. **Evaluation.** The ITSEF conducts the CC/CEM evaluation, following any additional scheme guidance (e.g., supporting documents, EUCC-specific interpretations).
4. **ETR and certification report.** The ITSEF produces an [Evaluation Technical Report](./EvaluationTechnicalReport.md). The CCA reviews the ETR and issues a certification decision.
5. **Certificate and listing.** Issued certificates are published in the EU Trust Services Dashboard and the EUCC certificate registry.
6. **Maintenance and monitoring.** Certificates have a defined validity period (typically 5 years). The certificate holder must report vulnerabilities and perform maintenance activities.

## Relationship to SOG-IS MRA

The SOG-IS Mutual Recognition Agreement was the previous European scheme for CC mutual recognition. Key differences with EUCC:

| Aspect | SOG-IS MRA | EUCC |
|---|---|---|
| Legal basis | Voluntary agreement between national schemes | EU Regulation (legally binding) |
| Scope | Participating EU/EEA states only | All EU member states |
| Assurance ceiling | Up to EAL4 (general) or EAL7 (technical domains) | Substantial (EAL1-4), High (EAL4+ to EAL7) |
| PP regime | SOG-IS-approved PPs | EUCC-certified PPs |
| Governance | SOG-IS Management Committee | ENISA + European Cybersecurity Certification Group (ECCG) |

> The SOG-IS MRA continues to operate during the EUCC transition period. Certificates issued under SOG-IS remain valid until their expiry.

## Practical guidance

### Preparing for EUCC certification

1. **Determine the applicable PP.** Check the EUCC PP registry for PPs relevant to the product category. If a certified PP exists, conformance is typically mandatory.
2. **Select the assurance level.** Choose substantial or high based on the product's risk profile, market requirements, and regulatory obligations (e.g., products for critical infrastructure may require high).
3. **Engage an ITSEF early.** Accredited ITSEFs can provide pre-evaluation consultancy to identify evidence gaps before formal evaluation begins.
4. **Prepare evaluation evidence.** Follow the [evaluation evidence](./EvaluationEvidence.md) requirements for the target EAL. EUCC may impose additional evidence requirements through scheme-specific supporting documents.
5. **Draft the Security Target.** Ensure the [Security Target](./SecurityTarget.md) conforms to the PP (if applicable) and meets EUCC requirements for the target assurance level.
6. **Plan for maintenance.** Budget for ongoing vulnerability monitoring, patch management, and certificate maintenance activities.

### Transitioning from SOG-IS to EUCC

1. Review existing SOG-IS certificates to determine their expiry dates and plan re-certification under EUCC where needed.
2. Identify differences between SOG-IS and EUCC scheme requirements (particularly around vulnerability handling and certificate maintenance).
3. Engage with the relevant CCA for guidance on the transition timeline and any transitional recognition arrangements.

## Additional resources

- Implementing Regulation (EU) 2024/482 — the EUCC scheme implementing act.
- EU Cybersecurity Act (Regulation (EU) 2019/881) — framework regulation establishing EU cybersecurity certification.
- ENISA EUCC Documentation — scheme rules, supporting documents, and PP registry.
- SOG-IS Crypto Evaluation Scheme — supplementary crypto guidance applicable to EUCC high-level evaluations.

## Related articles

- [Evaluation Methods](./EvaluationMethods.md)
- [Evaluation Assurance Levels](./EvaluationAssuranceLevel.md)
- [Protection Profile](./ProtectionProfile.md)
- [Attack Potential](./AttackPotential.md)
- [Evaluation Technical Report](./EvaluationTechnicalReport.md)
- [Composite Evaluation](./CompositeEvaluation.md)
- [Package](./Package.md)
