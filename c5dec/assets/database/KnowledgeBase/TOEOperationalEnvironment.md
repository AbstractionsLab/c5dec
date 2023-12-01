---
Last Updated: October 4, 2023
Relevant CC Version: 3.1 Revision 5
---

# TOE Operational Environment

The TOE Operational Environment encompasses all aspects that are presumed to exist in the environment where the [TOE](./TargetofEvaluation.md) will be deployed and operational. It encompasses physical, personnel, and technological aspects which are presumed to exist and safeguard security aspects which are outside the [TOE boundary](./TOEBoundary.md).

In the context of the Common Criteria the TOE Operational Environment must meet certain constraints such as:

- **Physical Aspect:** Includes the physical conditions and protections where the TOE is deployed and operated, such as secure installation sites, physical access controls, and environmental controls.
- **Personnel Aspect:** Refers to the individuals who interact with or within the environment of the TOE, including administrators, users, and potential attackers. Their roles, responsibilities, and qualifications are defined to assure secure operation of the TOE.
- **Technological Aspect:** Incorporates the IT environment, consisting of other IT products/systems (hardware and software) that interact with or support the TOE, such as operating systems, networks, and auxiliary storage devices.

These aspects are meticulously addressed through the establishment of [assumptions](./Assumption.md) and adherence to [Organizational Security Policies (OSPs)](./OrganizationalSecurityPolicy.md). These elements collaboratively formulate a structured framework wherein assumptions delineate presumed conditions or attributes of the operational environment while OSPs impose specific procedural and security guidelines set by the overseeing organization or regulatory bodies. Consequently, to synthesize these provisions into a practical and implementable format, they are translated into [security objectives for the operational environment](./SecurityObjective.md). 

## Practical Considerations

In practice, when dealing with TOE Operational Environment within CC:

- While the TOE Operational Environment might not be explicitly defined within the [Security Target (ST)](./SecurityTarget.md) or [Protection Profile (PP)](./ProtectionProfile.md), its characteristics and expectations are implicitly conveyed through assumptions and Organizational Security Policies (OSPs), as well as through the derivation of security objectives for the operational environment. These elements collectively provide insights into the conditions and requirements of the TOE Operational Environment, influencing how the TOE is expected to achieve its specified [security functionalities](./TOESecurityFunctionality.md) within that environment.
- The TOE Operational Environment is not tested during the evaluation but it’s vital to ensure that all the assumptions about the TOE Operational Environment are upheld in the actual deployment to ensure the TOE can provide the claimed security functionalities.
- It's imperative to have a clear boundary definition between the TOE and its operational environment to clearly segregate the security functionalities provided by the TOE and those assumed to be provided by its operational environment.

## Additional Resources

- **ISO/IEC TR 15446:** This technical report provides a methodical approach to creating an SPD, guiding users through the identification of informal security requirements, threats, policies, and assumptions.

## Related Articles

- [Security Target (ST)](./SecurityTarget.md)
- [Protection Profile (PP)](./ProtectionProfile.md)
- [Security Objective for the Operational Environment](./SecurityObjective.md)