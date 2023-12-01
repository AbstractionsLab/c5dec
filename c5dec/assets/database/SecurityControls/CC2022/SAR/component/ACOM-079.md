---
AppNotes: |
  In this component the developer is required to show how tests in the test documentation correspond to all of the TSFIs in the functional specification. This can be achieved by a statement of correspondence, perhaps using a table, but in addition the developer is required to demonstrate that the tests exercise all of the parameters of all TSFIs. This additional requirement includes bounds testing (i.e. verifying that errors are generated when stated limits are exceeded) and negative testing (e.g. when access is given to User A, verifying not only that User A now has access, but also that User B did not suddenly gain access). This kind of testing is not, strictly speaking, exhaustive because not every possible value of the parameters is expected to be checked.
Dependencies: |
  ADV_FSP.2 Security-enforcing functional specification, ATE_FUN.1 Functional testing
Id: ATE_COV.3
Name: Rigorous analysis of coverage
Objectives: |
  In this component, the objective is to confirm that the developer performed exhaustive tests of all interfaces in the functional specification. The objective of this component is to confirm that all parameters of all of the TSFIs have been tested.
active: true
derived: false
level: 1.78
links:
- AFML-040: fFaCJcNWyEUZwcuFqVFnWMc5OcL66E8dERjovQS59D8=
normative: true
ref: ''
reviewed: bFpKKt3jkgLJ-IcCfcMiL9-GEdhYhqwbrn0JTH096BA=
---

# ATE_COV.3 Rigorous analysis of coverage