---
Acronym: ACO_REL
CompLvl: |
  The components in this family are levelled according to the amount of detail provided in the description of the reliance by the dependent component upon the base component.
Name: Reliance of dependent component
Objectives: |
  The purpose of this family is to provide evidence that describes the reliance that a dependent component has upon the base component. This information is useful to persons responsible for integrating the component with other evaluated IT components to form the composed TOE, and for providing insight into the security properties of the resulting composition. This provides a description of the interface between the dependent and base components of the composed TOE that may not have been analysed during evaluation of the individual components, as the interfaces were not TSFIs of the individual component TOEs.
active: true
appNotes: |
  The Reliance of dependent component (ACO_REL) family considers the interactions between the components where the dependent component relies upon a service from the base component to support the operation of security functionality of the dependent component. The interfaces into these services of the base component may not have been considered during evaluation of the base component because the service in the base component was not considered security-relevant in the component evaluation, either because of the inherent purpose of the service (e.g. adjust type font) or because associated CC Part 2 SFRs are not being claimed in the base component´s ST (e.g. the login interface when no FIA: Identification and authentication SFRs are claimed). These interfaces into the base component are often viewed as functional interfaces in the evaluation of the base component, and are in addition to the security interfaces (TSFI) considered in the functional specification. In summary, the TSFIs described in the functional specification only include the calls made into a TSF by external entities and responses to those calls. Calls made by a TSF, which were not explicitly considered during evaluation of the components, are described by the reliance information provided to satisfy Reliance of dependent component (ACO_REL).
derived: false
level: 1.49
links:
- ACC-009: azX_w1Vo_f9F57VbWEtTiJw7ZF8ygj4WRojXlw4wCHo=
normative: true
ref: ''
reviewed: m7JKEeWCXGDp8hODAmBjwYzDaY4yXu27eWqgBpXyqG0=
---

# ACO_REL Reliance of dependent component