---
Acronym: ADV_ARC
CompLvl: This family contains only one component.
Name: Security Architecture
Objectives: |
  The objective of this family is for the developer to provide a description of the security architecture of the TSF. This will allow analysis of the information that, when coupled with the other evidence presented for the TSF, will confirm the TSF achieves the desired properties. The security architecture descriptions support the implicit claim that security analysis of the TOE can be achieved by examining the TSF; without a sound architecture, the entire TOE functionality would have to be examined.
active: true
appNotes: |
  The properties of self-protection, domain separation, and non-bypassability are distinct from security functionality expressed by CC Part 2 SFRs because self-protection and non-bypassability largely have no directly observable interface at the TSF. Rather, they are properties of the TSF that are achieved through the design of the TOE and TSF and enforced by the correct implementation of that design. The approach used in this family is for the developer to design and provide a TSF that exhibits the above-mentioned properties, and to provide evidence (in the form of documentation) that explains these properties of the TSF. This explanation is provided at the same level of detail as the description of the SFR-enforcing elements of the TOE in the TOE design document. The evaluator has the responsibility for looking at the evidence and, coupled with other evidence delivered for the TOE and TSF, determining that the properties are achieved. Specification of security functionality implementing the SFRs [in the Functional specification (ADV_FSP) and TOE design (ADV_TDS)] will not necessarily describe mechanisms employed in implementing self-protection and non-bypassability (e.g. memory management mechanisms). Therefore, the material needed to provide the assurance that these requirements are being achieved is better suited to a presentation separate from the design decomposition of the TSF as embodied in ADV_FSP and ADV_TDS. This is not to imply that the security architecture description called for by this component cannot reference or make use of the design decomposition material; but it is likely that much of the detail present in the decomposition documentation will not be relevant to the argument being provided for the security architecture description document. The description of architectural soundness can be thought of as a developer´s vulnerability analysis, in that it provides the justification for why the TSF is sound and enforces all of its SFRs. Where the soundness is achieved through specific security mechanisms, these will be tested as part of the Depth (ATE_DPT) requirements; where the soundness is achieved solely through the architecture, the behaviour will be tested as part of the AVA: Vulnerability assessment requirements. This family consists of requirements for a security architecture description that describes the self-protection, domain separation, non-bypassability principles, including a description of how these principles are supported by the parts of the TOE that are used for TSF initialisation. In case of a multi-assurance evaluation the properties of self-protection, domain separation, and non-bypassability may also be described for boundaries between the sub-TSF. Additional information on the security architecture properties of self-protection, domain separation, and non-bypassability can be found in A.1, ADV_ARC: Supplementary material on security architectures.
derived: false
level: 1.22
links:
- ACC-004: mOqg7LdyAc27RjJaidUMtlTnrW35Rvci4zjd34LpczE=
normative: true
ref: ''
reviewed: O7Ilp1sj80cC3wyGXdOlxtvLsfFPhuccJrALGvIcS2c=
---

# ADV_ARC Security Architecture