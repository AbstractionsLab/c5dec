---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: evaluation-assurance-level, EAL, assurance, package
---

# Evaluation Assurance Level

**Acronym:** EAL

An Evaluation Assurance Level (EAL) is a predefined [package](./Package.md) of [security assurance requirements](./SecurityAssuranceRequirement.md) drawn from CC Part 3 that represents a point on a scale of increasing assurance. Each EAL builds on the previous level, providing more rigorous evidence and deeper analysis.

## Definition

EALs provide an ordered, balanced set of assurance requirements. CC 2022 defines seven levels:

| EAL | Name | Description |
|-----|------|-------------|
| **EAL 1** | Functionally tested | Provides a basic level of assurance through functional testing. Applies where some confidence in correct operation is needed but the threat environment is not serious. Minimum useful independent evaluation. |
| **EAL 2** | Structurally tested | Requires cooperation from the developer in delivery of design information and test results. Applied where low-to-moderate independently assured security is required. Typical for legacy systems. |
| **EAL 3** | Methodically tested and checked | Requires more complete coverage in security testing and development controls. Applied where a moderate level of independently assured security is needed with thorough investigation of the TOE and its development. |
| **EAL 4** | Methodically designed, tested, and reviewed | Permits a developer to gain maximum assurance from positive security engineering based on good commercial development practices. Applied where moderate-to-high independently assured security is needed and the development costs are not unreasonable. EAL 4 is the highest level at which retrofit to existing products is likely to be economically feasible. |
| **EAL 5** | Semiformally designed and tested | Requires semiformal design descriptions, a modular and layered architecture, and more rigorous analysis. Applied where high independently assured security is needed in a planned development with a rigorous approach. |
| **EAL 6** | Semiformally verified design and tested | Requires a more comprehensive analysis, a structured representation of the implementation, and more systematic analysis of vulnerabilities. Applied where high-value assets benefit from the additional assurance in a rigorous development environment. |
| **EAL 7** | Formally verified design and tested | Applies to the highest-risk situations and/or where the value of the assets justifies the higher costs. Requires formal representation and correspondence, comprehensive testing, and analysis of covert channels. |

> **CC 2022 note:** The seven EAL definitions are structurally unchanged from CC 3.1 R5. The main changes in CC 2022 affect how EALs interact with [PP-Configurations](./PPConfiguration.md) and [multi-assurance evaluations](./MultiAssuranceEvaluation.md).

## Relationship to attack potential

An EAL indirectly corresponds to resistance against attack through the vulnerability analysis (AVA_VAN) component it includes. For a detailed treatment of attack factor scoring and resistance calculation, see [Attack Potential](./AttackPotential.md).

The mapping between EALs and AVA_VAN components is:

| EAL | AVA_VAN component | Minimum required resistance |
|-----|-------------------|---------------------------|
| EAL 1 | AVA_VAN.1 | Basic |
| EAL 2 | AVA_VAN.2 | Basic |
| EAL 3 | AVA_VAN.3 | Enhanced-basic |
| EAL 4 | AVA_VAN.4 | Moderate |
| EAL 5 | AVA_VAN.4 | Moderate |
| EAL 6 | AVA_VAN.5 | High |
| EAL 7 | AVA_VAN.5 | High |

The [TOE's](./TargetofEvaluation.md) resistance must meet or exceed the threshold for the AVA_VAN component included in its EAL. The attack scenario requiring the highest attack potential is decisive.

## Augmentation and diminishment

An EAL may be **augmented** by adding assurance components from CC Part 3 beyond those in the standard package. The notation uses a "+" suffix (e.g., "EAL 4 augmented with ALC_FLR.2" or "EAL 4+"). Augmentation is the primary mechanism for tailoring assurance without defining a fully custom package.

Augmentation rules:
- The added component must not already be included in the EAL.
- The added component must not be a lower-level component of one already included.
- The result is no longer a "pure" EAL but is referenced as "EAL n augmented with ...".

> **Important:** EALs cannot be officially "diminished" -- removing a component breaks the balanced package guarantee. If the standard EAL requirements are too onerous, select the next lower EAL and augment upward selectively.

## Practical guidance

### Selecting an EAL

1. **Assess the threat environment.** Consider the value of protected [assets](./Asset.md), the capability of likely [threat agents](./Threat.md), and regulatory requirements. Higher-value assets and more capable attackers justify higher EALs.
2. **Consider development feasibility.** EAL 4 is typically the highest level that existing commercial products can achieve without being designed for CC from the start. EAL 5+ requires semiformal or formal methods from early design stages.
3. **Check scheme and PP requirements.** The target [PP](./ProtectionProfile.md) or certification scheme may mandate a minimum EAL. [EUCC](./EUCC.md) defines "substantial" (generally EAL 4 or below) and "high" (EAL 5+) assurance levels.
4. **Evaluate cost-benefit.** Each EAL step increases the volume and depth of required [evaluation evidence](./EvaluationEvidence.md). Rough effort scaling:
   - EAL 1-2: weeks of evaluation effort; suitable for low-risk or legacy products.
   - EAL 3-4: months; suitable for most commercial IT products.
   - EAL 5-7: extensive; suitable for high-security or government/defence products.
5. **Consider augmentation.** If the standard EAL mostly fits but one assurance area needs strengthening (e.g., vulnerability analysis or lifecycle support), augment that single component rather than moving to a higher EAL entirely.

### CCRA mutual recognition

The CCRA (Common Criteria Recognition Arrangement) mutually recognises evaluations up to EAL 2, plus evaluations against collaborative Protection Profiles (cPPs) without EAL limitation. Recognition of EAL 3+ outside cPP-based evaluations depends on bilateral or scheme-specific agreements (such as [EUCC](./EUCC.md) within the EU or SOG-IS within Europe).

## Additional resources

- CC 2022 Part 3, Section 7 -- EAL definitions and component composition tables.
- CC 2022 Part 1, Section 5.4 -- introduction to assurance concepts.
- CEM, Annex B -- attack potential calculation methodology.
- CCRA Portal -- list of mutual recognition participants and cPPs.

## Related articles

- [Attack Potential](./AttackPotential.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
- [Package](./Package.md)
- [Protection Profile](./ProtectionProfile.md)
- [Evaluation Evidence](./EvaluationEvidence.md)
- [EUCC](./EUCC.md)
- [Single-Assurance Evaluation](./SingleAssuranceEvaluation.md)
- [Multi-Assurance Evaluation](./MultiAssuranceEvaluation.md)
