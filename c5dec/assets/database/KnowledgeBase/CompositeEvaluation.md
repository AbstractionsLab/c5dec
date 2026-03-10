---
Last Updated: March 10, 2026
Relevant CC Version: CC 2022 (with CC 3.1 R5 notes)
Tags: composite-evaluation, ACO, composition, layered, base-TOE, dependent-TOE
---

# Composite Evaluation

For IT products that are composed of several independent, already evaluated product components the composed security assurance can be evaluated. The composition of assurance is dependent upon:
- Type of composition -- it is differentiated between layered, network or bi-directional, and embedded compositions.
- Security function policies and [OSPs](./OrganizationalSecurityPolicy.md) that the component evaluation was based on.
- Claimed security assurance, for example the [assurance level](./EvaluationAssuranceLevel.md).
- The overall security policies for the entire product.

The CC only explicitly addresses the layered composition model. For bi-directional and embedded composition models [extended components](./ExtendedComponentDefinition.md) and [evaluation methods](./EvaluationMethods.md) have to be defined.

For the evaluation of layered [TOE](./TargetofEvaluation.md) compositions the CC defined the Composition class ACO in CC Part 3. In the layered composition two already evaluated TOEs are assumed, one of which is defined to be the **base TOE** while the other is considered to be the **dependent TOE**. The evaluation of such a composed TOE consists of evaluating the interaction between both TOEs. CC Part 5 provides pre-defined Composition Assurance Packages that may be used for determining the composed TOE's assurance level.

## Composition models

| Model | Description | CC Part 3 support |
|-------|-------------|-------------------|
| **Layered** | Dependent TOE sits on top of the base TOE and relies on its services through a well-defined interface (e.g., a smartcard application running on a certified smartcard platform). | Directly addressed by ACO class. |
| **Network / Bi-directional** | Two TOEs communicate as peers, each relying on security services provided by the other (e.g., a TLS client and TLS server). | Requires extended components and custom evaluation methods. |
| **Embedded** | One TOE is physically integrated within the other and shares hardware/software resources (e.g., a crypto library compiled into a larger application). | Requires extended components and custom evaluation methods. |

## ACO assurance class

The ACO (Composition) class in CC Part 3 defines the following families for layered composition:

| Family | Purpose |
|--------|---------|
| **ACO_COR** | Composition rationale -- demonstrates that the base and dependent TOE interact correctly and that the composed TOE's security objectives are met. |
| **ACO_DEV** | Development evidence -- provides design information about the dependent TOE's use of the base TOE's interfaces. |
| **ACO_REL** | Reliance of dependent component -- documents which base TOE services the dependent TOE relies upon and any assumptions it makes. |
| **ACO_CTT** | Composition testing -- testing of the interfaces between the base and dependent TOEs. |
| **ACO_VUL** | Composition vulnerability analysis -- focuses on vulnerabilities introduced by the composition itself, not already covered by individual component evaluations. |

## Practical guidance

### Preparing a composite evaluation

1. **Verify component certifications are current.** Both the base and dependent TOE must hold valid CC certificates. Expired or superseded certificates may require re-evaluation. Check that the certified configurations match the actual deployment.
2. **Identify the composition model.** Determine whether the relationship is layered, network, or embedded. If not layered, consult the scheme about acceptable extended evaluation approaches.
3. **Define the composed TOE boundary.** The [TOE boundary](./TOEBoundary.md) of the composed TOE encompasses both components. Clearly document which interfaces are internal (base-to-dependent) and which are external.
4. **Develop the composition rationale (ACO_COR).** Demonstrate that the security objectives of the composed TOE are met by combining the security properties of the base and dependent TOEs. Show that the dependent TOE's assumptions about the base TOE are satisfied by the base TOE's certified security properties.
5. **Document reliance (ACO_REL).** For each service the dependent TOE calls on the base TOE, identify the base TOE's TSFI used, the security property relied upon, and any configuration constraints.
6. **Plan composition testing (ACO_CTT).** Focus tests on the interface between the two TOEs. The goal is to confirm that the integration does not break the security properties established during individual evaluations.
7. **Analyse composition vulnerabilities (ACO_VUL).** Look specifically for vulnerabilities that arise from the interaction -- e.g., incorrect parameter passing, privilege escalation through combined API calls, or timing dependencies between components.

### Common challenges

- **Version mismatch:** The base TOE's certified version may differ from the version actually deployed in the composed product. This must be resolved before evaluation.
- **Incomplete interface documentation:** The base TOE's evaluation evidence may not fully document the interfaces the dependent TOE uses. The base TOE developer may need to provide additional information.
- **Assurance level alignment:** The composed TOE's overall assurance level is limited by the weaker of the two component evaluations. In the [EUCC](./EUCC.md) context, a "high" composed evaluation requires both components to have "high" level certificates.

> **CC 2022 note:** CC 2022 Part 5 introduces formal Composition Assurance Packages (COMP packages) to standardise the assurance requirements for composed evaluations, complementing the ACO class from Part 3.

## Additional resources

- CC 2022 Part 3, ACO class -- composition assurance families and components.
- CC 2022 Part 5 -- Composition Assurance Packages (COMP).
- CEM, ACO-related evaluation activities.
- EUCC scheme documentation -- composite evaluation procedures for smartcard and HSM products.

## Related articles

- [Composed TOE](./ComposedTOE.md)
- [Evaluation Assurance Levels](./EvaluationAssuranceLevel.md)
- [Security Assurance Requirements](./SecurityAssuranceRequirement.md)
- [TOE Boundary](./TOEBoundary.md)
- [Extended Component Definition](./ExtendedComponentDefinition.md)
- [Evaluation Methods](./EvaluationMethods.md)
- [EUCC](./EUCC.md)
