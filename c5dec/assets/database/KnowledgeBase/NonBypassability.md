---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: non-bypassability, TSF-architecture, security-architecture, reference-monitor, enforcement
---

# Non-bypassability

**Acronym:** None

**Non-bypassability** is one of the three fundamental architectural security properties of the [TOE Security Functionality (TSF)](./TOESecurityFunctionality.md). It ensures that the TSF's security enforcement mechanisms cannot be circumvented — every security-relevant operation must pass through the TSF, and no alternative execution path exists that would allow a subject to avoid TSF mediation. Without non-bypassability, an attacker could access [assets](./Asset.md) or perform actions without the TSF checking permissions, rendering all other security functions ineffective.

Together with [domain separation](./DomainSeparation.md) and [self-protection](./SelfProtection.md), non-bypassability forms the **TSF security architecture triad**.

## Definition

Non-bypassability means that for every [SFR](./SecurityFunctionalRequirement.md) that the TSF enforces, there is no way for a subject or external entity to perform the controlled action without the TSF being invoked. Specifically:

- All access to protected resources passes through the TSF's access control or information flow control enforcement points.
- All [TSF interfaces (TSFIs)](./TSFInterface.md) are fully mediated — there are no undocumented or unprotected interfaces.
- Hardware and software interfaces that could theoretically bypass the TSF (e.g., DMA, debug ports, shared memory) are either removed, disabled, or controlled by the TSF.
- The TSF is invoked on every security-relevant event, not just the first event in a sequence (i.e., caching or optimisation does not skip enforcement checks).

This property is closely related to the **reference monitor concept** from classical security architecture: a reference monitor must be always invoked, tamperproof, and verifiable.

## Relationship to other architectural properties

| Property | Role in the triad |
|---|---|
| **[Domain separation](./DomainSeparation.md)** | Provides the isolated execution domain within which the TSF operates. |
| **[Self-protection](./SelfProtection.md)** | Prevents the TSF's enforcement logic from being modified or corrupted. |
| **Non-bypassability** | Ensures all security-relevant actions are routed through the TSF — no alternative paths exist. |

Non-bypassability is the **outermost guarantee** — even if the TSF's domain is isolated and its code is intact, it must still be invoked on every relevant operation. A system with perfect domain separation and self-protection but with a bypassable enforcement point still fails to provide security assurance.

## Common bypass vectors

Evaluators and developers should consider these common bypass risks:

| Bypass vector | Description | Mitigation |
|---|---|---|
| **Direct hardware access (DMA)** | Devices performing DMA may read/write memory without CPU-mediated access control | IOMMU enforcement, DMA protection |
| **Debug interfaces (JTAG, UART)** | Physical debug ports may allow direct memory access | Disable or fuse off debug ports in production |
| **Shared memory** | Processes sharing memory regions may exchange data without TSF mediation | TSF-controlled shared memory allocation and labelling |
| **Alternate boot paths** | Booting from external media may bypass TSF initialisation | Secure boot with locked boot order |
| **Kernel module loading** | Loading untrusted kernel modules may introduce code with TSF-level privileges | Code signing enforcement for kernel modules |
| **Covert channels** | Information flow through unintended channels (timing, resource usage) | Covert channel analysis and bandwidth limitation |

## Practical guidance

### Evaluating non-bypassability

1. **Enumerate all data paths.** Using the TOE's design documentation, identify every path through which subjects can access protected resources or perform controlled operations. This includes internal interfaces, external interfaces, hardware buses, and inter-process communication mechanisms.

2. **Map enforcement points.** For each data path, verify that at least one TSF enforcement point mediates the access. There must be no path from a subject to a protected resource that bypasses all enforcement points.

3. **Assess completeness of mediation.** The TSF must check access on every invocation, not just the first. Evaluate caching and optimisation mechanisms to ensure they do not skip enforcement:
   - File system caches that serve data without re-checking permissions.
   - Connection caches that skip re-authentication.
   - Memory mappings that persist after permission revocation.

4. **Review hardware interfaces.** For hardware TOEs, check all physical interfaces (USB, JTAG, network, GPIO, SPI, I2C) and verify that each is either:
   - Mediated by the TSF, or
   - Physically disabled or absent in the evaluated configuration.

5. **Analyse privilege transitions.** At every privilege boundary (user → kernel, application → OS, guest → hypervisor), verify that the transition is controlled by the TSF and that the calling entity cannot manipulate the transition to bypass enforcement.

6. **Check for residual debug or test interfaces.** Verify that development-time interfaces (test modes, factory reset, diagnostic ports) are disabled or TSF-controlled in the production configuration.

### Documenting non-bypassability in the ST

The [TOE Summary Specification](./TOESummarySpecification.md) should:
- Describe how the TSF ensures that all security-relevant operations are mediated.
- Identify the enforcement points and the mechanisms that route operations through them.
- Address known bypass considerations specific to the TOE type (e.g., DMA protection for network appliances, secure boot for firmware-based TOEs).
- Reference the relevant SFR: typically FPT_RVM (reference mediation) in CC 3.1 R5 or equivalent assurance requirements in CC 2022.

> **CC 2022 note:** In CC 3.1 R5, non-bypassability was explicitly addressed by FPT_RVM (reference validation mechanism). In CC 2022, this property is addressed as an architectural requirement in the ADV_ARC family rather than as a standalone functional requirement. The concept remains the same; the location in the CC framework has changed.

## Additional resources

- CC Part 1, Section 10.3 — discussion of TSF security architecture properties.
- CC Part 3, ADV_ARC — security architecture description and evaluation, including non-bypassability assessment.
- Anderson, J.P., "Computer Security Technology Planning Study" (1972) — original reference monitor concept (always invoked, tamperproof, verifiable).
- CEM, ADV_ARC work units — evaluator activities for assessing architectural properties including non-bypassability.

## Related articles

- [Domain Separation](./DomainSeparation.md)
- [Self-Protection](./SelfProtection.md)
- [TOE Security Functionality](./TOESecurityFunctionality.md)
- [TSF Interface](./TSFInterface.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [TOE Boundary](./TOEBoundary.md)
- [Evaluation Evidence](./EvaluationEvidence.md)
