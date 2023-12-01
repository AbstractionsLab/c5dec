---
Acronym: AVA_COMP
CompLvl: This family contains only one component.
Name: Composite vulnerability assessment
Objectives: |
  The aim of this family is to determine the exploitability of flaws or weaknesses in the composite product as a whole in the intended environment.
active: true
appNotes: |
  This family focuses exclusively on the vulnerability assessment of the composite product as a whole and represents merely partial efforts within the general approach being covered by the standard, i.e. as defined by the CEM, assurance family of the class AVA: AVA_VAN. The composite product evaluator shall perform a vulnerability analysis for the composite product using, amongst other, the results of the base component evaluation. This vulnerability analysis shall be confirmed by penetration testing. The composite product evaluator shall check that the confidentiality protection of the dependent component embedded into/installed onto the base component is consistent with the confidentiality level claimed by the dependent component developer for ALC_DVS. In special cases, the vulnerability analysis and the definition of attacks can be difficult, need considerable time and require extensive pre-testing, if only documentation is available. The base component may also be used in a way that was not foreseen by the base component developer and the base component evaluator, or the dependent component developer may not have followed the stipulations provided with the base component. Different possibilities exist to shorten composite product vulnerability analysis in such cases: E.g. the composite product evaluator may consult the base component evaluator and draw on his experience gained during the base component evaluation. Alternatively, an approach aiming on the separation of vulnerabilities of the dependent component and the base component by using specific test samples of the base component on which the composite product evaluator may load test dependent components on his own discretion. The intention hereby is to use test dependent components without countermeasures and without deactivating any base component inherent countermeasure. The results of the vulnerability assessment for the base component of the composite product represented in the ETR for composite evaluation can be re-used under the following conditions: they are up-to-date and all composite activities for correctness – ASE_COMP.1, ALC_COMP.1, ADV_COMP.1 and ATE_COMP.1 – are finalised with the verdict PASS. Due to composing of the base component and the dependent component a new quality arises, which may cause additional vulnerabilities of the base component which might be not mentioned in the ETR for composite evaluation. In these circumstances the composite product evaluation authority may require a re-assessment or re-evaluation of the base component focusing on the new vulnerabilities’ issues. The composite product evaluation sponsor shall ensure that the following is made available for the composite product evaluator: — the base component-related user guidance, — the base component-related ETR for composite evaluation prepared by the base component evaluator, — the report of the base component evaluation authority.
derived: false
level: 1.46
links:
- ACC-008: zahaVAS6NyfjqrqwUib2DaTs5HH8LxKOgakBXBgihL0=
normative: true
ref: ''
reviewed: t1px8RZ4D_N8MsWpCsjMJj0htLMvEJuI4YCryhLH9EE=
---

# AVA_COMP Composite vulnerability assessment