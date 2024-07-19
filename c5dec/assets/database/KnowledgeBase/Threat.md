---
Last Updated: October 4, 2023
Relevant CC Version: 3.1 Revision 5
---

# Threat

**Acronym:** T

In the domain of cybersecurity and within the context of [Security Problem Definition (SPD)](./SecurityProblemdefinition.md), threats are potential occurrences that could exploit [vulnerabilities](./Vulnerability.md) to adversely impact [assets](./Asset.md). Threats may intentionally or unintentionally compromise the confidentiality, integrity, or availability of assets, thus posing a risk to the [Target of Evaluation (TOE)](./TargetofEvaluation.md) and its [operational environment](./TOEOperationalEnvironment.md).
Threats are indispensable in formulating the [Security Problem Definition](./SecurityProblemDefinition.md) (SPD).

## Practical Guidance

### Identification and Analysis of Threats

Threat identification is a fundamental aspect of risk and threat analysis, acting as a precursor to conducting meaningful risk assessments and formulating security controls. Given the CC's asset-centric nature, threats are identified relative to assets. Once assets are identified, an orderly approach to discerning relevant threats involves iterating through all assets and adhering to the following steps:

1. **Threat Source Identification:**
   - _Adversarial:_ Consider intentional entities like hackers.
   - _Non-Adversarial:_ Include non-intentional sources like system errors.
2. **Threat Event Characterization:** Describe potential adverse events from each source and their impacts.
3. **Utilize Threat Intelligence:** Leverage databases and forums for recognized threats.
4. **Regulatory Consultation:** Explore guidelines from cybersecurity bodies.
5. **Stakeholder Collaboration:** Employ insights from various stakeholders.
6. **Articulation into Security Objectives:** Ensure that for each threat an actionable [security objective](./SecurityObjective.md) are defined in the [Security Target (ST)](./SecurityTarget.md) or [Protection Profile (PP)](./ProtectionProfile.md). These security objectives should offer a clear, solution-oriented representation, elucidating how the TOE, its operational environment, or the combination of both, will concretely counter or mitigate the identified threat.

### Documentation of Threats

In the context of CC, threats must be described as adverse actions executed by [threat agents](./ThreatAgent.md) to compromise an asset, as shown in the example below.

**T.COMPROMISEDCOMMUNICATION**

A network attacker may gain unauthorised logical access to communication channels in order to
disclose or modify data exchanged between parts of the TOE and remote external entities.

- **Threat Agent:** a network attacker
- **Adverse Action:** unauthorised logical access to communication channels
- **Asset:** data exchanged betweent parts of the TOE and remote external entities

*Extracted from the Protection Profile Mobile Device Management - Trusted Server, BSI-CC-PP-0115, Version 1.0.

### Techniques for Threat Analysis:

- **Threat Modeling:** Utilize strategies like STRIDE, PASTA, LINDDUN, hTMM, or Attack Tree Modeling.
- **Industry Threat Libraries:** Employ predefined libraries for relevant scenarios.
   
## Beginners' Tips

- **Adopt an Attacker’s Perspective:** Think like an adversary to uncover various compromising avenues.
- **Simplicity First:** Start with clear, known threats, gradually advancing to nuanced scenarios.
- **Ensure Holistic Perspectives:** Embed organizational, technical, and environmental contexts in threat identification.

## Resources for Further Reading

- **CVE Database:** A comprehensive source of publicly known cybersecurity vulnerabilities.
- **MITRE ATT&CK:** A globally-accessible knowledge base of adversary tactics and techniques.
- [**Threat Modeling-12 available methods**](https://insights.sei.cmu.edu/blog/threat-modeling-12-available-methods/)

## Related Documents

- [Defining Security Problem (SPD)](./SecurityProblemDefinition.md)
- [Identifying Assets](./Asset.md)
- [Understanding Vulnerabilities](./Vulnerability.md)
- [Details about the Target of Evaluation (TOE)](./TargetofEvaluation.md)

