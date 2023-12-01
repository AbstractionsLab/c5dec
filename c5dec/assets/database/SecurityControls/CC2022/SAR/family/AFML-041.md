---
Acronym: ATE_DPT
CompLvl: |
  The components in this family are levelled on the basis of increasing detail provided in the TSF representations, from the TOE design to the implementation representation. This levelling reflects the TSF representations presented in the ADV class.
Name: Depth
Objectives: |
  The components in this family deal with the level of detail to which the TSF is tested by the developer. Testing of the TSF is based upon increasing depth of information derived from additional design representations and descriptions (TOE design, implementation representation, and security architecture description). The objective is to counter the risk of missing an error in the development of the TOE. Testing that exercises specific internal interfaces can provide assurance not only that the TSF exhibits the desired external security behaviour, but also that this behaviour stems from correctly operating internal functionality.
active: true
appNotes: |
  The TOE design describes the internal components (e.g. subsystems) and, perhaps, modules of the TSF, together with a description of the interfaces among these components and modules. Evidence of testing of this TOE design must show that the internal interfaces have been exercised and seen to behave as described. This may be achieved through testing via the external interfaces of the TSF, or by testing of the TOE subsystem or module interfaces in isolation, perhaps employing a test harness. In cases where some aspects of an internal interface cannot be tested via the external interfaces, there should either be justification that these aspects need not be tested, or the internal interface needs to be tested directly. In the latter case the TOE design needs to be sufficiently detailed in order to facilitate direct testing. In cases where the description of the TSF´s architectural soundness [in Security Architecture (ADV_ARC)] cites specific mechanisms, the tests performed by the developer must show that the mechanisms have been exercised and seen to behave as described. At the highest component of this family, the testing is performed not only against the TOE design, but also against the implementation representation.
derived: false
level: 1.41
links:
- ACC-007: YAf68vCm-XI37IKCyvgwLJYyF5drXUXePjDrlKQdJo4=
normative: true
ref: ''
reviewed: YGVWCiGnw4lI1qlaOHzXR3-5p7m8CtiU-k1IyGioP-0=
---

# ATE_DPT Depth