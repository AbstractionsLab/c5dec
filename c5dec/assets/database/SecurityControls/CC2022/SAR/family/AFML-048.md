---
Acronym: ACO_DEV
CompLvl: |
  The components are levelled on the basis of increasing amounts of detail about the interfaces provided, and how they are implemented.
Name: Development evidence
Objectives: |
  This family sets out requirements for a specification of the base component in increasing levels of detail. Such information is required to gain confidence that the appropriate security functionality is provided to support the requirements of the dependent component (as identified in the reliance information).
active: true
appNotes: |
  The TSF of the base component is often defined without knowledge of the dependencies of the possible applications with which it may by composed. The TSF of this base component is defined to include all parts of the base component that have to be relied upon for enforcement of the base component SFRs. This will include all parts of the base component required to implement the base component SFRs. The functional specification of the base component will describe the TSFI in terms of the interfaces the base component provides to allow an external entity to invoke operations of the TSF. This includes interfaces to the human user to permit interaction with the operation of the TSF invoking SFRs and also interfaces allowing an external IT entity to make calls into the TSF. The functional specification only provides a description of what the TSF provides at its interface and the means by which that TSF functionality are invoked. Therefore, the functional specification does not necessarily provide a complete interface specification of all possible interfaces available between an external entity and the base component. It does not include what the TSF expects/requires from the operational environment. The description of what a dependent component TSF relies upon of a base component is considered in Reliance of dependent component (ACO_REL) and the development information evidence provides a response to the interfaces specified. The development information evidence includes a specification of the base component. This may be the evidence used during evaluation of the base component to satisfy the ADV requirements, or may be another form of evidence produced by either the base component developer or the composed TOE developer. This specification of the base component is used during Development evidence (ACO_DEV) to gain confidence that the appropriate security functionality is provided to support the requirements of the dependent component. The level of detail required of this evidence increases to reflect the level of required assurance in the composed TOE. This is expected to broadly reflect the increasing confidence gained from the application of the assurance packages to the components. The evaluator determines that this description of the base component is consistent with the reliance information provided for the dependent component.
derived: false
level: 1.48
links:
- ACC-009: azX_w1Vo_f9F57VbWEtTiJw7ZF8ygj4WRojXlw4wCHo=
normative: true
ref: ''
reviewed: xqBTQ1UBPFgRupQS6iggkHDv4_ZOJ5z92qgKg8ctDXk=
---

# ACO_DEV Development evidence