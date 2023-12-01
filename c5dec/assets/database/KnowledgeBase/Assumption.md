# Assumption

**Acronym:** None

Security rests on assumptions specific to the type of security required and the environement in which it is to be employed. Assumptions are treated as axioms, i.e., they are taken to be true, to serve as a premise for further reasoning and arguments. Assumptions provide a grounding, describing expected conditions in the [operational environment](TOEOperationalEnvironment.md) which are presumed to be true, and under which the [Target of Evaluation (TOE)](./TargetofEvaluation.md) will operate securely. These are essential in the construction of a [Security Problem Definition (SPD)](./SecurityProblemdefinition.md) and subsequently the entire security posture of the TOE.

In the world of CC, assumptions are categorized based on aspects such as physical, personnel, and connectivity of the operational environment. However, these assumptions are not scrutinized or tested during the evaluation phase as they are regarded as fundamental truths, providing a reliable basis upon which the [TOE's security functionality](./TOESecurityFunctionality.md) is conceived and designed. Consequently, if a TOE is placed in an environment that does not adhere to these assumptions, its security functionality and reliability can be compromised.

## Practical Guidance

Navigating through the landscape of crafting and implementing assumptions within CC involves being mindful of their dual utility and strategic integration. Assumptions in CC are leveraged to:

- **Dictate Environmental Controls**: Highlight specific controls or types of controls that are the responsibility of the operational environment and not the TOE.
- **Dismiss Irrelevant Threats**: Specify threats or types of threats that can be disregarded, asserting that they either do not exist or are not pertinent in the context of the posited operational environment.

### Identifying and Formulating Assumptions:
- **Operational Insights:** Derive assumptions from an in-depth understanding of the physical, personnel, and connectivity aspects of the operational environment.
- **Policy Alignment:** Shape assumptions that are in sync with organizational policies and user behaviors.
- **Regulatory Adherence:** Ensure that assumptions are congruent with legal and regulatory requirements.
- **Industry Benchmarking:** Evaluate industry best practices and historical incident data to extract relevant assumptions.
- **Articulation into Security Objectives:** Ensure that assumptions are translated into actionable [security objective](./SecurityObjective.md) in the [Security Target (ST)](./SecurityTarget.md) or [Protection Profile (PP)](./ProtectionProfile.md). These security objectives should offer a clear, solution-oriented representation, elucidating how the TOE's operational environment will concretely upheld the assumptions.

## Additional Resources

- **ISO/IEC TR 15446:** A Guide for the production of Protection Profiles and Security Targets.

## Related Articles

- [Deriving the Security Problem Definition](./SecurityProblemdefinition.md)
- [Identifying Threats](./Threat.md)
- [Deriving Security Objectives](./SecurityObjectives.md)
- [Understanding the Operational Environment (OE)](./TOEOperationalEnvironment.md)