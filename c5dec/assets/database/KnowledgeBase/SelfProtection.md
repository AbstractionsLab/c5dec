---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: self-protection, TSF-architecture, security-architecture, tamper-resistance, integrity
---

# Self-protection

**Acronym:** None

**Self-protection** is one of the three fundamental architectural security properties of the [TOE Security Functionality (TSF)](./TOESecurityFunctionality.md). It ensures that the TSF can protect its own code, data, and execution state from tampering, modification, or corruption — whether by untrusted subjects within the TOE, by physical attack, or by exploitation of software vulnerabilities. Without self-protection, the TSF's enforcement of [security functional requirements](./SecurityFunctionalRequirement.md) cannot be trusted, because an attacker who can modify the TSF can disable or subvert any security function.

Together with [domain separation](./DomainSeparation.md) and [non-bypassability](./NonBypassability.md), self-protection forms the **TSF security architecture triad**.

## Definition

Self-protection means that the TSF is able to protect itself against external interference and tampering that might compromise its correct operation. Specifically:

- The TSF's executable code cannot be modified by any subject other than authorised administrative actions performed through TSF-controlled interfaces.
- The TSF's internal data (security attributes, configuration parameters, policy databases, audit logs) cannot be read or modified by untrusted subjects.
- The TSF maintains its security properties across state transitions, including startup, shutdown, and recovery from failure.
- The TSF detects and responds to attempts to tamper with its code or data.

## Scope of self-protection

Self-protection operates at multiple layers:

### Software self-protection

- Code integrity: The TSF's executable code is protected from modification (e.g., through read-only memory mappings, code signing, secure boot chains).
- Data integrity: TSF-internal data structures (access control databases, key stores, audit logs) are protected from unauthorised modification.
- State integrity: The TSF maintains a consistent security state across all operating modes, including error handling and recovery.

### Hardware-based self-protection

For TOEs with hardware components (smartcards, HSMs, trusted platform modules):
- Tamper-resistant enclosures or shielding.
- Sensors that detect physical probing, voltage glitching, or temperature manipulation.
- Zeroisation of sensitive data upon tamper detection.

### Boot and initialisation integrity

- Secure boot chain ensuring only authorised TSF code executes at startup.
- Integrity verification of TSF images before loading.
- Protection of boot-time configuration parameters.

## Practical guidance

### Evaluating self-protection

1. **Identify TSF assets.** List the TSF's code, configuration data, security attributes, and internal state that require protection. These are the self-protection targets.

2. **Review protection mechanisms.** For each TSF asset, identify the mechanism that prevents unauthorised modification:
   - Memory protection (MMU, MPU, flash write-protect).
   - Access control on TSF data files and databases.
   - Cryptographic integrity checks (MACs, digital signatures on TSF code/data).
   - Secure boot and measured boot chains.

3. **Assess recovery behaviour.** Determine what happens when the TSF detects a compromise:
   - Does the TSF fail secure (deny all access) or fail open (permit access)?
   - Can the TSF recover to a known-good state?
   - Are audit events generated for detected tampering attempts?

4. **Check for administrative overrides.** Verify that administrative interfaces for updating TSF code or configuration:
   - Require strong authentication.
   - Verify the integrity of updates before applying them.
   - Log all administrative changes.

5. **Evaluate physical self-protection** (if applicable). For hardware TOEs:
   - Review tamper detection and response mechanisms.
   - Assess the effectiveness of shielding and sensor coverage.
   - Check zeroisation procedures for sensitive material.

### Documenting self-protection in the ST

The [TOE Summary Specification](./TOESummarySpecification.md) should:
- Describe all self-protection mechanisms.
- Trace each mechanism to the relevant SFRs (typically FPT_PHP for physical protection, FPT_TST for TSF self-testing, FPT_SEP for domain separation as a supporting property, FPT_FLS for failure handling).
- Describe the TSF's behaviour upon detection of a self-protection violation.

## Additional resources

- CC Part 2, FPT class — Protection of the TSF, including FPT_PHP (physical protection), FPT_TST (TSF testing), FPT_FLS (failure with preservation of secure state).
- CC Part 1, Section 10.3 — discussion of TSF security architecture properties.
- FIPS 140-3 — security requirements for cryptographic modules, with extensive physical security level definitions relevant to hardware self-protection.

## Related articles

- [Domain Separation](./DomainSeparation.md)
- [Non-Bypassability](./NonBypassability.md)
- [TOE Security Functionality](./TOESecurityFunctionality.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [TOE Summary Specification](./TOESummarySpecification.md)
- [Sub-TOE Security Functionality](./SubTOESecurityFunctionality.md)
