---
Acronym: ASE_COMP
CompLvl: This family contains only one component.
Name: Consistency of composite product Security Target
Objectives: |
  The aim of this family is to determine whether the ST of the composite product (denoted by composite product Security Target or composite-ST in the following) does not contradict the ST of the related base component (denoted by base component Security Target or base-ST in the following, Generally, a Security Target expresses a security policy for the TOE defined.)
active: true
appNotes: |
  A ST for the composite product shall be written and evaluated. The composite product evaluator shall examine that the ST of the composite product does not contradict the ST of the related base component. In particular, it means that the composite product evaluator shall examine the composite product ST and the base component ST for any conflicting assumptions, compatibility of security objectives, security requirements and security functionality needed by the dependent component. The composite product evaluation sponsor shall ensure that the ST of the base component is available for the dependent component developer, for the composite product evaluator and for the composite product evaluation authority. The information available in the public version of the base component ST may not be sufficient. These application notes aid the developer to create as well as the evaluator to analyse a composite product ST and describe a general methodology for it. In order to create a composite product ST, the developer should perform the following steps: Step 1: The developer formulates a preliminary ST for the composite product (the composite-ST) using the standard code of practice. The composite-ST can be formulated independently of the ST of the composite product’s related base component (the base-ST), at least as long as there are no formal PP conformance claims. Step 2: The developer determines the overlap between the base-ST and the composite-ST through analysing and comparing their respective TOE Security Functionality (TSF). Because the TSF enforce the Security Target (together with the organisational measures enforcing the security objectives for the operational environment of the TOE). The comparison shall be performed on the abstraction level of SFRs. If the developer defined security functionality groups (TSF-groups) in the TSS part of his Security Target, the evaluator should also consider them in order to get a better understanding for the context of the security services offered by the TOE. Step 3: The developer determines under which conditions he can trust in and rely on the base component-TSF being used by the composite-ST without a new examination. Having undertaken these steps the developer completes the preliminary ST for the composite product. It is not mandatory that the composite product and its related base component are being evaluated according to the same edition of the CC. It is due to the fact that the dependent component of the composite product can rely on some security services of the base component, if (i) the assurance level of the base component covers the intended assurance level of the composite product and (ii) the base component evaluation is valid (i.e. accepted by the base component evaluation authority) and up-to-date. Equivalence of single assurance components (and, hence, of assurance levels) belonging to different CC editions shall be established / acknowledged by the composite product evaluation authority. If conformance to a PP is claimed, e.g. a composite product ST claims conformance to a PP (that possibly claims conformance to a further PP), the consistency check can be reduced to the elements of the ST having not already been covered by these PPs. However, in general the fact of compliance to a PP is not sufficient to avoid inconsistencies. Assume the following situation, where → stands for “complies with”: composite-ST → PP 1 → PP 2 ← base-ST PP 1 may require any kind of conformance, e.g. “strict”, “exact” or “demonstrable” according to the CC, but this does not affect the ‘additional elements’ that the base-ST may introduce beyond PP 2. In conclusion, these additions are not necessarily consistent with the composite-ST’s additions chosen beyond PP 1. There is no scenario that ensures their consistency ‘by construction’. Note that consistency may be no direct matching: Objectives for the base component’s environment may become objectives for the composite TOE.
derived: false
level: 1.21
links:
- ACC-003: zRIUAa5ibXIpURMErU9sp70OpLbHeOt92QB6vM4F6fA=
normative: true
ref: ''
reviewed: p59aQSBBZ5gpmO4MayQ_56XsHDhJDpfuUDmxYl1aJI8=
---

# ASE_COMP Consistency of composite product Security Target