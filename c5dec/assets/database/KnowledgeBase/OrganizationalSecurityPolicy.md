# Organizational Security Policy

**Acronym:** OSP

Organizational Security Policy (OSP) within the Common Criteria framework is a fundamental construct, defined as a set of security rules, procedures, or guidelines for an organization. Embedded within the [Security Problem Definition (SPD)](./SecurityProblemdefinition.md) of both [Protection Profiles (PP)](./ProtectionProfiles.md) and [Security Targets (ST)](./SecurityTarget.md) to enforce compliance, mitigate potential threats, and ensure the protection of assets within a specified operational environment. Within the CC paradigm, OSPs are not merely declarative; they are enforced through defined [security objectives](./SecurityObjective.md) that are shouldered by the [Target of Evaluation (TOE)](./TargetofEvaluation.md), its [operational environment](./TOEOperationalEnvironment.md), or synergistically by both.

## Practical Guidance

While OSPs might initially be identified during the informal security requirement definition or threat analysis phases, a detailed revisit ensures that every relevant policy, whether mandating specific security functions, prescribing certain technologies, or strategically replacing threats, is encapsulated comprehensively within the Security Problem Definition (SPD). 

**1. Leveraging Existing Organizational Policies:**   
   Begin by exploring the existing set of security policies established within the organization. Assess their applicability and pertinence to the TOE. Where these pre-established policies align with TOE’s functionality and operational environment, tailor them accordingly to befit the specific requirements and contexts of the TOE under evaluation. This approach ensures that the OSPs formulated are not only aligned with organizational strategies and norms but are also tailored to effectively navigate the specific security contours and requirements of the TOE.

**2. Policy Specification:**   
   Specify policies with a clear focus on mandatory security functions or technologies/techniques, ensuring they are directly tied to the TOE and its integral security functions.

**3. Threat Replacement Consideration:**   
   Evaluate whether policies should replace threats based on certainty, pre-existing policy decisions about threat management, and the strategic approach to countering related threats.

**4. Articulation into Security Objectives:**   
   Ensure that OSPs, which denote mandatory security functions or requisite technologies/techniques, are translated into actionable security objectives in the Security Target (ST) or Protection Profile (PP). These objectives should offer a clear, solution-oriented representation, elucidating how the TOE will concretely adhere to or implement the stipulated security functions and technologies elucidated in the OSPs.

## Additional Resources

- **ISO/IEC TR 15446:** This technical report provides a methodical approach to creating an SPD, guiding users through the identification of informal security requirements, threats, policies, and assumptions.
- **ISO/IEC 27001:** Guidelines on establishing, implementing, maintaining, and continuously improving an information security management system.
- **NIST SP 800-53:** Guidance on security and privacy controls for federal information systems and organizations.

## Related Articles

- [Security Problem Definition](./SecurityProblemdefinition.md)
- [Security Objectives](./SecurityObjectives)