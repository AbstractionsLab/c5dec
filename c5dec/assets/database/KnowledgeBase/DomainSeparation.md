---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: domain-separation, TSF-architecture, security-architecture, isolation, process-separation
---

# Domain separation

**Acronym:** None

**Domain separation** is one of the three fundamental architectural security properties that the [TOE Security Functionality (TSF)](./TOESecurityFunctionality.md) must exhibit to be considered trustworthy. It ensures that the TSF maintains its own execution domain, isolated from untrusted processes and subjects, so that the security enforcement mechanisms cannot be tampered with or interfered with by non-TSF code.

Together with [self-protection](./SelfProtection.md) and [non-bypassability](./NonBypassability.md), domain separation forms the **TSF security architecture triad** — the foundational properties that underpin all other security functions of the TOE.

## Definition

Domain separation means that the TSF provides and manages a security domain for its own execution that protects it from interference and tampering by untrusted subjects. In practical terms:

- The TSF's code and data reside in a protected memory space that cannot be accessed or modified by non-TSF processes.
- The TSF mediates all interactions between different security domains (e.g., between user processes, between user processes and the TSF).
- Subjects operating in different security domains cannot observe or influence each other's state except through TSF-controlled interfaces.

Domain separation is the mechanism through which the TSF ensures that its security enforcement decisions are based on authentic, unmodified data and that its enforcement logic has not been altered.

## Relationship to other architectural properties

The three properties are complementary:

| Property | What it ensures |
|---|---|
| **Domain separation** | The TSF has its own protected execution domain, isolated from untrusted subjects. |
| **[Self-protection](./SelfProtection.md)** | The TSF can protect its own code and data from tampering, even by privileged processes. |
| **[Non-bypassability](./NonBypassability.md)** | All security-relevant operations must pass through the TSF — no path exists to circumvent enforcement. |

Domain separation provides the **foundation** — without an isolated domain, self-protection and non-bypassability become meaningless, because an attacker with access to the TSF's domain could directly modify enforcement logic.

## Implementation mechanisms

Different TOE types achieve domain separation through different mechanisms:

| TOE type | Domain separation mechanism |
|---|---|
| Operating systems | Hardware-enforced privilege rings (ring 0 for kernel/TSF, ring 3 for user space), memory management unit (MMU) protection, address space isolation |
| Hypervisors | Hardware virtualisation extensions (VT-x, SVM), separate VM address spaces, IOMMU for device isolation |
| Smartcards / secure elements | Hardware isolation of applets, firewall between card applications, secure loading |
| Applications | Process-level sandboxing, capability-based access control, separate address spaces |
| Network devices | Separate control plane and data plane, hardware isolation of management interfaces |

## Practical guidance

### Evaluating domain separation

1. **Identify the TSF domain boundaries.** Review the [TOE design documentation](./EvaluationEvidence.md) to understand how the TSF's execution domain is defined. Identify the hardware and software mechanisms that enforce the separation.

2. **Verify enforcement mechanisms.** For each domain separation mechanism:
   - Is it hardware-enforced, software-enforced, or a combination?
   - Can the enforcement be disabled or reconfigured by non-TSF code?
   - What happens if the mechanism fails (fail-secure vs. fail-open)?

3. **Assess inter-domain communication.** Where subjects in different domains must communicate:
   - Is all communication mediated by the TSF?
   - Are shared resources (e.g., shared memory, shared files) protected by TSF access control?
   - Can covert channels bypass domain separation?

4. **Check for privilege escalation paths.** Verify that no non-TSF subject can elevate its privileges to gain access to the TSF domain. Review system call interfaces, driver interfaces, and any debug or maintenance interfaces.

5. **Review the Security Target.** Confirm that the [TOE Summary Specification](./TOESummarySpecification.md) describes the domain separation mechanisms and traces them to [SFRs](./SecurityFunctionalRequirement.md) (typically FPT_SEP — TSF domain separation).

### Documenting domain separation for the ST

When writing the TOE Summary Specification, ensure that domain separation is addressed by:
- Naming the specific isolation mechanism(s) used.
- Describing the TSF's protected execution environment.
- Identifying the [TSF interfaces](./TSFInterface.md) through which non-TSF subjects interact with the TSF.
- Referencing the relevant SFR (typically FPT_SEP.1 or FPT_SEP.2 for multi-domain separation).

## Additional resources

- CC Part 2, FPT_SEP family — TSF domain separation functional components.
- CC Part 1, Section 10.3 — discussion of TSF security architecture properties.
- Anderson, R., *Security Engineering* — foundational treatment of reference monitor concepts and domain separation.

## Related articles

- [Self-Protection](./SelfProtection.md)
- [Non-Bypassability](./NonBypassability.md)
- [TOE Security Functionality](./TOESecurityFunctionality.md)
- [TSF Interface](./TSFInterface.md)
- [Sub-TOE Security Functionality](./SubTOESecurityFunctionality.md)
- [Security Functional Requirements](./SecurityFunctionalRequirement.md)
- [TOE Boundary](./TOEBoundary.md)
