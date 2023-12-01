---
Acronym: ATE_IND
CompLvl: |
  Levelling is based upon the amount of developer test documentation and test support and the amount of evaluator testing.
Name: Independent testing
Objectives: |
  The objectives of this family are built upon the assurances achieved in the ATE_FUN, ATE_COV, and ATE_DPT families by verifying the developer testing and performing additional tests by the evaluator.
active: true
appNotes: |
  This family deals with the degree to which there is independent functional testing of the TSF. Independent functional testing may take the form of repeating the developer´s functional tests (in whole or in part) or of extending the scope or the depth of the developer´s tests. These activities are complementary, and an appropriate mix must be planned for each TOE, which takes into account the availability and coverage of test results, and the functional complexity of the TSF. Sampling of developer tests is intended to provide confirmation that the developer has carried out his planned test programme on the TSF and has correctly recorded the results. The size of sample selected will be influenced by the detail and quality of the developer´s functional test results. The evaluator will also need to consider the scope for devising additional tests, and the relative benefit that may be gained from effort in these two areas. It is recognized that repetition of all developer tests may be feasible and desirable in some cases, but may be very arduous and less productive in others. The highest component in this family should therefore be used with caution. Sampling will address the whole range of test results available, including those supplied to meet the requirements of both Coverage (ATE_COV) and Depth (ATE_DPT). There is also a need to consider the different configurations of the TOE that are included within the evaluation. The evaluator will need to assess the applicability of the results provided, and to plan his own testing accordingly. The suitability of the TOE for testing is based on the access to the TOE, and the supporting documentation and information required (including any test software or tools) to run tests. The need for such support is addressed by the dependencies to other assurance families. Additionally, suitability of the TOE for testing may be based on other considerations. For example, the version of the TOE submitted by the developer may not be the final version. The term interfaces refers to interfaces described in the functional specification and TOE design, and parameters passed through invocations identified in the implementation representation. The exact set of interfaces to be used is selected through Coverage (ATE_COV) and the Depth (ATE_DPT) components. References to a subset of the interfaces are intended to allow the evaluator to design an appropriate set of tests which is consistent with the objectives of the evaluation being conducted.
derived: false
level: 1.43
links:
- ACC-007: YAf68vCm-XI37IKCyvgwLJYyF5drXUXePjDrlKQdJo4=
normative: true
ref: ''
reviewed: AK7umopUcByxAUhXlQYc_xcVnpLi1yXt8hKmwHy5HPM=
---

# ATE_IND Independent testing