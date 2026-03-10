---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: attack-potential, vulnerability-analysis, AVA_VAN, CEM, penetration-testing, scoring
---

# Attack potential

**Acronym:** None

**Attack potential** is a measure of the effort, expertise, and resources required to successfully exploit a vulnerability in the [TOE](./TargetofEvaluation.md). It is the central metric used in vulnerability assessment ([AVA_VAN](./EvaluationAssuranceLevel.md)) to determine whether identified vulnerabilities are exploitable given the assumed [threat](./Threat.md) environment. If the attack potential required to exploit a vulnerability exceeds the attack potential assumed for the threat agents in the TOE's operational environment, the TOE is considered resistant to that attack.

Attack potential assessment is defined in the CEM (ISO/IEC 18045), Annex B, and is used by evaluators during penetration testing and vulnerability analysis activities.

## Factors

The CEM defines five factors that contribute to attack potential. Each factor is scored on a defined scale, and the total score determines the required attack potential level.

### 1. Elapsed time

The time required to identify and exploit a vulnerability.

| Rating | Description | Score |
|--------|-------------|-------|
| ≤ 1 day | The attack can be performed in under a day | 0 |
| ≤ 1 week | Requires up to a week of effort | 1 |
| ≤ 2 weeks | Requires up to two weeks | 2 |
| ≤ 1 month | Requires up to one month | 4 |
| ≤ 2 months | Requires up to two months | 7 |
| ≤ 3 months | Requires up to three months | 10 |
| ≤ 4 months | Requires up to four months | 13 |
| ≤ 5 months | Requires up to five months | 15 |
| ≤ 6 months | Requires up to six months | 17 |
| > 6 months | Requires more than six months | 19 |

### 2. Expertise

The level of specialist knowledge needed.

| Rating | Description | Score |
|--------|-------------|-------|
| Layman | No special expertise required; general knowledge only | 0 |
| Proficient | Familiar with the underlying concepts of the TOE type | 3 |
| Expert | Specialist in the relevant domain (e.g., cryptanalysis, OS internals) | 6 |
| Multiple experts | Multiple specialists from different domains | 8 |

### 3. Knowledge of the TOE

The level of TOE-specific information needed to mount the attack.

| Rating | Description | Score |
|--------|-------------|-------|
| Public | Information is publicly available (manuals, user guides) | 0 |
| Restricted | Information is controlled but obtainable (e.g., under NDA) | 3 |
| Sensitive | Information is closely held (internal design documents) | 7 |
| Critical | Information known only to a very small group (e.g., source code under strict access control) | 11 |

### 4. Window of opportunity

The access and opportunity available to the attacker.

| Rating | Description | Score |
|--------|-------------|-------|
| Unnecessary / unlimited | No physical or logical access constraints; attack can be attempted any time | 0 |
| Easy | The window is readily available but not unlimited | 1 |
| Moderate | Access is limited but achievable with some effort | 4 |
| Difficult | Access is tightly controlled and rarely available | 10 |
| None | Practical access is not feasible | — |

### 5. Equipment

The tools and equipment required.

| Rating | Description | Score |
|--------|-------------|-------|
| Standard | Readily available tools (PCs, open-source software) | 0 |
| Specialised | Specialised but obtainable equipment (e.g., protocol analysers, JTAG probes) | 4 |
| Bespoke | Custom-built equipment or highly specialised lab setups | 7 |
| Multiple bespoke | Multiple pieces of custom equipment | 9 |

## Interpreting the total score

The sum of all five factor scores yields the total attack potential. The CEM maps total scores to attack potential levels:

| Total score | Attack potential level | Resistant at... |
|--|--|--|
| 0–9 | Basic | Resistant at AVA_VAN.1 (none resisted) |
| 10–13 | Enhanced-Basic | Resistant at AVA_VAN.2 |
| 14–19 | Moderate | Resistant at AVA_VAN.3 |
| 20–24 | High | Resistant at AVA_VAN.4 |
| ≥ 25 | Beyond High | Resistant at AVA_VAN.5 |

The mapping to [Evaluation Assurance Levels](./EvaluationAssuranceLevel.md):

| EAL | AVA_VAN component | Minimum resistance |
|-----|--------------------|--------------------|
| EAL1 | AVA_VAN.1 | No attack potential claim |
| EAL2 | AVA_VAN.2 | Basic |
| EAL3 | AVA_VAN.2 | Basic |
| EAL4 | AVA_VAN.3 | Enhanced-Basic |
| EAL5 | AVA_VAN.4 | Moderate |
| EAL6 | AVA_VAN.5 | High |
| EAL7 | AVA_VAN.5 | High |

## Practical guidance

### Performing an attack potential assessment

1. **Identify candidate vulnerabilities.** Review the TOE's design documentation, public vulnerability databases (CVE, NVD), and the results of evaluator analysis (ADV, ATE activities). List potential attack paths.

2. **Score each vulnerability.** For each candidate vulnerability, estimate values for all five factors based on the TOE's design, operational environment, and assumed attacker profile. Document the rationale for each score.

3. **Sum the scores.** Calculate the total for each vulnerability and determine the attack potential level.

4. **Compare against the claimed resistance.** The TOE must resist all attacks at or below the attack potential level corresponding to its AVA_VAN component. For example, at EAL4 (AVA_VAN.3), the TOE must resist all attacks requiring Moderate or lower attack potential (total score < 20).

5. **Perform penetration testing.** For vulnerabilities where the total score falls below the threshold, design and execute penetration tests to confirm exploitability. If a vulnerability is successfully exploited, it constitutes a finding against the TOE.

6. **Document results.** Record all vulnerability assessments, scores, and penetration test results in the [Evaluation Technical Report (ETR)](./EvaluationTechnicalReport.md).

### Tips for developers

- **Design to raise the attacker's cost.** Prefer designs that require high expertise, restricted knowledge, and specialised equipment to attack. Each factor score that increases pushes the total beyond the exploitation threshold.
- **Minimise the window of opportunity.** Limit physical and logical access points. Network-facing interfaces should be hardened and rate-limited.
- **Monitor public vulnerability sources.** Regularly review CVE, NVD, and product-specific advisories to identify newly disclosed vulnerabilities that may affect attack potential calculations.
- **Prepare for independent testing.** Evaluators will attempt to confirm vulnerabilities. Ensuring robust test evidence (ATE) helps demonstrate that developer testing already covered potential attack paths.

## Additional resources

- CEM (ISO/IEC 18045), Annex B — Attack potential calculation methodology.
- CC Part 3, AVA_VAN family — Vulnerability analysis component definitions.
- CCDB-0099 — Joint Interpretation Library: Application of Attack Potential to Smartcards (for domain-specific guidance).
- BSI AIS 25/31/46 — German scheme-specific guidance on attack potential for hardware and smartcard evaluations.

## Related articles

- [Evaluation Assurance Levels](./EvaluationAssuranceLevel.md)
- [Evaluation Methods](./EvaluationMethods.md)
- [Threat](./Threat.md)
- [Evaluation Technical Report](./EvaluationTechnicalReport.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
- [EUCC](./EUCC.md)
