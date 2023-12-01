---
Acronym: ATE_FUN
CompLvl: |
  This family contains two components, the higher requiring that ordering dependencies are analysed.
Name: Functional tests
Objectives: |
  Functional testing performed by the developer provides assurance that the tests in the test documentation are performed and documented correctly. The correspondence of these tests to the design descriptions of the TSF is achieved through the Coverage (ATE_COV) and Depth (ATE_DPT) families. This family contributes to providing assurance that the likelihood of undiscovered flaws is relatively small. The families Coverage (ATE_COV), Depth (ATE_DPT) and Functional tests (ATE_FUN) are used in combination to define the evidence of testing to be supplied by a developer. Independent functional testing by the evaluator is specified by Independent testing (ATE_IND).
active: true
appNotes: |
  Procedures for performing tests are expected to provide instructions for using test programs and test suites, including the test environment, test conditions, test data parameters and values. The test procedures should also show how the test results are derived from the test inputs. Ordering dependencies are relevant when the successful execution of a particular test depends upon the existence of a particular state. For example, this can require that test A be executed immediately before test B, since the state resulting from the successful execution of test A is a prerequisite for the successful execution of test B. Thus, failure of test B can be related to a problem with the ordering dependencies. In the above example, test B can fail because test C (rather than test A) was executed immediately before it, or the failure of test B can be related to a failure of test A.
derived: false
level: 1.42
links:
- ACC-007: YAf68vCm-XI37IKCyvgwLJYyF5drXUXePjDrlKQdJo4=
normative: true
ref: ''
reviewed: my-_MMKspXlc_EKYlxZA2yi6mtgRqMkb_VZ2QJ__yzQ=
---

# ATE_FUN Functional tests