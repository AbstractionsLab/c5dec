---
Acronym: ACO_CTT
CompLvl: |
  The components in this family are levelled on the basis of increasing rigour of interface testing and increasing rigour of the analysis of the sufficiency of the tests to demonstrate that the composed TSF operates in accordance with the reliance information and the composed TOE SFRs.
Name: Composed TOE testing
Objectives: |
  This family requires that testing of composed TOE and testing of the base component, as used in the composed TOE, is performed.
active: true
appNotes: |
  There are two distinct aspects of testing associated with this family: a) testing of the interfaces between the base component and the dependent component, which the dependent component rely upon for enforcement of security functionality, to demonstrate their compatibility; b) testing of the composed TOE to demonstrate that the TOE behaves in accordance with the SFRs for the composed TOE. If the test configurations used during evaluation of the dependent component included use of the base component as a “platform” and the test analysis sufficiently demonstrates that the TSF behaves in accordance with the SFRs, the developer need perform no further testing of the composed TOE functionality. However, if the base component was not used in the testing of the dependent component, or the configuration of either component varied, then the developer is to perform testing of the composed TOE. This may take the form of repeating the dependent component developer testing of the dependent component, provided this adequately demonstrates the composed TOE TSF behaves in accordance with the SFRs. The developer is to provide evidence of testing the base component interfaces used in the composition. The operation of base component TSFIs would have been tested as part of the ATE: Tests activities during evaluation of the base component. Therefore, provided the appropriate interfaces were included within the test sample of the base component evaluation and it was determined in Composition rationale (ACO_COR) that the base component is operating in accordance with the base component evaluated configuration, with all security functionality required by the dependent component included in the TSF, the evaluator action ACO_CTT.1.1E may be met through reuse of the base component ATE: Tests verdicts. If this is not the case, the base component interfaces used relevant to the composition that are affected by any variations to the evaluated configuration and any additional security functionally will be tested to ensure they demonstrate the expected behaviour. The expected behaviour to be tested is that described in the reliance information [reliance of dependent component (ACO_REL) evidence].
derived: false
level: '1.50'
links:
- ACC-009: azX_w1Vo_f9F57VbWEtTiJw7ZF8ygj4WRojXlw4wCHo=
normative: true
ref: ''
reviewed: CVwXIq250z6eBNPRcJ8qT8GN4z3jvk7OqAszvJEtSKY=
---

# ACO_CTT Composed TOE testing