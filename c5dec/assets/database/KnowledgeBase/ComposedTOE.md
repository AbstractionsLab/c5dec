---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: composed-TOE, base-component, dependent-component, composition, ACO
---

# Composed TOE

**Acronym:** None

A **Composed TOE** is a [Target of Evaluation](./TargetofEvaluation.md) that consists of two or more separately evaluated IT components combined into a single product or system. In a composed TOE, one component (the **base component**) provides services that another component (the **dependent component**) relies upon. The key advantage of composed evaluation is the ability to reuse prior evaluation results for individual components, thereby reducing the overall evaluation effort.

Composed TOE evaluation is governed by the ACO (Composition) assurance class in CC Part 3 and the corresponding CEM activities. It is particularly relevant in industries where products are assembled from pre-certified building blocks, such as smartcard platforms with applications, or secure operating systems with security modules.

## Architecture

A composed TOE has two essential roles:

- **Base component** — provides underlying services (e.g., a smartcard operating system, a hardware security module). The base component has been previously evaluated and holds a valid certificate.
- **Dependent component** — relies on the base component's services to fulfil its security functions (e.g., a payment application running on a smartcard platform). The dependent component may or may not have been evaluated independently.

The relationship between components is defined by:
1. **Reliance** — the dependent component relies on specific security services of the base component.
2. **Interfaces** — the interaction between components occurs through defined [TSF interfaces](./TSFInterface.md).
3. **Consistency** — the security policies of both components must be consistent; the dependent component must not undermine the base component's security.

Multiple levels of composition are possible: a component that is dependent in one composition may serve as the base in another.

> **CC 2022 note:** CC 2022 refined the ACO class and clarified the requirements for composed TOE evaluation. The fundamental concept remains consistent with CC 3.1 R5, but CC 2022 provides more explicit guidance on evidence reuse and multi-layer composition.

## Composed TOE vs. composite evaluation

These terms are related but distinct:

| Concept | Meaning |
|---|---|
| **Composed TOE** | The product itself — a TOE made of multiple components. |
| **[Composite evaluation](./CompositeEvaluation.md)** | The evaluation process — an evaluation that assesses the composed TOE, reusing results from prior component evaluations. |

## Practical guidance

### Preparing a composed TOE for evaluation

1. **Identify the components.** Clearly define which parts of the product constitute the base component and which constitute the dependent component. Document the [TOE boundary](./TOEBoundary.md) for the composed product.

2. **Verify base component certification.** Ensure the base component holds a valid, current evaluation certificate. Check that the base component's evaluated configuration matches the configuration used in the composed product.

3. **Define the reliance relationship.** Document exactly which security services of the base component the dependent component relies upon. Map these to specific [SFRs](./SecurityFunctionalRequirement.md) from the base component's [Security Target](./SecurityTarget.md).

4. **Identify the component interfaces.** Describe the interfaces through which the dependent component interacts with the base component. These must be consistent with the base component's evaluated [TSF interfaces](./TSFInterface.md).

5. **Assess security policy consistency.** Verify that the dependent component's security policy does not weaken or contradict the base component's policy. Document any assumptions the dependent component makes about the base component's behaviour.

6. **Prepare the composed TOE Security Target.** Write an ST for the composed TOE that:
   - Describes both components and their roles.
   - Defines the composed TOE's security problem definition, objectives, and SFRs.
   - References the base component's certification.
   - Includes the ACO assurance requirements appropriate for the target assurance level.

7. **Develop composition evidence.** Prepare the evidence required by the ACO class:
   - **ACO_DEV** — composed TOE functional specification and design documentation.
   - **ACO_REL** — reliance characterisation (what the dependent component relies on).
   - **ACO_CTT** — composition testing (testing of the integrated product).
   - **ACO_VUL** — composition vulnerability analysis.
   - **ACO_COR** — correlation of composed TOE SFRs with component SFRs.

### Tips for composed TOE developers

- **Engage with the base component vendor early.** Access to the base component's evaluation evidence (or at least the ST and public certification report) is essential for demonstrating reliance and consistency.
- **Minimise the interface surface.** A narrower interface between components simplifies the reliance characterisation and reduces the composition vulnerability surface.
- **Plan for base component updates.** If the base component is re-evaluated or its certificate expires, the composed TOE may need maintenance evaluation. Design the reliance documentation to facilitate updates.

## Additional resources

- CC Part 3, ACO class — composition assurance requirements.
- CEM, ACO activities — evaluator sub-activities for composed TOE evaluation.
- CC Part 1, Annex A.5 — guidance on composed TOE Security Target development.
- ISO/IEC TR 15446 — guidance on composed TOE description and component interaction modelling.

## Related articles

- [Composite Evaluation](./CompositeEvaluation.md)
- [TOE Boundary](./TOEBoundary.md)
- [TOE Security Functionality](./TOESecurityFunctionality.md)
- [Sub-TOE Security Functionality](./SubTOESecurityFunctionality.md)
- [TSF Interface](./TSFInterface.md)
- [Security Target](./SecurityTarget.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
