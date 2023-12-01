---
Acronym: ALC_TDA
CompLvl: |
  The components in this family are levelled on the basis of increasing cross-checking for consistency with relevant evidence from components of other families of other security assurance classes.
Name: TOE Development Artefacts
Objectives: |
  This family aims to add trust to the development process or a development. It focuses on the generation of certain artefacts in the development process. These artefacts are used at a later point in time to assess the degree to which the development process is trustable. This trust is realized through the validation of the generated artefacts for confirming them as sufficient evidence for trustable development. This family introduces developer practices within the development process to generate the required artefacts for realizing trustable development. If a requirement in this family does not explicitly specify the use of automation to generate the required artefacts, the developer is free to undertake the corresponding practice manually, or to use some integrated automation in the development process, or to use a hybrid method of both. It is expected that the degree of trust in the development process is proportional to the degree of automation adoption to implement the corresponding practice in the development process. This family also has a relationship with the ALC_TAT family. As ALC_TAT focuses on the tools and techniques aspect for developing, analysing, and implementing the TOE, it provides the necessary context when describing the practices of this family being introduced into the development process.
active: true
appNotes: |
  The requirements in ALC_TDA.1 provide a degree of trust in the developer’s ability to identify the set of implementation representation which actually has been used during the TOE generation time. This degree of trust helps to positively answer the question “is that really the source code for this software” or “is that really the register-transfer level (RTL) design or description for this integrated circuit hardware”” or “is that really the set of implementation representation for this TOE”, which is potentially relevant in an evaluation. Such degree of trust is built on a) the timing of when the set of implementation representation identifiers is recorded or logged, b) the integrity and authenticity of the record of implementation representation identifiers, and c) the traceability of implementation representation identifiers from the TOE. In the case where some implementation representation elements are also covered in the configuration list due to ALC_CMS.3, the requirements in ALC_TDA.2 make sure that these implementation representation elements actually are identifiable through the use of the implementation representation identifiers of ALC_TDA.1. With the accurate recording or logging of the actual implementation representation being used by the development tools under the scope of ALC_TAT, it provides an additional evidence to convince a third party that a regeneration of the TOE is functionally equivalent to the original TOE. The requirements in ALC_TDA.3 provide the developer an opportunity to testify the absence of functional differences between the two possibly visibly different TOEs which have been independently generated from the identical set of implementation representation.
derived: false
level: 1.37
links:
- ACC-006: YQ8i2ZUSt6kGDyuv_uHQtZ_Ad09nXbPtqfs-nxPsWWM=
normative: true
ref: ''
reviewed: 7Msk3KUyBb2ZkJuqFtMpo7PaGY08XpuMWUCyhoqk54M=
---

# ALC_TDA TOE Development Artefacts