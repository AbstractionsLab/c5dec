---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: non-TSF, TOE-boundary, untrusted-code, operational-environment
---

# Non-TSF part

**Acronym:** None

The **Non-TSF part** of a [TOE](./TargetofEvaluation.md) comprises all hardware, software, and firmware components that are within the [TOE boundary](./TOEBoundary.md) but are **not** part of the [TOE Security Functionality (TSF)](./TOESecurityFunctionality.md). These components do not enforce security policy and are not relied upon for security enforcement. However, they are still part of the evaluated product and can affect the TOE's security properties if they are able to interfere with the TSF.

Understanding the distinction between TSF and non-TSF parts is essential for accurate [TOE Description](./TOEDescription.md), proper security architecture analysis, and correct application of the TSF architectural properties ([domain separation](./DomainSeparation.md), [self-protection](./SelfProtection.md), [non-bypassability](./NonBypassability.md)).

## Why non-TSF parts matter

Even though non-TSF parts do not enforce security policy, they are evaluated to the extent that they might:

1. **Interfere with the TSF.** A non-TSF component that shares resources with the TSF (e.g., common libraries, shared hardware bus) could potentially disrupt TSF operation.
2. **Bypass the TSF.** A non-TSF component with direct hardware access or elevated privileges could create a path around TSF enforcement.
3. **Receive user data processed by the TSF.** Non-TSF components may handle user data after TSF processing, affecting post-enforcement confidentiality or integrity.

The TSF's security architecture must ensure that non-TSF parts cannot compromise TSF properties. This is primarily achieved through [domain separation](./DomainSeparation.md) — the TSF isolates itself from non-TSF code.

## Examples

| TOE type | TSF part | Non-TSF part |
|---|---|---|
| Operating system | Kernel security subsystem, access control enforcement, audit engine | User interface shell, file manager, text editor |
| Firewall | Packet filtering engine, rule management, logging | Web-based admin GUI (if not enforcing policy), diagnostic utilities |
| Smartcard | Card OS security kernel, cryptographic engine, applet firewall | Specific applets that do not enforce cross-applet security |
| VPN gateway | IPsec engine, key management, authentication module | SNMP agent, web dashboard (if not security-enforcing) |

## Practical guidance

### Identifying non-TSF parts

1. **Start from the TSF definition.** Review the [Security Target](./SecurityTarget.md) to identify all TSF components. Everything within the [TOE boundary](./TOEBoundary.md) that is not part of the TSF is, by definition, a non-TSF part.

2. **Classify each component.** For every component listed in the [TOE Description](./TOEDescription.md):
   - Does it enforce any [SFR](./SecurityFunctionalRequirement.md)? → TSF.
   - Does it support TSF enforcement (e.g., provides cryptographic services used by the TSF)? → TSF.
   - Does it neither enforce nor support SFR enforcement? → Non-TSF.

3. **Be conservative with the boundary.** When in doubt about whether a component supports TSF enforcement, include it in the TSF. This avoids under-evaluation of security-relevant code.

### Addressing non-TSF parts in the security architecture

1. **Document the separation.** The [TOE Summary Specification](./TOESummarySpecification.md) should describe how the TSF is isolated from non-TSF parts — which [domain separation](./DomainSeparation.md) mechanisms prevent non-TSF code from accessing TSF resources.

2. **Assess interference potential.** For each non-TSF component:
   - Can it modify TSF code or data? (Should be prevented by self-protection.)
   - Can it bypass TSF enforcement points? (Should be prevented by non-bypassability.)
   - Can it consume resources needed by the TSF (denial of service)?

3. **Address shared resources.** Where TSF and non-TSF parts share hardware (e.g., the same CPU, the same network interface):
   - Document the sharing arrangement.
   - Describe the isolation mechanism (e.g., privilege separation, resource quotas).
   - Show that shared resource contention does not create a security vulnerability.

4. **Specify the evaluated configuration.** The presence or absence of specific non-TSF components may affect the security of the evaluated TOE. The ST should specify the evaluated configuration, including which non-TSF components are present and which are optional.

## Additional resources

- CC Part 1, Section 10.3 — distinction between TSF and non-TSF parts, architectural requirements.
- CC Part 3, ADV_ARC — security architecture evidence, including assessment of TSF vs. non-TSF separation.
- ISO/IEC TR 15446 — guidance on defining the TSF boundary and handling non-TSF components.

## Related articles

- [TOE Boundary](./TOEBoundary.md)
- [TOE Security Functionality](./TOESecurityFunctionality.md)
- [Domain Separation](./DomainSeparation.md)
- [Self-Protection](./SelfProtection.md)
- [Non-Bypassability](./NonBypassability.md)
- [TOE Description](./TOEDescription.md)
- [Security Target](./SecurityTarget.md)
