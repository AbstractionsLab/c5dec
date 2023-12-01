---
Last Updated: October 4, 2023
Relevant CC Version: CC 2022
Tags: [Composite Evaluation]
---

# Composite Evaluation

**Acronym:** None

For IT products that are composed of several independent, already evaluated product components the composed security assurance can be evaluated. The composition of assurance is dependent upon:
- Type of composition, it is differentiated between layered, network or bi-directional, and embedded compositions.
- Security function policies, and [OSPs](./OrganizationalSecurityPolicy.md) that the component evaluation was based on:
- Claimed security assurance, for example the [assurance level](./EvaluationAssuranceLevel.md)
- The overall security policies for the entire product.

The CC only explicitly addresses the layered composition model. For bi-directional and embedded composition models [extended components](./ExtendedComponentDefinition.md) and [evaluation methods](./EvaluationMethods.md) have to be defined.

For the evaluation of layered [TOE](./TargetofEvaluation.md) compositions the CC defined the Composition class ACO in CC Part 3. In the layered composition two already evaluated TOEs are assumed one of which is defined to be the base TOE while the other is considered to be the dependent TOE. The evaluation of such a composed TOE consists of evaluating the interaction between both TOEs. CC Part 5 provides pre-defined Composition Assurance Packages that may be used for determining the composed TOE’s assurance level. The COMP related assurance families specified in CC Part 3 for the ADV, ALC, ASE, ATE and AVA classes provide evaluation criteria pertinent to composite products using this layered model. 
