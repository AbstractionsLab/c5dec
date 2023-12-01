---
Acronym: ATE_COMP
CompLvl: This family contains only one component.
Name: Composite functional testing
Objectives: |
  The aim of this family is to determine whether the composite product as a whole exhibits the properties necessary to satisfy the functional requirements of its composite product ST.
active: true
appNotes: |
  A composite product can be tested by testing its components separately and by testing the integrated product. Separate testing means that its base component and its dependent component are being tested independently of each other. A lot of tests of the base component may have been performed within the scope of its accomplished evaluation. The dependent component may be tested on a simulator or an emulator, which represent a virtual machine. Integration testing means that the composite product is being tested as it is: the dependent component is running together with the related base component. Some dependent component functionality testing can only be performed on emulators, before its embedding/integration onto the base component, as effectiveness of this testing may not be visible using the interfaces of the composite product. Nevertheless, functional testing of the composite product shall be performed also on composite product samples according to the description of the security functions of the composite product and using the standard approach as required by the relevant ATE assurance class. No additional developer’s action is required here. Since the amount, the coverage and the depth of the functional tests of the base component have already been validated by the base component evaluation, it is not necessary to re-perform these tasks in the composite evaluation. Please note that the ETR for composite evaluation does not provide any information on functional testing for the base component. The behaviour of implementation of some SFRs can depend on properties of the base component as well as on the dependent component (e.g. correctness of the measures of the composite product to withstand a side channel attack or correctness of the implementation of tamper resistance against physical attacks). In such case the SFR implementation shall be tested on the final composite product, but not on a simulator or an emulator. This family focuses exclusively on testing of the composite product as a whole and represents merely partial efforts within the general test approach being covered by the assurance class ATE. These integration tests shall be specified and performed, whereby the approach of the standard assurance families of the class ATE shall be applied. The composite product evaluation sponsor shall ensure that the following is available for the composite product evaluator: — composite product samples suitable for testing.
derived: false
level: 1.44
links:
- ACC-007: YAf68vCm-XI37IKCyvgwLJYyF5drXUXePjDrlKQdJo4=
normative: true
ref: ''
reviewed: urgXpq5BZJicUeW06pe0ngOQawSFFywMscRXIHeDrDM=
---

# ATE_COMP Composite functional testing