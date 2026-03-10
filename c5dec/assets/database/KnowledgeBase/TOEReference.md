---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: TOE-reference, identification, security-target, PP, versioning
---

# TOE Reference

The **TOE Reference** uniquely identifies the [Target of Evaluation](./TargetofEvaluation.md) within a [Security Target](./SecurityTarget.md). It provides the information necessary for consumers, evaluators, and certification bodies to unambiguously determine which product (and which version/configuration of that product) was evaluated.

## Definition

The TOE Reference is a mandatory section of the ST Introduction (ASE_INT). It must contain enough information to distinguish the evaluated TOE from any other product or version. The CC does not prescribe a rigid format but requires that the identification be unambiguous.

The TOE Reference typically includes the following elements:

| Element | Description | Example |
|---------|-------------|---------|
| **Developer / Vendor** | The organisation responsible for the TOE. | Acme Security Inc. |
| **Product name** | The commercial or technical name of the product. | SecureGate Firewall |
| **Version identifier** | The specific version, build number, or firmware revision evaluated. | v3.2.1 Build 4587 |
| **Hardware identifier** (if applicable) | Model number or hardware revision for physical TOEs. | Model SG-4000 Rev C |
| **Configuration identifier** (if applicable) | The specific configuration or SKU evaluated, when the product supports multiple configurations. | Enterprise Edition with FIPS module enabled |

## Practical guidance

### Writing a TOE reference

1. **Be precise on versioning.** Certificates apply to the exact version evaluated. If the product uses semantic versioning, include the full version string (major.minor.patch). For firmware, include build or revision identifiers. Any ambiguity risks the certificate being questioned during procurement.
2. **Include all identifiable components.** If the TOE comprises hardware and software (e.g., an HSM appliance), list both the hardware model/revision and the software/firmware version.
3. **Align with the certificate.** The TOE Reference in the ST must match the identification on the CC certificate exactly. Discrepancies cause administrative delays and may require re-certification.
4. **Consider future maintenance.** Use an identification scheme that supports the developer's planned [assurance continuity](./EvaluationAssuranceLevel.md) strategy. If minor version updates are expected to be covered under assurance maintenance, document the versioning policy.
5. **Reference the PP's TOE type.** If the ST claims conformance to a [PP](./ProtectionProfile.md), verify that the TOE Reference clearly places the product within the PP's defined TOE type.

### Common mistakes

- **Vague version strings.** "SecureGate Firewall v3" is insufficient if multiple v3.x releases exist with different security properties.
- **Missing component identifiers.** A composed product listing only the software version but omitting the hardware platform leaves the evaluated configuration ambiguous.
- **Mismatch with marketing names.** If the vendor uses different names internally versus commercially, ensure the ST uses the identifier that appears on the product and its certificate.

## Additional resources

- CC 2022 Part 1, Section 7.2 -- ST Introduction (ASE_INT) requirements.
- CC Part 3, ASE_INT family -- evaluator actions for ST identification.
- CEM, ASE_INT evaluation activities.

## Related articles

- [Security Target](./SecurityTarget.md)
- [TOE Overview](./TOEOverview.md)
- [TOE Description](./TOEDescription.md)
- [Target of Evaluation](./TargetofEvaluation.md)
- [Protection Profile](./ProtectionProfile.md)
